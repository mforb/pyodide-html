let pyodide;
let editor;
let starterCode = '';
let storageKey = '';
let saveTimer;
let runCount = 0;
let running = false;

const MAX_OUTPUT_SIZE = 50000;
const RUN_TIMEOUT_SECONDS = 5;

function appendRun(text, isError) {
  const out = document.getElementById('output');
  const header = document.createElement('div');
  header.className = 'run-header';
  header.textContent = `Run #${runCount}  ·  ${new Date().toLocaleTimeString()}`;
  const body = document.createElement('div');
  if (isError) body.className = 'run-error';
  text = String(text);
  if (text.length > MAX_OUTPUT_SIZE) {
    text = text.slice(0, MAX_OUTPUT_SIZE) +
      `\n\n[Output truncated - exceeded maximum size of ${MAX_OUTPUT_SIZE} characters]`;
  }
  body.textContent = text.replace(/\n+$/, '');
  out.appendChild(header);
  out.appendChild(body);
  while (out.children.length > 100) out.removeChild(out.firstChild);
  out.scrollTop = out.scrollHeight;
  document.getElementById('run-count').textContent =
    `(${runCount} run${runCount === 1 ? '' : 's'})`;
}

function clearConsole() {
  runCount = 0;
  document.getElementById('output').innerHTML = '';
  document.getElementById('run-count').textContent = '';
}

function hashString(text) {
  let hash = 0;
  for (let i = 0; i < text.length; i++) hash = (hash * 31 + text.charCodeAt(i)) | 0;
  return (hash >>> 0).toString(36);
}

function codeSource(params) {
  // Explicit encodings avoid interpreting ordinary Python (e.g. "pass") as base64.
  if (params.has('code')) return {kind: 'code', value: params.get('code')};
  if (params.has('text')) return {kind: 'code', value: params.get('text')};
  if (params.has('code64')) return {kind: 'code64', value: params.get('code64')};
  if (params.has('file')) {
    return {kind: 'file', value: new URL(params.get('file'), location.href).href};
  }
  return {kind: 'default', value: '# Write your Python code here'};
}

function makeStorageKey(source) {
  const id = source.kind === 'file' ? 'file:' + source.value :
    source.kind + ':' + hashString(source.value);
  return 'pyrunner:' + location.pathname + ':' + id;
}

async function loadStarter(source) {
  if (source.kind === 'code64') {
    const bytes = Uint8Array.from(atob(source.value), character => character.charCodeAt(0));
    return new TextDecoder('utf-8', {fatal: true}).decode(bytes);
  }
  if (source.kind !== 'file') return source.value;
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), 15000);
  try {
    const response = await fetch(source.value, {signal: controller.signal});
    if (!response.ok) throw new Error(`HTTP ${response.status}: ${source.value}`);
    if ((response.headers.get('content-type') || '').includes('text/html')) {
      throw new Error('The starter link returned an HTML page. Use a raw .py or .txt file URL.');
    }
    return await response.text();
  } finally {
    clearTimeout(timer);
  }
}

function loadSaved() {
  try { return localStorage.getItem(storageKey); }
  catch (error) { return null; }
}

function saveNow() {
  if (!editor || !storageKey) return;
  const label = document.getElementById('save-status');
  try {
    localStorage.setItem(storageKey, editor.getValue());
    label.textContent = 'Saved ' + new Date().toLocaleTimeString();
  } catch (error) {
    label.textContent = 'Auto-save unavailable';
  }
}

function scheduleSave() {
  clearTimeout(saveTimer);
  saveTimer = setTimeout(saveNow, 500);
}

function resetCode() {
  if (editor && storageKey && confirm('Replace your code with the original starter code? This cannot be undone.')) {
    editor.setValue(starterCode, -1);
    saveNow();
  }
}

function runtimeMessage(error) {
  // Python exceptions are handled inside Python below. A loader/JS failure
  // should show its message, never the Pyodide JavaScript/WASM stack.
  return String(error.message || error).replace(/\n\s+at (?:.*\n?)*$/, '').trimEnd();
}

