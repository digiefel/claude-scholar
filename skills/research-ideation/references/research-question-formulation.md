# Research Question Formulation

A systematic method for transforming research interests into specific, actionable research questions.

## 1. SMART Principles

Good research questions should satisfy the SMART principles:

### 1.1 Specific

**Bad question**:
- "How to improve model performance?" (too broad)

**Good question**:
- "How can improving the attention mechanism enhance Transformer performance on long-text understanding tasks?"

**Key elements**:
- Clear research subject (Transformer)
- Specific improvement direction (attention mechanism)
- Clear task scenario (long-text understanding)
- Clear goal (improve performance)

### 1.2 Measurable

Research questions should have clear evaluation criteria:

**Examples**:
- "Improve performance" → "Improve F1 score on the SQuAD dataset"
- "Improve interpretability" → "Improve human-evaluated faithfulness score"

**Evaluation dimensions**:
- Quantitative metrics: accuracy, F1, BLEU, perplexity
- Qualitative metrics: human evaluation, case analysis
- Efficiency metrics: training time, inference speed, memory footprint

### 1.3 Achievable

Consider resource and capability constraints:

**Resource assessment**:
- Computational resources: number and type of GPUs
- Data resources: availability and quality of datasets
- Time resources: research duration (3 months, 6 months, 1 year)
- Human resources: team size and professional skills

**Feasibility check**:
- Is there similar existing work as a foundation?
- Is the required technology already mature?
- Are datasets publicly available?
- Is the computational cost within budget?

### 1.4 Relevant

Research questions should have value for academia or industry:

**Academic value**:
- Fills a research gap
- Challenges existing assumptions
- Provides new theoretical perspectives
- Advances methodology

**Practical value**:
- Solves real-world application problems
- Improves system performance
- Reduces cost or resource consumption
- Improves user experience

### 1.5 Time-bound

Set a reasonable research timeframe:

**Short-term goals** (1-3 months):
- Literature review and problem definition
- Initial experiments and proof of concept

**Medium-term goals** (3-6 months):
- Method development and optimization
- Full experiments and analysis

**Long-term goals** (6-12 months):
- Paper writing and submission
- Code open-source and community outreach

## 2. Research Question Types

### 2.1 Exploratory Questions

**Characteristics**: Explore unknown territory, discover new phenomena

**Examples**:
- "What patterns does the Transformer attention mechanism exhibit when processing long texts?"
- "What internal representations do large language models use for reasoning tasks?"

**Applicable scenarios**:
- Emerging research fields
- Phenomena lacking theoretical foundations
- Complex systems requiring deeper understanding

### 2.2 Confirmatory Questions

**Characteristics**: Validate hypotheses or theories

**Examples**:
- "Does increasing model depth improve long-text understanding performance?"
- "Does pre-training help low-resource language tasks?"

**Applicable scenarios**:
- Clear hypotheses that need validation
- Challenging existing theories or views
- Reproducing and extending existing work

### 2.3 Applied Questions

**Characteristics**: Solve practical application problems

**Examples**:
- "How to reduce model size by 50% while maintaining performance?"
- "How to make dialogue systems better understand user intent?"

**Applicable scenarios**:
- Clear application requirements
- Optimization under constraints
- Industry collaboration projects

## 3. Research Question Evaluation Criteria

### 3.1 Significance

**Evaluation dimensions**:
- **Academic impact**: Does it advance the field?
- **Practical value**: Does it solve important problems?
- **Audience size**: How many people care about this problem?

**Scoring criteria** (1-5 points):
- 5: Breakthrough problem affecting the entire field
- 4: Important problem, multiple research groups paying attention
- 3: Valuable problem, some researchers interested
- 2: Peripheral problem, limited interest
- 1: Trivial problem, almost no interest

### 3.2 Novelty

**Evaluation dimensions**:
- **Problem novelty**: Is it a new problem?
- **Method novelty**: Is it using a new method?
- **Perspective novelty**: Is there a new perspective?

**Scoring criteria** (1-5 points):
- 5: Entirely new problem or breakthrough method
- 4: New problem or significantly improved method
- 3: New perspective or method combination
- 2: Incremental improvement
- 1: Duplicates existing work

### 3.3 Feasibility

**Evaluation dimensions**:
- **Technical feasibility**: Can current technology achieve this?
- **Resource feasibility**: Are resources sufficient?
- **Time feasibility**: Is the timeline reasonable?

**Scoring criteria** (1-5 points):
- 5: Fully feasible, resources sufficient
- 4: Basically feasible, resources adequate
- 3: Has challenges, requires effort
- 2: Relatively difficult, requires breakthroughs
- 1: Almost infeasible

### 3.4 Comprehensive Assessment

**Decision matrix**:

| Significance | Novelty | Feasibility | Recommendation |
|-------------|---------|-------------|----------------|
| High | High | High | Execute first |
| High | High | Medium | Worth trying |
| High | Medium | High | Safe choice |
| Medium | High | High | Can consider |
| Low | * | * | Reconsider |
