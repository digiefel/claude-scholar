# Multi-Person Collaboration Standards

## Pull Request Standards

A PR should include the following content:

```markdown
## Change Description
<!-- Describe the content and purpose of this change -->

## Change Type
- [ ] New feature (feat)
- [ ] Bug fix (fix)
- [ ] Code refactoring (refactor)
- [ ] Documentation update (docs)
- [ ] Other

## How to Test
<!-- Describe how to test these changes -->

## Related Issue
Closes #xxx

## Checklist
- [ ] Code has been self-tested
- [ ] Documentation has been updated
- [ ] Change has been added to CHANGELOG
```

## Code Review Standards

### Review Points

#### 1. Code Quality

- Is the code clear and readable
- Are naming conventions followed
- Is there duplicate code

#### 2. Logical Correctness

- Is the business logic correct
- Are boundary conditions handled
- Are exception cases considered

#### 3. Security

- Are there security vulnerabilities
- Is sensitive information exposed
- Is input validated

#### 4. Performance

- Are there performance problems
- Are resources properly released
- Is algorithm complexity reasonable

### Feedback Format

```markdown
<!-- Must fix -->
REQUIRED: There is an SQL injection risk here; use parameterized queries

<!-- Suggestion -->
SUGGESTION: This method could be extracted as a utility function to improve reusability

<!-- Discussion -->
DISCUSSION: Could we consider using caching here?

<!-- Praise -->
PRAISE: This encapsulation is very elegant!
```

## Best Practices Summary

### Commit Standards

Recommended:

- Use Conventional Commits specification
- Commit messages clearly describe the change
- One commit does one thing
- Run code checks before committing

Prohibited:

- Vague commit messages
- Committing multiple unrelated changes at once
- Committing sensitive information (passwords, keys)
- Developing directly on the main branch

### Branch Management

Recommended:

- Use feature branches for development
- Regularly sync main branch code
- Delete branches promptly after feature is complete
- Use `--no-ff` merge to preserve history

Prohibited:

- Developing directly on the main branch
- Long-running feature branches that never merge
- Non-standard branch naming
- Rebasing on public branches

### Code Review

Recommended:

- All code goes through Pull Requests
- At least one reviewer must approve before merging
- Provide constructive feedback

Prohibited:

- Merging without review
- Reviewing your own code
