# Commit Message Detailed Conventions

## Conventional Commits Format

Commit messages follow the **Conventional Commits** specification and use the following format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

## Field Descriptions

| Field | Required | Description |
|:------|:---------|:------------|
| type | Yes | Commit type |
| scope | No | Affected scope |
| subject | Yes | Short description |
| body | No | Detailed description |
| footer | No | Footer information |

## Type Values

| Type | Description | Example |
|:-----|:------------|:--------|
| `feat` | New feature | `feat(user): add user export feature` |
| `fix` | Bug fix | `fix(login): fix CAPTCHA not refreshing` |
| `docs` | Documentation update | `docs(api): update API documentation` |
| `style` | Code formatting | `style: adjust code indentation` |
| `refactor` | Refactoring | `refactor(utils): refactor date utility functions` |
| `perf` | Performance optimization | `perf(list): optimize list rendering performance` |
| `test` | Tests | `test(user): add user module unit tests` |
| `build` | Build-related | `build: upgrade vite to 5.0` |
| `ci` | CI configuration | `ci: add GitHub Actions` |
| `chore` | Other changes | `chore: update dependency versions` |
| `revert` | Revert commit | `revert: revert feat(user)` |

## Scope Values

Scope describes the area affected by the commit. Common scopes include:

- `data` - Data processing
- `utils` - Utility functions
- `model` - Model architecture
- `config` - Parameter configuration
- `trainer` - Training
- `evaluator` - Evaluation
- `workflow` - Workflow

## Subject Standards

- Start with a verb: add, fix, update, remove, optimize
- No more than 50 characters
- Do not end with a period
- Use English consistently

### Correct and Incorrect Examples

```
# Correct examples
feat(user): add user export feature
fix(login): fix CAPTCHA not refreshing

# Incorrect examples
feat(user): add user export feature.    # no period
feat(user): user export                 # must start with verb
feat: added a new user export feature   # too long
```

## Body Detailed Description

When the change is large or the reason needs to be explained, use Body for detailed description:

```
feat(user): add batch user import feature

- Supports Excel file import
- Supports data validation and error messages
- Supports import progress display

Related issue: #123
```

## Footer

Used to link Issues or describe breaking changes:

```
# Link Issue
Closes #123, #456

# Breaking change
BREAKING CHANGE: user interface return format changed
Old format: { data: user }
New format: { code: 200, data: user, msg: 'success' }
```

## Complete Examples

### Simple Commit

```bash
git commit -m "feat(user): add user export feature"
```

### Commit with Body

```bash
git commit -m "fix(login): fix CAPTCHA not refreshing

Cause: Cache time was set too long, causing the CAPTCHA to always show the same image
Solution: Reduced cache time from 5 minutes to 1 minute"
```

### Commit with Footer

```bash
git commit -m "feat(api): refactor user API

BREAKING CHANGE: user query endpoint path changed
Old path: /api/user/list
New path: /api/system/user/list

Closes #789"
```