async function init() {
  const status = document.getElementById('status');
  try {
    editor = ace.edit('editor');
    editor.setTheme('ace/theme/chrome');
    editor.session.setMode('ace/mode/python');
    editor.setShowPrintMargin(false);
    const source = codeSource(new URLSearchParams(location.search));
    status.textContent = 'Loading starter code...';
    starterCode = await loadStarter(source);
    storageKey = makeStorageKey(source);
    const saved = loadSaved();
    editor.setValue(saved !== null ? saved : starterCode, -1);
    editor.session.on('change', scheduleSave);
    window.addEventListener('pagehide', saveNow);
    document.getElementById('reset-btn').disabled = false;
    editor.commands.addCommand({
      name: 'runCode',
      bindKey: {win: 'Ctrl-Enter', mac: 'Command-Enter'},
      exec: runPython
    });
  } catch (error) {
    status.textContent = 'Could not load starter code: ' + runtimeMessage(error);
    document.getElementById('run-btn').textContent = 'Starter code unavailable';
    return;
  }
  try {
    status.textContent = 'Initializing Pyodide WebAssembly runtime...';
    pyodide = await loadPyodide();
    document.getElementById('run-btn').disabled = false;
    document.getElementById('run-btn').textContent = 'Run Code (Ctrl+Enter)';
    status.textContent = 'Pyodide Ready';
  } catch (error) {
    status.textContent = 'Failed to load WebAssembly: ' + runtimeMessage(error);
    console.error(error);
  }
}

const STUDENT_RUNNER = `
import sys, io, time, builtins, traceback, json, linecache
from js import prompt as js_prompt

class RunTimeout(BaseException):
    pass

deadline = [0.0]

def make_tracer(limit):
    deadline[0] = time.time() + limit
    def tracer(frame, event, arg):
        if time.time() > deadline[0]:
            raise RunTimeout(f'Your code was stopped after {limit} seconds. Is there an infinite loop?')
        if frame.f_code.co_filename == '<user_code>':
            return tracer
        return None
    return tracer

def student_input(message=''):
    message = str(message)
    started = time.time()
    reply = js_prompt(message or 'Python is asking for input:')
    deadline[0] += time.time() - started
    if reply is None:
        raise KeyboardInterrupt('Input cancelled')
    print(message + reply)
    return reply

original_input = builtins.input
old_stdout, old_stderr = sys.stdout, sys.stderr
sys.stdout = sys.stderr = stdout_buffer = io.StringIO()
builtins.input = student_input
failed = False
# Let tracebacks show the student's actual source line and caret indicators.
linecache.cache['<user_code>'] = (len(user_code), None, user_code.splitlines(True), '<user_code>')

try:
    sys.settrace(make_tracer(run_limit))
    exec(compile(user_code, '<user_code>', 'exec'), {'__name__': '__main__'})
except BaseException as error:
    sys.settrace(None)
    failed = True
    # Skip the exec wrapper, retaining student frames and useful library frames.
    # Returning text means no PythonError crosses into JavaScript with WASM noise.
    details = traceback.TracebackException.from_exception(error)
    def hide_runner_frames(details):
        details.stack = traceback.StackSummary.from_list(
            frame for frame in details.stack if frame.filename != '<exec>'
        )
        if details.__cause__ is not None:
            hide_runner_frames(details.__cause__)
        if details.__context__ is not None:
            hide_runner_frames(details.__context__)
        for nested in getattr(details, 'exceptions', None) or []:
            hide_runner_frames(nested)
    hide_runner_frames(details)
    print(''.join(details.format()), end='', file=stdout_buffer)
finally:
    sys.settrace(None)
    builtins.input = original_input
    sys.stdout, sys.stderr = old_stdout, old_stderr

json.dumps({'output': stdout_buffer.getvalue(), 'failed': failed})
`;

async function runPython() {
  const status = document.getElementById('status');
  const button = document.getElementById('run-btn');
  if (!pyodide) {
    status.textContent = 'Pyodide is not ready yet.';
    return;
  }
  if (running) return;
  running = true;
  button.disabled = true;
  runCount++;
  saveNow();
  const code = editor.getValue();
  try {
    status.textContent = 'Checking libraries (first use can take a while)...';
    await pyodide.loadPackagesFromImports(code);
    status.textContent = 'Running...';
    pyodide.globals.set('user_code', code);
    pyodide.globals.set('run_limit', RUN_TIMEOUT_SECONDS);
    const result = JSON.parse(await pyodide.runPythonAsync(STUDENT_RUNNER));
    appendRun(result.output || '(Code executed with no output)', result.failed);
  } catch (error) {
    appendRun('Error:\n' + runtimeMessage(error), true);
  } finally {
    running = false;
    button.disabled = false;
    status.textContent = 'Pyodide Ready';
  }
}

window.addEventListener('load', init);
