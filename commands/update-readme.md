---
description: Update README documentation and push changes to GitHub.
---

# Update README

Update README.md file with latest project information and push to GitHub.

## Instructions

1. **Analyze Current State**
   - Read existing README.md
   - Check recent code changes (git log)
   - Identify documentation gaps

2. **Determine Updates Needed**
   Check for:
   - New features added
   - Configuration changes
   - Dependencies updated
   - Installation instructions
   - Usage examples
   - API changes

3. **Propose README Updates**
   Show sections that need updating:
   ```markdown
   Proposed changes:
   - [ ] Update Installation section (new dependencies)
   - [ ] Add usage example for feature X
   - [ ] Update API documentation
   - [ ] Fix broken links
   ```

4. **Update README**
   - Apply proposed changes
   - Maintain markdown formatting
   - Keep language consistent
   - Preserve structure

5. **Commit and Push**
   - Run `/update-github` with `docs(readme):` type
   - Example commit: `docs(readme): update README documentation`

## Example Usage

```
User: /update-readme

1. Analyzing repository state...

Recent changes:
- feat(data): add new data loader
- fix(model): fix memory leak during training
- chore: update dependencies to v2.0.0

2. Checking README.md...

Current README sections:
- Installation
- Usage
- API Reference
- Contributing

3. Proposed updates:
   [ ] Installation - add new dependency instructions
   [ ] Usage - add data loader example
   [ ] API Reference - update model interface docs

4. Applying updates...

   Updating Installation:
   + pip install torch>=2.0.0
   + pip install transformers>=4.30.0

   Adding usage example:
   ## Data Loading Example
   ```python
   from data import DataLoader
   loader = DataLoader(batch_size=32)
   ```

5. Review changes before committing...
   [Show diff]

6. Proceed with commit?
   > yes

7. Committing with: docs(readme): update README documentation
   Co-Authored-By: Claude <noreply@anthropic.com>

README updated and pushed to GitHub!
```

## README Structure Template

When updating README, follow this structure:

```markdown
# Project Name

Short description of what the project does.

## Installation

### Requirements
- Python >= 3.8
- uv or pip

### Installation Steps
```bash
uv sync
```

## Usage

### Basic Usage
```python
# example code
```

### Configuration
Describe configuration file location and format.

## API Documentation

Main interface descriptions.

## Development

### Running Tests
```bash
pytest
```

### Code Standards
- Follow PEP 8
- Use mypy for type checking
- Use ruff for linting

## Contributing

Pull Requests are welcome.

## License

MIT License
```

## Arguments

$ARGUMENTS can be:
- `--full` - Complete README rewrite
- `--quick` - Only update critical sections (installation, usage)
- `<section>` - Update specific section only

## Integration

After updating README, this command automatically invokes `/update-github` with `docs(readme):` commit type.
