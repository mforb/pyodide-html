# pyodide-html
Class HTML page for running Pyodide exercises and linking from Moodle

## Linkable runner

`runner_link.html` uses the same editor and controls as the existing runners:
Run (Ctrl+Enter / Command+Enter), Reset code, autosave, run history, Clear console,
package loading, `input()` prompts, a five-second Python tracing limit, and output
truncation. With no parameters it starts with `# Write your Python code here`.
Keep `runner_link.js` beside the HTML file when publishing.

Python errors show the student's traceback, source lines and final error message,
without the runner's Python frames or the trailing Pyodide JavaScript/WASM stack.
Output printed before an error and writes to stderr are retained.

### Starter-code links

These work as an iframe `src` or a normal anchor `href`:

```html
<a href="https://mforb.github.io/pyodide-html/runner_link.html?file=exercises%2Fclass2%2F01_measurements.py">Open Task 1</a>

<iframe src="https://mforb.github.io/pyodide-html/runner_link.html?file=exercises%2Fclass2%2F01_measurements.py" width="100%" height="600" title="Python Task 1"></iframe>

<a href="https://mforb.github.io/pyodide-html/runner_link.html?code=print%28%22Hello%22%29">Open a text starter</a>
```

- `file`: relative or absolute URL of a raw UTF-8 Python/text file (`.py` or
  `.txt`). Relative paths resolve beside the runner. Files on other hosts must
  allow cross-origin fetching; use GitHub Pages or a raw-file URL, not a GitHub
  file-view page. HTTP failures are displayed instead of being loaded as code.
- `code`: literal Python text, URL-encoded. `text` is an alias.
- `code64`: explicitly base64-encoded UTF-8 Python text. Unlike the original
  runner's automatic guess, plain `code=pass` really loads `pass`.
- If more than one is supplied, precedence is `code`, `text`, `code64`, `file`.

Use `URLSearchParams` to correctly encode spaces, newlines, `+`, `#`, `&` and
Unicode when constructing a link:

```javascript
const url = new URL('https://mforb.github.io/pyodide-html/runner_link.html');
url.searchParams.set('code', 'name = "Camp A"\nprint(name)');
const href = url.href;
```

Each starter has its own locally saved draft. Revisiting the same exercise
restores that draft; **Reset code** restores the original URL-supplied starter.
No code runs automatically when a link opens.

## Class 2 Moodle blocks

`moodle_class2.html` stores **13 copyable Moodle HTML blocks**, using the existing
Python-logo heading, `section`/`number` numbering, difficulty stars and 600px
runner iframe format. `START TASK` / `END TASK` comments mark each complete block.

Copy one block into each Moodle text/HTML area. The optional numbering script at
the top is copied **once**, only if your Moodle section does not already set
`section` and `number`. Its default section number is **8** (following Class 1's
7.x examples); change it to match your Moodle course. Do not copy the whole file
into every individual task, as that would reset the numbering.

| Block | Exercise |
| --- | --- |
| 1 | List indexing and slicing |
| 2 | String indexing and slicing |
| 3 | Editing lists with append, insert, pop and remove |
| 4 | Count, mean, minimum, maximum and range |
| 5 | Tuple coordinates and unpacking |
| 6 | Dictionary site record and formatted summary |
| 7 | Pass/fail with if / else and boundary tests |
| 8 | Three wind bands with if / elif / else |
| 9 | Sensor alarm combining and / or and dictionary lookups |
| 10 | Three deliberate bugs: SyntaxError, IndexError, KeyError |
| 11 | Everyone's sensor-report checkpoint, with three test cases |
| 12 | Optional known-sites membership and classification extension |
| 13 | Optional set uniqueness, membership, add/discard and sorting |

Tasks 1–6 fit the first self-paced block, and 7–11 the second; 12–13 are optional
extensions. Each task includes
expected outputs, room to experiment, and a formal reflection question with an
explanatory answer. No loops,
comprehensions or NumPy are required. The matching incomplete starter files are
under `exercises/class2/`; Task 10 intentionally contains a syntax error.

Publish `runner_link.html`, `runner_link.js`, `moodle_class2.html` and
`exercises/class2/` to the GitHub Pages branch before using the Moodle links.

## Class 3 Moodle blocks

