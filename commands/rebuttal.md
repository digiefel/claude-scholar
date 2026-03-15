---
name: rebuttal
description: Start systematic review response workflow for professional rebuttal writing
args:
  review_file:
    description: Path to the review file (optional)
    required: false
---

# /rebuttal - Review Response Workflow

Start a systematic rebuttal writing workflow, from review analysis to final rebuttal document generation.

## Usage

```bash
/rebuttal [review_file]
```

**Arguments**:
- `review_file` (optional): path to the file containing review comments
  - If not provided, the user will be guided to provide the review comments

## Features

This command starts a complete rebuttal writing workflow:

1. **Get review comments** - read or receive review comments
2. **Analyze and classify** - classify comments into Major/Minor/Typo/Misunderstanding
3. **Develop strategy** - select a response strategy for each comment
4. **Write rebuttal** - generate a structured response document
5. **Tone optimization** - ensure professional and polite expression
6. **Generate output** - save the final rebuttal document


## Workflow

### Step 1: Get Review Comments

If the `review_file` argument is provided:
- Read the file content
- Identify the number of reviewers and comment structure

If no file is provided:
- Guide the user to paste or describe the review comments
- Confirm the number of reviewers

### Step 2: Analyze and Classify

Use the `rebuttal-writer` agent for analysis:
- Group comments by reviewer
- Classify into Major/Minor/Typo/Misunderstanding
- Identify priorities

### Step 3: Develop Response Strategy

Select a strategy for each comment:
- **Accept** - accept and improve
- **Defend** - politely defend
- **Clarify** - clarify misunderstandings
- **Experiment** - add supplementary experiments


### Step 4: Write the Rebuttal

Generate a structured response:
- Write a Response and Changes for each comment
- Include specific location references
- Provide evidence and reasoning

### Step 5: Tone Optimization

Check and optimize tone:
- Ensure each response begins with thanks
- Avoid defensive or aggressive language
- Maintain professionalism and respect

### Step 6: Generate Output

Save the final documents:
- `rebuttal.md` - complete rebuttal document
- `review-analysis.md` - review comment analysis (optional)
- `experiment-plan.md` - supplementary experiment plan (if additional experiments are needed)


## Output Files

After running this command, the following files will be generated:

### rebuttal.md
Complete rebuttal document including:
- Opening (thanking reviewers)
- Point-by-point responses (Response + Changes)
- Summary of major revisions

### review-analysis.md (optional)
Review comment analysis document including:
- Comment classification statistics
- Strategy selection rationale
- List of experiments to add

### experiment-plan.md (optional)
Supplementary experiment plan including:
- List of experiments to add
- Purpose and expected results of each experiment
- Priority and time estimate for each experiment

## Usage Examples

### Example 1: Provide a review file

```bash
/rebuttal reviews.txt
```

Reads the review comments from `reviews.txt` and starts the rebuttal writing workflow.

### Example 2: Interactive input

```bash
/rebuttal
```

Guides you to paste or describe review comments, then starts the rebuttal writing workflow.


## Notes

### Important Principles

1. **No code parsing** - review comment analysis is done through natural language understanding, not automated scripts
2. **Maintain professional tone** - all responses must be polite, respectful, and well-reasoned
3. **Provide specific evidence** - every response must include specific location references and evidence
4. **Completeness check** - ensure all review comments receive a response

### Reference Resources

This command automatically uses the following reference documents:
- `review-classification.md` - comment classification standards
- `response-strategies.md` - response strategy guide
- `rebuttal-templates.md` - response template library
- `tone-guidelines.md` - tone optimization guide

### Agent Invocation

This command automatically calls the `rebuttal-writer` agent to execute the rebuttal writing task.

## Related Commands

- `/commit` - commit revised paper
- `/code-review` - review code quality

---

**Tip**: Before using this command, it is recommended to have the review file ready and to ensure that necessary revisions to the paper have been completed.
