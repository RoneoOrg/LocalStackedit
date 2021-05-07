This script aims to bodge the limit of [StackEdit.io](https://stackedit.io/) which cannot access local files.
It opens in Brave (as an automated browser - Selenium) the file provided as first argument.

**Usage**:
`python LocalStackedit.py <filepath>`

or (Linux only on a Python virtual env)
`StackEdit.sh <filepath>`

TODO: 
- Save file as markdown and html on `ctrl + s`
- no limit of instances (for now, it's limited to one)

Depends on Brave-browser (version `90.1.24.82`)

For future or ulterior versions of Brave, the proper driver can be downloaded on [Chrome's official website](https://chromedriver.storage.googleapis.com/index.html).

## Installation

**Python**

Python version 3.6 or above

_On Linux/Mac:_
```bash
python3 --version
```

_On Windows_:
```bash
python --version
```

**Clone the repository**

Git is required
```bash
git --version
```

Clone it
```bash
git clone <++> 
```

**Dependencies**

Install dependencies:

_On Linux/Mac:_
```bash
pip3 install -r requirements.txt
```

_On Windows_:
```bash
pip install -r requirements.txt
```
**Create a virtual environnement**
Optional

`python -m venv venv`

Activate it
`source ./venv/bin/activate`

**Executable**

Allows execution of entry point (not needed for Windows)
```bash
chmod +x <++>
```

**Bash shortcut**

If you want to access it directly from the terminal (Linux and MacOsX) with the command `<++>`:

```bash
INSTALL_DIR=""
printf "# <++>\nalias <++>='${INSTALL_DIR}/<++>.py'" >> ~/.bash_aliases
```

**Update**

```bash
git pull
```

## License and EULA
Unmodified [MIT license](https://opensource.org/licenses/MIT)

See `LICENSE.md`

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