`moodle_class3.html` contains **12 copyable Moodle HTML blocks** for loops and
algorithms, with the same heading, numbering, difficulty stars, reflection
answers and 600px runner iframes as Class 2. The optional numbering header
defaults to section **9**; copy it once only and adjust it to your Moodle course.

Each task begins with **flow chart → hand trace → plain-language steps → Python**.
The first self-paced block uses Tasks 1–5; the second uses Tasks 6–10, followed
by optional extensions 11–12. Use loops for the calculations; no user-defined
functions, comprehensions or NumPy are required.

| Block | Exercise |
| --- | --- |
| 1 | Square root by repeated guessing with a `while` loop |
| 2 | Peak reading with a `for` loop and running maximum |
| 3 | Load/deflection table with `range()` and an inclusive last load |
| 4 | Count, mean, minimum and maximum using accumulators |
| 5 | Count readings strictly above a limit, including boundary tests |
| 6 | Loop over dictionary site records and check each site's tolerance |
| 7 | Skip missing (`None`) readings with `continue` |
| 8 | Stop at the first overload with `break` |
| 9 | Fix an off-by-one endpoint and a missing `while` update |
| 10 | Measurement-log checkpoint with missing, empty and negative data |
| 11 | Optional square-root tolerance versus number of updates |
| 12 | Optional iteration limit and convergence reporting |

Incomplete starters are under `exercises/class3/`. **Task 9 deliberately contains
an infinite loop** until the missing update is fixed; the runner stops it after
five seconds. Compile checks are safe, but do not execute that starter with an
unbounded local Python process. The square-root tasks state their positive-input
assumptions and use an absolute squared-value residual.

Publish `moodle_class3.html` and `exercises/class3/` alongside `runner_link.html`
and `runner_link.js` on the GitHub Pages branch before using the new links.

## Class 4 Moodle blocks

`moodle_class4.html` contains **12 copyable Moodle HTML blocks** for functions and
scientific Python. It uses the same heading, numbering, reflection answers and
600px runner iframe format as Classes 2 and 3. The optional numbering header
defaults to section **10**.

Use **inputs → calculation → returned result**, then predict, run and compare.
Tasks 1–8 are the core lesson; **Tasks 9–12 are optional**. The matching incomplete
starters are under `exercises/class4/`.

| Block | Exercise |
| --- | --- |
| 1 | Return a Celsius temperature from a Fahrenheit input |
| 2 | Return a 2D distance using Pythagoras |
| 3 | Signal travel distance with a default speed and keyword arguments |
| 4 | Check the distance function, including zero and negative differences |
| 5 | Sort toy satellites by supplied azimuth, then calculate array distances |
| 6 | Select distances at or below a limit with a Boolean mask |
| 7 | Label a step plot and estimate a chip duration |
| 8 | Required checkpoint: reusable distance-array filter with checks |
| 9 | Optional 2D positioning: compare three candidate locations |
| 10 | Optional ground-projected speed at different circular-orbit heights |
| 11 | Optional seven-chip code matching against a shifted register |
| 12 | Optional two-component velocity update towards circular-orbit speed |

The small 2D coordinates and slow chip timing are teaching models. Orbit speed
uses a spherical, non-rotating Earth; the velocity update is an impulse
approximation, not a full orbital transfer simulation. The first work block uses
Tasks 1–4; the second uses Tasks 5–8 before any optional task.

Task 2 now links to `02_distance_function.py` and Task 7 to `07_chip_plot.py`.
Replace the existing Class 4 Moodle blocks when publishing this revision so their
instructions and iframe links match the new starters.

Publish `moodle_class4.html` and `exercises/class4/` with the runner files before
using the links in Moodle. The link runner includes a plot target so a student's
`plt.show()` output is visible below the console.

## Verification

Material block/link/compile checks can run without browser dependencies:

```bash
python -c "import runpy; runpy.run_path('tests/test_runner_browser.py')['check_materials'](); print('PASS: Class 2, Class 3 and Class 4 materials')"
```

Browser regression tests use the real CDN-hosted Ace and Pyodide runtime:

```bash
python -m pip install playwright
python -m playwright install chromium
python tests/test_runner_browser.py
```

The test starts a local HTTP server, checks URL loading, saving/resetting,
errors, input, timeout and the supplied exercise starters and links. Chromium
may also require the platform dependencies installed by
`python -m playwright install-deps chromium`.
