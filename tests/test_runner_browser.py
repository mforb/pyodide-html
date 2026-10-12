"""Real-browser regression checks. Run: python tests/test_runner_browser.py."""
import base64
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from urllib.parse import parse_qs, urlencode, urlparse
import re

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def check_materials():
    html = (ROOT / 'moodle_class2.html').read_text()
    blocks = re.findall(r'<!-- START TASK (\d+):.*?<!-- END TASK \1 -->', html, re.S)
    assert blocks == [str(i) for i in range(1, 13)]
    links = re.findall(r'<iframe src="([^"]+)"', html)
    assert len(links) == 12
    for index, link in enumerate(links, 1):
        url = urlparse(link)
        assert url.path == '/pyodide-html/runner_link.html'
        starter = ROOT / parse_qs(url.query)['file'][0]
        assert starter.is_file(), starter
        source = starter.read_text()
        if index == 10:
            try:
                compile(source, str(starter), 'exec')
            except SyntaxError:
                pass
            else:
                raise AssertionError('The debugging starter should have a syntax error')
        else:
            compile(source, str(starter), 'exec')
    return links


def open_runner(page, base, **params):
    page.goto(base + '/runner_link.html' + ('?' + urlencode(params) if params else ''))
    page.wait_for_function("document.getElementById('status').textContent === 'Pyodide Ready'", timeout=120000)


def run(page, code):
    page.evaluate('(code) => editor.setValue(code, -1)', code)
    page.evaluate('runPython()')
    return page.locator('#output > div').last.text_content()


def clean_error(page, code, ending):
    output = run(page, code)
    assert output.endswith(ending), output
    assert '<exec>' not in output, output
    assert 'pyodide.asm' not in output and 'wasm-function' not in output, output
    assert not re.search(r'^\s+at ', output, re.M), output
    assert page.locator('#output > div').last.get_attribute('class') == 'run-error'
    return output


