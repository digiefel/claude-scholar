#!/bin/bash
# Git workflow common command examples

# ============================================
# Daily development workflow
# ============================================

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

# 5. Sync upstream updates to feature branch
git fetch origin develop
git rebase origin/develop

# 6. Merge to develop (via PR or directly)
git checkout develop
git merge --no-ff feature/user-management
git push origin develop

# 7. Delete feature branch
git branch -d feature/user-management
git push origin -d feature/user-management

# ============================================
# Emergency fix workflow
# ============================================

# 1. Create fix branch from master
git checkout master
git pull origin master
git checkout -b hotfix/security-fix

# 2. Fix and commit
git add .
git commit -m "fix(auth): fix authentication bypass vulnerability"

# 3. Merge to master
git checkout master
git merge --no-ff hotfix/security-fix
git tag -a v1.0.1 -m "hotfix: fix authentication bypass vulnerability"
git push origin master --tags

# 4. Sync to develop
git checkout develop
git merge --no-ff hotfix/security-fix
git push origin develop

# 5. Delete fix branch
git branch -d hotfix/security-fix

# ============================================
# Version release workflow
# ============================================

# 1. Create release branch
git checkout develop
git checkout -b release/v1.0.0

# 2. Update version number and documentation
# Manually edit package.json, CHANGELOG.md, etc.

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

# ============================================
# Conflict handling
# ============================================

# Merge conflict handling
git merge feature/xxx
# Edit conflicted files...
git add <file>
git commit

# Rebase conflict handling
git rebase develop
# Edit conflicted files...
git add <file>
git rebase --continue

# Abort merge
git merge --abort
git rebase --abort

# ============================================
# Common utility commands
# ============================================

# Check status
git status

# View log
git log --oneline --graph --all

# View branches
git branch -a

# Stash work
git stash save "work in progress"
git stash list
git stash pop

# View file changes
git diff
git diff --staged
git log -p -- <file>
