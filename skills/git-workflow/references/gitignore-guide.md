# .gitignore Standards

## Basic Rules

```
# Empty line: matches no files
# Comment: starts with #
# Directory: ends with /
# Negation: starts with ! to un-ignore
# Root: starts with / to mean project root

*.log               # ignore all .log files
node_modules/       # ignore node_modules directory
/temp/              # ignore temp directory at root
**/.env             # ignore .env files in all directories
!.gitkeep           # do not ignore .gitkeep files
```

## General .gitignore

```
# ============================================
# Dependency directories
# ============================================
node_modules/
vendor/

# ============================================
# Build artifacts
# ============================================
dist/
build/
target/

# ============================================
# Editors and IDEs
# ============================================
.idea/
.vscode/
*.sw?

# ============================================
# Environment configuration
# ============================================
.env
.env.local
.env.*.local

# ============================================
# Log files
# ============================================
logs/
*.log
npm-debug.log*

# ============================================
# System files
# ============================================
.DS_Store
Thumbs.db

# ============================================
# Cache files
# ============================================
.cache/
.eslintcache
.stylelintcache
```

## Project-Specific Configuration

### Frontend/Documentation Projects

```
# VitePress
docs/.vitepress/dist
docs/.vitepress/cache

# Node.js
package-lock.json
yarn.lock
pnpm-lock.yaml
```

### Backend Projects

```
# Maven
target/
pom.xml.tag
*.jar
!**/src/main/**/target/

# Sensitive configuration
application-local.yml
application-dev.yml
```

### Python Projects

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/
.pytest_cache/

# Jupyter Notebook
.ipynb_checkpoints

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# pytype
.pytype/
```

### Go Projects

```
# Binaries for programs and plugins
*.exe
*.exe~
*.dll
*.so
*.dylib

# Test binary, built with `go test -c`
*.test

# Output of the go coverage tool
*.out

# Dependency directories
vendor/

# Go workspace file
go.work
```

### Rust Projects

```
# Rust
/target/
**/*.rs.bk
*.pdb
Cargo.lock
```

## .gitignore Tips

### Ignore files but keep directory

```
logs/*
!logs/.gitkeep
```

### Check ignore rules

```bash
git check-ignore -v filename
```

### Clean up committed ignored files

```bash
git rm --cached filename
git commit -m "chore: remove files that should not be committed"
```

### Debug .gitignore

```bash
# Check if a file is ignored and which rule matches
git check-ignore -v path/to/file

# List all ignored files
git ls-files --others --ignored --exclude-standard
```

## Common Patterns

### Ignore specific files

```
# Ignore specific files
config/local.json
secrets.yaml
```

### Ignore by type

```
# Ignore all .log files
*.log

# Ignore all temporary files
*.tmp
*.temp
```

### Ignore directories

```
# Ignore all node_modules directories
node_modules/

# Ignore build directory at root
/build/

# Ignore build directory anywhere
**/build/
```

### Negation rules

```
# Ignore all .a files
*.a

# But not lib.a
!lib.a

# Ignore all TODO files
TODO*

# But not TODO.md
!TODO.md
```

### Wildcards

```
# * matches any characters
*.log

# ** matches any directory
**/temp/

# ? matches a single character
file?.txt

# [] matches any character in brackets
file[0-9].txt
```

## .gitignore Priority

1. Files specified on the command line (e.g., `git add -f`)
2. `.git/info/exclude` (local exclusion rules)
3. `.gitignore` (project-level, committed to repository)
4. `~/.gitignore_global` (global level)

### Local Exclusion Rules

For local ignore rules you don't want to commit to the repository:

```bash
# Edit global ignore file
git config --global core.excludesfile ~/.gitignore_global

# Or use .git/info/exclude (current repository only)
echo "secrets.yaml" >> .git/info/exclude
```
