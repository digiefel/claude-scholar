# Branch Management Strategies

## Branch Types

| Branch Type | Naming Convention | Description | Lifecycle |
|:-----------|:-----------------|:------------|:----------|
| master | `master` | Main branch, always in releasable state | Permanent |
| develop | `develop` | Development branch, integrates latest development code | Permanent |
| feature | `feature/feature-name` | Feature branch | Delete after development is complete |
| bugfix | `bugfix/issue-description` | Bug fix branch | Delete after fix is complete |
| hotfix | `hotfix/issue-description` | Emergency fix branch | Delete after fix is complete |
| release | `release/version-number` | Release branch | Delete after release is complete |

## Branch Naming Conventions

### Feature Branches

```
feature/user-management          # user management feature
feature/123-add-export          # feature linked to an issue
```

### Bug Fix Branches

```
bugfix/login-error              # login error fix
bugfix/456-fix-timeout          # fix linked to an issue
```

### Emergency Fix Branches

```
hotfix/security-vulnerability   # security vulnerability fix
hotfix/v1.0.1                   # version number fix
```

### Release Branches

```
release/v1.0.0                  # version release
release/v2.0.0-beta.1           # pre-release version
```

## Branch Protection Rules

### master branch

- Direct push prohibited
- Must merge via Pull Request
- Must pass CI checks
- Must be reviewed by at least one person

### develop branch

- Direct push restricted
- Recommended to merge via Pull Request
- Must pass CI checks

## Branch Operation Commands

### Create Feature Branch

```bash
git checkout develop
git pull origin develop
git checkout -b feature/user-management
```

### Create Bug Fix Branch

```bash
git checkout develop
git pull origin develop
git checkout -b bugfix/login-error
```

### Create Emergency Fix Branch (from master)

```bash
git checkout master
git pull origin master
git checkout -b hotfix/security-fix
```

### Delete Branch

```bash
git branch -d feature/user-management      # delete local branch
git push origin -d feature/user-management # delete remote branch
```

## Detailed Workflows

### Daily Development Workflow

```bash
# 1. Sync latest code
git checkout develop
git pull origin develop

# 2. Create feature branch
git checkout -b feature/user-management

# 3. Develop and commit
git add .
git commit -m "feat(user): add user list page"

# 4. Push to remote
git push -u origin feature/user-management

# 5. Create Pull Request and request Code Review

# 6. Merge to develop (via PR)

# 7. Delete feature branch
git branch -d feature/user-management
git push origin -d feature/user-management
```

### Emergency Fix Workflow

```bash
# 1. Create fix branch from master
git checkout master
git pull origin master
git checkout -b hotfix/critical-bug

# 2. Fix and commit
git add .
git commit -m "fix(auth): fix authentication bypass vulnerability"

# 3. Merge to master
git checkout master
git merge --no-ff hotfix/critical-bug
git tag -a v1.0.1 -m "hotfix: fix authentication bypass vulnerability"
git push origin master --tags

# 4. Sync to develop
git checkout develop
git merge --no-ff hotfix/critical-bug
git push origin develop

# 5. Delete fix branch
git branch -d hotfix/critical-bug
```

### Version Release Workflow

```bash
# 1. Create release branch
git checkout develop
git checkout -b release/v1.0.0

# 2. Update version number and documentation
# Modify package.json version
# Update CHANGELOG.md

# 3. Commit version update
git add .
git commit -m "chore(release): prepare for v1.0.0 release"

# 4. Merge to master
git checkout master
git merge --no-ff release/v1.0.0
git tag -a v1.0.0 -m "release: v1.0.0 official release"
git push origin master --tags

# 5. Sync to develop
git checkout develop
git merge --no-ff release/v1.0.0
git push origin develop

# 6. Delete release branch
git branch -d release/v1.0.0
```
