# Git Advanced Usage

## Tag Management

### Version Numbering Convention

Use **Semantic Versioning**:

```
MAJOR.MINOR.PATCH[-PRERELEASE]
```

| Version Change | Description | Example |
|:--------------|:------------|:--------|
| Major version | Incompatible API changes | `v1.0.0 → v2.0.0` |
| Minor version | Backward-compatible feature additions | `v1.0.0 → v1.1.0` |
| Patch version | Backward-compatible bug fixes | `v1.0.0 → v1.0.1` |

### Pre-release Identifiers

- `alpha` - Alpha version
- `beta` - Beta version
- `rc` - Release candidate

```
v1.0.0-alpha.1    # First alpha version
v1.0.0-beta.1     # First beta version
v1.0.0-rc.1       # First release candidate
v1.0.0            # Official release
```

### Tag Operations

#### Create Annotated Tag (Recommended)

```bash
git tag -a v1.0.0 -m "release: v1.0.0 official release

Major updates:
- Added user management module
- Added payment feature
- Optimized query performance"
```

#### Push Tags

```bash
# Push a single tag
git push origin v1.0.0

# Push all tags
git push origin --tags
```

#### View Tags

```bash
git tag
git tag -l "v1.*"
git show v1.0.0
```

#### Delete Tags

```bash
# Delete local tag
git tag -d v1.0.0

# Delete remote tag
git push origin :refs/tags/v1.0.0
```

## Git Performance Optimization

### Large Repository Optimization

```bash
# Shallow clone (get only recent commits)
git clone --depth 1 https://github.com/repo/project.git

# Partial clone (fetch on demand)
git clone --filter=blob:none https://github.com/repo/project.git

# Sparse checkout (check out only needed directories)
git clone --filter=blob:none --sparse https://github.com/repo/project.git
cd project
git sparse-checkout init --cone
git sparse-checkout set src/frontend
```

### Repository Cleanup

```bash
# Check repository size
git count-objects -vH

# Clean up unused objects
git gc --aggressive --prune=now

# Clean up remote-deleted branch references
git remote prune origin

# Clean up locally merged branches
git branch --merged master | grep -v "\\*\\|master\\|develop" | xargs -n 1 git branch -d
```

### Improve Operation Speed

```bash
# Enable file system cache
git config --global core.fscache true

# Enable parallel fetching
git config --global fetch.parallel 4

# Enable untracked file cache
git config --global core.untrackedCache true
```

## Git Security Standards

### Sensitive Information Protection

```bash
# Check historical commits for sensitive information
git log -p | grep -E "(password|secret|api_key)"

# Remove sensitive files from history
git filter-branch --force --index-filter \
  'git rm --cached --ignore-unmatch config/secrets.yml' \
  --prune-empty --tag-name-filter cat -- --all

# Use git-secrets to prevent committing sensitive information
git secrets --install
git secrets --register-aws
```

### Signature Verification

```bash
# Configure GPG signature
git config --global user.signingkey YOUR_KEY_ID
git config --global commit.gpgsign true

# Create signed commit
git commit -S -m "feat: signed commit"

# Verify signature
git log --show-signature
```

### Repository Permission Control

| Rule | master | develop | feature/* |
|:-----|:-------|:--------|:----------|
| No force push | Yes | Yes | No |
| No delete | Yes | Yes | No |
| Code Review required | Yes | Yes | No |
| CI must pass | Yes | Yes | No |
| Signed commits required | Yes | No | No |

## Submodule Management

### Add Submodule

```bash
git submodule add https://github.com/user/repo.git libs/repo

# Clone project with submodules
git clone --recurse-submodules https://github.com/user/project.git

# Initialize submodules for existing project
git submodule init
git submodule update
```

### Update Submodule

```bash
# Update a single submodule
cd libs/repo
git pull origin main

# Update all submodules
git submodule update --remote

# Commit submodule update
cd ..
git add libs/repo
git commit -m "chore: update submodule version"
```

### Delete Submodule

```bash
# Remove submodule entry
git submodule deinit -f libs/repo

# Remove cache in .git/modules
rm -rf .git/modules/libs/repo

# Remove submodule directory
git rm -f libs/repo
```

## Common Problem Solving

### 1. Amend Last Commit

```bash
# Amend commit content (not yet pushed)
git add forgotten-file.ts
git commit --amend --no-edit

# Amend commit message
git commit --amend -m "new commit message"

# Roll back last commit, keep changes
git reset --soft HEAD~1
```

### 2. Push Rejected

```bash
# Pull then push
git pull origin master
git push origin master

# Use rebase for clean history
git pull --rebase origin master
git push origin master
```

### 3. Roll Back to Previous Version

```bash
# Reset to specified commit (discards subsequent commits)
git reset --hard abc123

# Create reverse commit (recommended, preserves history)
git revert abc123
```

### 4. Recover Accidentally Deleted Branch

```bash
# View operation history
git reflog

# Restore branch
git checkout -b feature/xxx def456
```

### 5. Merge Multiple Commits

```bash
# Interactive rebase (only for unpushed commits)
git rebase -i HEAD~5

# Mark commits to merge as "squash" in the editor
```

### 6. Stash Current Work

```bash
git stash save "work in progress"
git stash list
git stash pop
git stash apply stash@{0}
```

### 7. View File Modification History

```bash
git log -- <file>             # commit history
git log -p -- <file>          # detailed content
git blame <file>              # who modified each line
```

### 8. Handle Large Files

```bash
# Use Git LFS
git lfs install
git lfs track "*.zip"
git add .gitattributes
```

## Useful Tips

### Configure Aliases

```bash
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.st status
git config --global alias.lg "log --graph --oneline --all"
```

### Beautify Logs

```bash
# Graphical history
git log --graph --oneline --all

# Search commit messages
git log --grep="user management"

# Search code changes
git log -S"function_name"
```

### Quick Operations

```bash
# Discard all uncommitted changes
git reset --hard HEAD

# Discard changes to a specific file
git checkout -- filename

# Delete untracked files
git clean -fd

# Batch delete merged branches
git branch --merged master | grep -v "\* master" | xargs -n 1 git branch -d
```

### Safe Operations

```bash
# Preview what will be pushed
git push --dry-run

# Safe force push
git push --force-with-lease

# Backup branch
git branch backup-master master
```

### Find Problem Commits

```bash
# Binary search for commit that introduced a bug
git bisect start
git bisect bad              # Mark current as broken
git bisect good v1.0.0      # Mark a known-good version
# Git auto-switches commits; mark each as good/bad after testing
git bisect reset            # End search
```

## CHANGELOG Management

### Auto-generate CHANGELOG

Use `conventional-changelog`:

```bash
# Install
pnpm install -D conventional-changelog-cli

# Generate CHANGELOG
npx conventional-changelog -p angular -i CHANGELOG.md -s
```

### CHANGELOG Format

```markdown
# Changelog

## [1.2.0] - 2024-01-15

### Added
- Added user export feature (#123)
- Added data backup module

### Fixed
- Fixed login CAPTCHA not refreshing (#456)
- Fixed list pagination anomaly

### Changed
- Optimized user query performance
- Adjusted menu permission validation logic

### Removed
- Removed deprecated API endpoints

## [1.1.0] - 2024-01-01
...
```
