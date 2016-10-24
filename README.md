# sitegeist/git-hooks [![Build Status](https://travis-ci.org/sitegeist/git-hooks.svg)](https://travis-ci.org/sitegeist/git-hooks)

> Git-Hooks which are supporting our workflow and QA process.

## Installation
``` bash
git clone https://github.com/sitegeist/git-hooks.git $HOME/.sitegeist-hooks && cd $HOME/.sitegeist-hooks && ./install && cd
```

## CLI
`cd` into your target directory which contains your local `.git/` repository and run hook.

``` bash
hook install
```
Afterwards all available hooks should be installed in your local repository.

#### Commands
| Command            | Description                                                     |
| ------------------ | --------------------------------------------------------------- |
| `hook`             | Prints the usage guidelines.                                    |
| `hook install`     | Installs all hooks in your current working directory.           |
| `hook self-update` | Updates all installed hooks which you've installed via the CLI. |
| `hook help`        | Prints the usage guidelines.                                    |
| `hook help:hooks`  | Prints a list of all installed hooks.                           |

#### Why bother install them globally?
These git-hooks are conventional hooks, not project specific ones. Installing them globally reduces the amount of time you need to invest once a new feature has been released or a bug has been found in one of the hooks.

In that case, just run `self-update` once and all hooks which you've installed via the CLI are updated. The CLI and the corresponding hooks will also update itself automatically every 30 days on every CLI run. This prevents the hooks from being in a obsolete state.

## Globally installed hooks
| Name                 | Description                                                         |
| -------------------- | ------------------------------------------------------------------- |
| `pre-commit`         | Lints changed files & creates a npm-shrinkwrap if necessary.        |
| `post-merge`         | Updates the local dependencies if necessary.                        |
| `commit-msg` | Reviews the commit message against the [guidelines](#guidelines) and append ticket number if available in branch(abc/<#branchnumber>/def).   |

#### pre-commit
> Lints changed files & creates a npm-shrinkwrap if necessary.

We encourage the use of static analysis tools. To enforce a certain code style, and to prevent nasty code from shipping into production, we recommend to lint your source files before committing them.
The `pre-commit` hook will automatically do this for you.
As of now, we only lint `.js` files via [xo](https://github.com/sindresorhus/xo).

The pre-commit hook will execute `npm run lint`, if it's return value is 0 it will continue otherwise it throws an error message.

The pre-commit hook also checks if a `package.json` file is in your changeset, and will automatically create and commit a `npm-shrinkwrap.json` file for you. *Note:* This functionality is kind of useless if you are using `> npm@3.0.0` - [Related issue](https://github.com/npm/npm/issues/5083).

#### post-merge
> Updates the local dependencies if necessary.

In some cases, after you've checked out a branch, you will be greeted
with errors while starting up the project because the dependency versions have been changed.
The `post-merge` hook solves this problem for `git checkout`, `git pull` as well as `git merge`.

If the `package.json` or `composer.json` have been changed in the upstream, it will automatically run either
`npm prune && npm install` or `composer install` so your local dependencies match the current checked out HEAD.

#### commit-msg
> Reviews the commit message against the [guidelines](#guidelines).

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

## Configuration
You can configure & extend the existing hooks by creating a `.hook.yml` in your git repositories root directory.
All paths which where specified in the `.hook.yml` are relative to the git repositories root directory.
If you specify a regex for your commit messages the global commit guidelines are disabled

An example `.hook.yml`.
```yaml
#
# Custom location for package.json. For example:
# only necessary when the package.json is not placed in the root directory of the project
#
path:
  packageJSON: Web/typo3conf/ext/sms_boilerplate/

#
# Regex for commit message guidelines
# Otherwise the global ones will be used
#
commitmsg:
  regex: ^t

#
# Paths to executable shell files which are extending the global hooks.
# For example:
#
extend:
  pre_commit: Build/hooks/pre-commit
  post_merge: Build/hooks/post-merge
  commit_msg: Build/hooks/commit-msg
```

## Extending the global hooks
The hook extension is immediately executed after the global hook,
arguments which where passed to the global hook via git are propagated to your hook extension.

Please note that all hook extensions need to be executable (`chmod +x path/to/hook/extension`) and
we expect the script to exit with code 0, otherwise the current git process will abort.

TL;DR: A hook extension acts like a standalone hook which is traditionally placed in the `.git/hooks/` directory.

## Misc. configurations
### <a name="packagejsonLocation"></a> packe.json location
As of now, you can also specify a custom location for the `package.json`.
The `pre-commit` hook expects the following structure in your `.hook.yml`.

Please note that the path is relative to the local git repository and is not a direct pointer to the `package.json`.
Instead we point to the directory which holds the `package.json`.

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