def main():
    links = check_materials()
    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(QuietHandler, directory=str(ROOT)))
    Thread(target=server.serve_forever, daemon=True).start()
    base = f'http://127.0.0.1:{server.server_port}'
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            context = browser.new_context(ignore_https_errors=True)
            page = context.new_page()
            failures = []
            page.on('pageerror', lambda error: failures.append(str(error)))

            # Real relative-file loading and independent saved drafts.
            first = 'exercises/class2/01_readings.py'
            original = (ROOT / first).read_text()
            open_runner(page, base, file=first)
            assert page.evaluate('editor.getValue()') == original
            page.evaluate('editor.setValue("print(123)", -1); saveNow()')
            page.reload()
            page.wait_for_function("document.getElementById('status').textContent === 'Pyodide Ready'", timeout=120000)
            assert page.evaluate('editor.getValue()') == 'print(123)'
            page.once('dialog', lambda dialog: dialog.dismiss())
            page.locator('#reset-btn').click()
            assert page.evaluate('editor.getValue()') == 'print(123)'
            page.once('dialog', lambda dialog: dialog.accept())
            page.locator('#reset-btn').click()
            assert page.evaluate('editor.getValue()') == original
            second = 'exercises/class2/02_text_slices.py'
            open_runner(page, base, file=second)
            assert page.evaluate('editor.getValue()') == (ROOT / second).read_text()

            # Literal text must not be guessed as base64; URL special characters
            # and Unicode survive both text and explicitly encoded starters.
            open_runner(page, base, code='pass', file='missing.py')
            assert page.evaluate('editor.getValue()') == 'pass'
            assert run(page, 'pass') == '(Code executed with no output)'
            text = 'print("Māori + # & café")\nprint(2 + 3)'
            open_runner(page, base, code=text)
            assert page.evaluate('editor.getValue()') == text
            assert run(page, text) == 'Māori + # & café\n5'
            encoded = base64.b64encode(text.encode()).decode()
            assert page.evaluate('(value) => loadStarter(codeSource(new URLSearchParams({code64: value})))', encoded) == text
            assert page.evaluate('(value) => loadStarter(codeSource(new URLSearchParams({text: value})))', text) == text
            assert page.evaluate('loadStarter(codeSource(new URLSearchParams({file: "README.md"})))').startswith('# pyodide-html')

            # Ordinary anchor hrefs open the supplied starter too.
            href = base + '/runner_link.html?' + urlencode({'text': 'print("from a link")'})
            page.evaluate('(href) => { const a = document.createElement("a"); a.id = "test-link"; a.href = href; a.textContent = "Open"; document.body.appendChild(a); }', href)
            page.locator('#test-link').click()
            page.wait_for_function("document.getElementById('status').textContent === 'Pyodide Ready'", timeout=120000)
            assert page.evaluate('editor.getValue()') == 'print("from a link")'

            # Clean Python errors, including compile-time errors and exceptions
            # with chained causes, while keeping student line numbers and output.
            output = clean_error(page, 'print("before")\nraise ValueError("bad reading")', 'ValueError: bad reading')
            assert output.startswith('before\nTraceback') and 'line 2' in output
            clean_error(page, 'print(missing)', "NameError: name 'missing' is not defined")
            clean_error(page, 'print([1][3])', 'IndexError: list index out of range')
            clean_error(page, 'print({"temp_c": 1}["temp"])', "KeyError: 'temp'")
            clean_error(page, 'if True\n    print(1)', "SyntaxError: expected ':'")
            clean_error(page, 'if True:\nprint(1)', "IndentationError: expected an indented block after 'if' statement on line 1")
            clean_error(page, 'if a = 1:\n    pass', "SyntaxError: invalid syntax. Maybe you meant '==' or ':=' instead of '='?")
            output = clean_error(page, 'try:\n    1/0\nexcept ZeroDivisionError as error:\n    raise ValueError("outer") from error', 'ValueError: outer')
            assert 'ZeroDivisionError: division by zero' in output
            clean_error(page, 'raise SystemExit("stopped")', 'SystemExit: stopped')
            output = run(page, 'import sys\nprint("ok")\nsys.stderr.write("warning\\n")')
            assert output == 'ok\nwarning'

            # input() echoes the prompt/reply, cancellation is a clean error,
            # and the original input() is restored after each run.
            page.once('dialog', lambda dialog: dialog.accept('2.5'))
            assert run(page, 'value = float(input("Reading: "))\nprint(value * 2)') == 'Reading: 2.5\n5.0'
            page.once('dialog', lambda dialog: dialog.dismiss())
            clean_error(page, 'input("Reading: ")', 'KeyboardInterrupt: Input cancelled')
            assert run(page, 'print(7)') == '7'
            clean_error(page, 'while True:\n    pass', 'RunTimeout: Your code was stopped after 5 seconds. Is there an infinite loop?')
            assert run(page, 'print("recovered")') == 'recovered'

            # Imported Pyodide packages, shortcut, concurrent-run guard, output
            # truncation/history, and localStorage-unavailable fallback.
            assert run(page, 'import numpy as np\nprint(np.sum([1, 2, 3]))') == '6'
            page.evaluate('editor.setValue("print(99)", -1)')
            previous = page.evaluate('runCount')
            page.locator('#editor textarea').press('Control+Enter')
            page.wait_for_function('(n) => runCount === n + 1 && !running', arg=previous)
            assert page.locator('#output > div').last.text_content() == '99'
            output = run(page, 'print("x" * 50001)')
            assert '[Output truncated' in output
            page.evaluate('clearConsole()')
            assert page.locator('#output').text_content() == ''
            assert page.locator('#run-count').text_content() == ''
            page.evaluate('''() => {
                const original = Storage.prototype.setItem;
                Storage.prototype.setItem = () => { throw new Error('Blocked'); };
                saveNow();
                Storage.prototype.setItem = original;
            }''')
            assert page.locator('#save-status').text_content() == 'Auto-save unavailable'
            page.evaluate('''async () => {
                editor.setValue('print(42)', -1);
                await Promise.all([runPython(), runPython()]);
            }''')
            assert page.evaluate('runCount') == 1

            # Invalid starter URLs never overwrite a saved draft or silently
            # install a 404/HTML page as the reset baseline.
            bad = context.new_page()
            bad.goto(base + '/runner_link.html?file=missing.py')
            bad.wait_for_function("document.getElementById('status').textContent.startsWith('Could not load starter code:')")
            assert 'HTTP 404' in bad.locator('#status').text_content()
            assert bad.locator('#run-btn').is_disabled()
            assert bad.evaluate('storageKey') == ''
            bad.goto(base + '/runner_link.html?file=index.html')
            bad.wait_for_function("document.getElementById('status').textContent.includes('HTML page')")
            bad.close()

            # Check real iframe integration separately from the Moodle preview.
            iframe_page = context.new_page()
            iframe_page.goto(base + '/index.html')
            iframe_page.evaluate('(src) => { document.body.innerHTML = ""; const frame = document.createElement("iframe"); frame.id = "runner-test"; frame.src = src; document.body.appendChild(frame); }', base + '/runner_link.html?' + urlencode({'code': 'print("iframe")'}))
            frame = iframe_page.frame_locator('#runner-test')
            frame.locator('#run-btn').wait_for()
            iframe_page.wait_for_function('document.querySelector("iframe").contentDocument.getElementById("status").textContent === "Pyodide Ready"', timeout=120000)
            frame.locator('#run-btn').click()
            frame.locator('#output').get_by_text('iframe', exact=True).wait_for()
            iframe_page.close()

            # Preview numbering and 12 iframe links, without starting 12 runtimes.
            preview = context.new_page()
            preview.route('https://mforb.github.io/pyodide-html/runner_link.html*', lambda route: route.fulfill(body='<p>Runner placeholder</p>', content_type='text/html'))
            preview.goto(base + '/moodle_class2.html')
            headings = preview.locator('h2').all_text_contents()
            assert len(headings) == 12
            for index, heading in enumerate(headings, 1):
                assert re.search(rf'Task 8\.{index}\s*:', heading), heading
            assert preview.locator('iframe').count() == len(links)
            assert not failures, failures
            browser.close()
        print('PASS: 12 exercise blocks/starters, URL loading, autosave/reset, href/iframe integration, clean Python errors, prompts, timeout, packages and controls.')
    finally:
        server.shutdown()
        server.server_close()


if __name__ == '__main__':
    main()
