---
name: create_project
description: Create a new project from template with uv and Git initialization
arguments:
  - name: project_name
    description: project name
    required: true
  - name: path
    description: project path (default is ~/Code/)
    required: false
  - name: template_repo
    description: "GitHub template repository (format: owner/repo or full URL, default: gaoruizhang/template)"
    required: false
  - name: local
    description: use local template ~/Code/template instead of GitHub (overrides template_repo)
    required: false
---

# Create New Project

This command creates a new project based on a template with the following steps:
1. Fetch template files from GitHub or locally
2. Replace project name
3. Initialize uv project
4. Configure Git repository and branch strategy
5. Create initial tag
6. Initialize GitHub remote repository

```bash
# Parse arguments
PROJECT_NAME="{{project_name}}"
PROJECT_PATH="${path:-$HOME/Code}"
FULL_PATH="$PROJECT_PATH/$PROJECT_NAME"
TEMPLATE_REPO="{{template_repo:-gaoruizhang/template}}"
USE_LOCAL="{{local}}"
INITIAL_TAG="v0.1.0"

# Determine whether to use local or GitHub template
if [ "$USE_LOCAL" = "true" ]; then
  # local argument takes priority
  TEMPLATE_PATH="$HOME/Code/template"
  USE_LOCAL_TEMPLATE=true
else
  # Use GitHub template
  if [[ "$TEMPLATE_REPO" == https://github.com/* ]] || [[ "$TEMPLATE_REPO" == git@github.com:* ]]; then
    TEMPLATE_URL="$TEMPLATE_REPO"
  else
    # owner/repo format, convert to HTTPS URL
    TEMPLATE_URL="https://github.com/$TEMPLATE_REPO"
  fi
  USE_LOCAL_TEMPLATE=false
fi

echo "Creating new project: $PROJECT_NAME"
echo "Path: $FULL_PATH"
echo ""

# Check template source
if [ "$USE_LOCAL_TEMPLATE" = true ]; then
  if [ ! -d "$TEMPLATE_PATH" ]; then
    echo "Error: local template directory does not exist: $TEMPLATE_PATH"
    exit 1
  fi
  echo "Using local template: $TEMPLATE_PATH"
else
  echo "Using GitHub template: $TEMPLATE_URL"
fi

# Check if target directory already exists
if [ -d "$FULL_PATH" ]; then
  echo "Error: directory already exists: $FULL_PATH"
  exit 1
fi

# 1. Create project directory
echo "Creating project directory..."
mkdir -p "$FULL_PATH"

# 2. Fetch template files
echo "Fetching template files..."
if [ "$USE_LOCAL_TEMPLATE" = true ]; then
  # Local template: use rsync to copy (excluding .git, .idea, .DS_Store, etc.)
  rsync -av --exclude='.git' \
            --exclude='.idea' \
            --exclude='.DS_Store' \
            --exclude='__pycache__' \
            --exclude='*.pyc' \
            "$TEMPLATE_PATH/" "$FULL_PATH/"
else
  # GitHub template: use git clone to a temp directory, then move files
  TEMP_TEMPLATE_DIR=$(mktemp -d)
  git clone --depth 1 "$TEMPLATE_URL" "$TEMP_TEMPLATE_DIR"

  # Move files to target directory (excluding .git)
  rsync -av --exclude='.git' \
            --exclude='.idea' \
            --exclude='.DS_Store' \
            --exclude='__pycache__' \
            --exclude='*.pyc' \
            "$TEMP_TEMPLATE_DIR/" "$FULL_PATH/"

  # Clean up temp directory
  rm -rf "$TEMP_TEMPLATE_DIR"
fi

# 3. Replace project name
echo "Replacing project name..."
cd "$FULL_PATH"

# Replace first line of README.md (if it is an example title)
if [ -f "README.md" ]; then
  # Check if first line starts with #
  FIRST_LINE=$(head -n 1 README.md)
  if [[ "$FIRST_LINE" == "#"* ]]; then
    # Replace first line with project name
    echo "# $PROJECT_NAME" > README.md.new
    tail -n +2 README.md >> README.md.new
    mv README.md.new README.md
    echo "   Updated README.md title"
  fi
fi

# Replace project name in pyproject.toml (if it exists)
if [ -f "pyproject.toml" ]; then
  sed -i.bak "s/name = \".*\"/name = \"$PROJECT_NAME\"/" pyproject.toml
  rm -f pyproject.toml.bak
  echo "   Updated pyproject.toml project name"
fi

# 4. Initialize uv project
echo "Initializing uv project..."
uv init --no-readme  # README was already copied from template

# 4.5 Generate uv.lock (best practice: initial commit should include lockfile)
echo "Generating uv.lock..."
uv sync

# 5. Initialize Git repository (defaults to master branch)
echo "Initializing Git repository..."
git init

# 6. Initial commit on master
echo "Creating initial commit..."
git add .
git commit -m "chore: initialize project

Create project structure from template
- Configure project structure
- Initialize uv dependency management (including uv.lock)
- Set up Git workflow (master/develop)
- Create initial version $INITIAL_TAG"

# 7. Create initial tag (on master)
echo "Creating initial tag: $INITIAL_TAG"
git tag -a "$INITIAL_TAG" -m "release: $INITIAL_TAG initial version

Project initialization complete"

# 8. Create develop branch
echo "Creating develop branch..."
git checkout -b develop

# 9. Ask whether to create GitHub repository
echo ""
echo "Project created successfully!"
echo ""
echo "Project location: $FULL_PATH"
echo "Initial version: $INITIAL_TAG"
echo ""
echo "Next steps:"
echo "   cd $FULL_PATH"
echo ""

# Ask whether to create GitHub remote repository
read -p "Create GitHub remote repository? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
  # Check if gh CLI is installed
  if ! command -v gh &> /dev/null; then
    echo "Warning: GitHub CLI (gh) not installed, skipping remote repository creation"
    echo "   Install: brew install gh"
  else
    echo "Creating GitHub remote repository..."
    cd "$FULL_PATH"

    # Use gh CLI to create repository
    gh repo create "$PROJECT_NAME" --private --source=. --remote=origin

    # Push branches and tags (switch back to master first)
    echo "Pushing branches and tags to remote..."
    git checkout master
    git push -u origin master
    git push origin "$INITIAL_TAG"
    git push -u origin develop
    git checkout develop

    echo ""
    echo "GitHub repository created successfully!"

    # Get repository URL
    REPO_URL=$(git config --get remote.origin.url)
    if [[ "$REPO_URL" == "git@github.com"* ]]; then
      # SSH URL
      REPO_URL="https://github.com/$(git config --get user.name)/$PROJECT_NAME"
    fi
    echo "   $REPO_URL"
  fi
else
  echo "Skipping GitHub repository creation"
  echo "   You can run manually later:"
  echo "   cd $FULL_PATH && gh repo create $PROJECT_NAME --private --source=. --remote=origin"
fi

echo ""
echo "Project initialization complete!"
echo ""
echo "Git workflow summary:"
echo "   - master: main branch (production) - direct push prohibited"
echo "   - develop: development branch"
echo "   - feature/xxx: feature branch (created from develop)"
echo "   - bugfix/xxx: bug fix branch (created from develop)"
echo ""
echo "Common commands:"
echo "   git checkout develop                    # switch to develop branch"
echo "   git checkout -b feature/xxx             # create feature branch"
echo "   git checkout develop && git merge --no-ff feature/xxx  # merge feature branch"
echo "   git tag -a v1.0.0 -m \"release: v1.0.0\" # create version tag"
echo ""
echo "uv common commands:"
echo "   uv run python script.py                 # run script (no need to activate venv)"
echo "   uv add <package>                        # add dependency"
echo "   uv add --dev pytest black ruff          # add dev dependencies"
echo "   uv lock --check                         # check if lockfile is up to date"
echo "   uv sync --frozen                        # use in CI (exact versions)"
echo ""
echo "Next step:"
echo "   cd $FULL_PATH"
echo "   # Dependencies are installed, virtual environment created (.venv)"
echo ""
