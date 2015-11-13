# sitegeist/git-hooks

> Git-Hooks which are supporting our workflow and QA process.

## Installation
``` bash
git clone https://github.com/sitegeist/git-hooks.git $HOME/.sitegeist-hooks && cd $HOME/.sitegeist-hooks && ./install && cd
```

## CLI
Change into your package directory which contains your local `.git/` repository and run:
``` bash
hook
```
Afterwards all available hooks should be installed in your local repository.

#### Arguments
| Argument      | Description                            |
| ------------- | -------------------------------------- |
| `--help`      | Prints the usage guidelines.           |
| `self-update` | Updates the hooks.                     |

#### Why bother install them globally?
These git-hooks are conventional hooks, not project specific ones. Installing them globally reduces the amount of time you need to invest once a bug has been found in one of the hooks. Just run `self-update` once and the hooks are updated everywhere since they all point to the global instance.

## Available git-hooks
#### pre-commit
Lints all `.js` files and aborts the commit if errors are found.

#### post-merge
If the `package.json`, `npm-shrinkwrap.json`, `composer.json` or the `composer.lock` has been changed in the upstream,
this hook will automatically run either `npm update && npm prune` or `composer install` so your local dependencies match the current checked out HEAD.

#### prepare-commit-msg
Evaluates the commit message against the [TYPO3 Commit guidelines](#guidelines).

In case your current branch is a feature branch, the issue number of the branch gets parsed
and automatically appended to the commit message.

For example, if your current branch is called `task/29381/taskDescription`, and you commit
``` bash
git commit -m "[TASK] Add person select to the quick booking widget"
```

The final commit message in your history will be
```
[TASK] Add person select to the quick booking widget

refs #29381
```

## <a name="guidelines"></a> Commit message guidelines
In short, a commit message must be prefixed with either `[FEATURE]`, `[TASK]`, `[BUGFIX]`, `[DOCS]` or `[CLEANUP]`. F.e:
``` bash
git commit -m "[FEATURE] Add person select to the quick booking widget"
```

Additionally, for breaking changes, you should specify the prefix `[!!!]`, and for not finished work, the `[WIP]` prefix.
Note that both of them should be immediately followed by one of the prefixes above. F.e.:
``` bash
git commit -m "[!!!][TASK] Change the person argument of the booking API for consistency"
```

For an overview of the commit message guidelines, please visit the official [TYPO3 commit guidelines page](https://wiki.typo3.org/CommitMessage_Format_(Git)#Commit_Message_rules_for_TYPO3_CMS).

## License
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
