# sitegeist/git-hooks

> Git-Hooks which are supporting our workflow and QA process.


| Prefix               | Description                                                                                        |
| -------------------- | -------------------------------------------------------------------------------------------------- |
| `pre-commit`         | Lints all `.js` files and aborts the commit if errors are found.                                   |
| `post-merge`         | If a meta data file for `npm` or `composer` has changed, run update commands for the dependencies. |
| `prepare-commit-msg` | Evaluates the commit message against the [TYPO3 Commit guidelines]().                                  |


## Commit message guidelines
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
