# Merge Strategies

## Merge vs Rebase

| Feature | Merge | Rebase |
| :------ | :---- | :----- |
| History | Preserves full history, creates merge commit | Linear history, no merge commit |
| Use case | Public branches, preserve history | Private branches, keep history clean |
| Conflict handling | Resolve all conflicts at once | Resolve conflicts per commit |
| Recommended for | Merging into main branch | Syncing upstream code |

## Usage Guidelines

### Sync feature branch with develop: use rebase

```bash
git checkout feature/user-management
git rebase develop
```

### Merge feature branch into develop: use merge --no-ff

```bash
git checkout develop
git merge --no-ff feature/user-management
```

### Merge develop into master: use merge --no-ff

```bash
git checkout master
git merge --no-ff develop
```

### Never rebase on public branches

```bash
# Dangerous operation
git checkout develop
git rebase feature/xxx  # rewrites public history
```

## Fast-Forward vs No-Fast-Forward

### Fast-Forward merge (no merge commit)

```bash
git merge feature/xxx
```

```
# A---B---C  (master)
#          \
#           D---E  (feature)
# Result: A---B---C---D---E  (master)
```

### No-Fast-Forward merge (creates merge commit)

```bash
git merge --no-ff feature/xxx
```

```
# A---B---C---------M  (master)
#          \       /
#           D---E    (feature)
```

**Project convention**: Use `--no-ff` when merging feature branches to preserve branch history.

## Squash Merge

Squash multiple commits into one:

```bash
git checkout develop
git merge --squash feature/user-management
git commit -m "feat(user): add user management feature"
```

### Use cases

- Feature branch has too many trivial commits
- Want to keep main branch history clean
- Development process details are not needed

### Squash vs Merge --no-ff

| Strategy | Pros | Cons | Use case |
| :------- | :--- | :--- | :------- |
| merge --no-ff | Preserves full history and development process | History can be complex | Feature branches, important features |
| squash | Clean history, one commit per feature | Loses development process information | Small features, experimental features |
| rebase | Linear history, easy to understand | Rewrites history, can cause issues | Personal branches, syncing upstream |

## Advanced Rebase Usage

### Interactive Rebase

```bash
# Edit last 5 commits
git rebase -i HEAD~5
```

Available commands in the editor:
- `pick` - keep the commit
- `reword` - edit commit message
- `edit` - edit commit content
- `squash` - merge into previous commit
- `drop` - delete the commit

### Resolving conflicts during rebase

```bash
git rebase develop
# After conflict appears, edit the file to resolve
git add <file>
git rebase --continue
# To abort the rebase
git rebase --abort
```
