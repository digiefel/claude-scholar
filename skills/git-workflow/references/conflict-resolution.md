# Conflict Resolution

## Identifying Conflicts

When Git cannot automatically merge, it marks conflicts:

```
<<<<<<< HEAD
// current branch code
const name = 'Alice'
=======
// code from the branch being merged
const name = 'Bob'
>>>>>>> feature/user-management
```

## Steps to Resolve Conflicts

### 1. View Conflicted Files

```bash
git status
```

### 2. Manually Edit Files to Resolve Conflicts

Open the conflicted file, find the conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`), and manually edit to select the content to keep or merge both.

### 3. Mark as Resolved

```bash
git add <file>
```

### 4. Complete the Merge

```bash
# For merge conflicts
git commit

# For rebase conflicts
git rebase --continue
```

## Conflict Resolution Strategies

### Keep Current Branch Version

```bash
git checkout --ours <file>
git add <file>
```

### Keep Incoming Branch Version

```bash
git checkout --theirs <file>
git add <file>
```

### Abort Merge

```bash
# Abort merge
git merge --abort

# Abort rebase
git rebase --abort
```

## Best Practices for Preventing Conflicts

1. **Sync code promptly** - Pull latest code before starting work each day
2. **Small commits** - Commit small changes frequently
3. **Modular features** - Implement different features in different files
4. **Communication** - Avoid multiple people modifying the same file simultaneously

## Common Conflict Scenarios

### Scenario 1: Same file, different locations modified

Git can usually auto-merge this case without manual intervention.

### Scenario 2: Same line, different modifications

Need to manually decide which version to keep or how to merge both.

### Scenario 3: File rename

Git can usually detect this intelligently, but if one branch renames a file while another modifies its content, manual handling may be needed.

### Scenario 4: Binary file conflict

For binary files like images and PDFs, decide which version to keep:

```bash
# Keep current branch version
git checkout --ours image.png

# Or keep incoming branch version
git checkout --theirs image.png
```

## Conflict Resolution Tools

### Using merge tool

```bash
# Configure merge tool
git config --global merge.tool vimdiff
git config --global mergetool.prompt false

# Use merge tool
git mergetool
```

### Using diff tool

```bash
# View detailed differences
git diff --ours
git diff --theirs
git diff --base
```

## Rebase Conflict Handling

Conflicts during rebase appear one commit at a time; handle them as:

```bash
git rebase develop
# conflict 1 -> resolve -> git add -> git rebase --continue
# conflict 2 -> resolve -> git add -> git rebase --continue
# ...
# until complete
```

To skip a step:

```bash
git rebase --skip
```

To abort entirely:

```bash
git rebase --abort
```
