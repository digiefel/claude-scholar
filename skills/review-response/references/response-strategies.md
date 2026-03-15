# Response Strategy Library

This document provides systematic response strategies for different types of review comments, helping to write professional and effective rebuttals.

## Four Core Strategies

### 1. Accept

**Applicable scenarios**:
- The reviewer has identified a genuine problem or deficiency
- The cost of revision is low and will improve paper quality
- Typos and formatting issues
- Reasonable improvement suggestions

**Response template**:
```
We thank the reviewer for this valuable suggestion. We have [specific action taken].
```

**Example**:

**Review comment**:
> "The related work section is too brief and misses several important recent papers."

**Response**:
> "We thank the reviewer for pointing this out. We have significantly expanded the related work section and added discussions of the suggested papers [X, Y, Z]. The revised section now provides a more comprehensive overview of the field."


---

### 2. Defend

**Applicable scenarios**:
- The current approach has sound reasons
- The reviewer's suggestion does not apply to this research
- Need to explain the rationale for design choices

**Key principles**:
- Maintain politeness and respect
- Provide sufficient justification and evidence
- Avoid expressions such as "The reviewer is wrong"

**Response template**:
```
We appreciate the reviewer's concern. However, we respectfully note that [explanation]. This choice is motivated by [specific reason].
```

**Example**:

**Review comment**:
> "The authors should use method X instead of method Y."

**Response**:
> "We appreciate the reviewer's suggestion. However, we respectfully note that method Y is more suitable for our specific setting because [reason 1] and [reason 2]. While method X has advantages in [scenario A], our preliminary experiments showed that method Y achieves better performance in our task due to [specific reason]. We have added this discussion to Section 3.2."


---

### 3. Clarify

**Applicable scenarios**:
- The reviewer misunderstood the paper content
- Related content already exists in the paper but the reviewer did not notice
- Need to point to existing explanations or experiments in the paper

**Key principles**:
- Politely point to existing content in the paper
- Provide specific location references (sections, page numbers, figures/tables)
- Avoid making the reviewer feel embarrassed
- Consider improving wording to make it clearer

**Response template**:
```
We thank the reviewer for raising this point. We would like to respectfully clarify that [description of existing content]. This is discussed in [specific location]. To make this clearer, we have [improvement action].
```

**Example**:

**Review comment**:
> "The authors did not compare their method with baseline X."

**Response**:
> "We thank the reviewer for this comment. We would like to respectfully clarify that we did include comparisons with baseline X in our experiments. These results are presented in Table 2 (page 6) and discussed in Section 4.2. To make this comparison more prominent, we have added a dedicated paragraph highlighting the key differences and added baseline X to Figure 3 for visual comparison."

**Notes**:
- Even if the reviewer misunderstood, maintain politeness and respect
- If possible, acknowledge that the paper phrasing could be clearer and make improvements
- Provide specific citation locations to make it easy for the reviewer to find


---

### 4. Experiment

**Applicable scenarios**:
- Reviewer requests supplementary key experiments or comparisons
- The experimental request is reasonable and feasible
- Additional experiments can significantly strengthen the paper
- Experimental requirements in Major Issues

**Key principles**:
- Explicitly commit to conducting additional experiments
- Describe the experimental design and expected timeline
- If already completed, show results directly
- If time is tight, describe preliminary results or plans

**Response template**:
```
We thank the reviewer for this valuable suggestion. We agree that [importance of experiment]. We have conducted additional experiments on [content]. The results show that [main findings]. These new results have been added to [location].
```

**Example 1 (experiments completed)**:

**Review comment**:
> "The authors should compare their method with the recent state-of-the-art method Z."

**Response**:
> "We thank the reviewer for this excellent suggestion. We agree that comparing with method Z is important for a comprehensive evaluation. We have conducted additional experiments comparing our method with Z on all three datasets. The results show that our method achieves comparable or better performance (Dataset A: +2.3%, Dataset B: +1.1%, Dataset C: -0.5%). These new results have been added to Table 3 and discussed in Section 4.3. We also provide detailed analysis of the performance differences in the revised manuscript."

**Example 2 (committing to experiments)**:

**Review comment**:
> "The authors should conduct ablation studies to verify the contribution of each component."

**Response**:
> "We thank the reviewer for this important suggestion. We agree that ablation studies are crucial for understanding the contribution of each component. We are currently conducting comprehensive ablation experiments and will include the results in the revised manuscript. Based on our preliminary analysis, we expect to show that [expected findings]. We will complete these experiments within the rebuttal period and update the manuscript accordingly."

**Notes**:
- Only commit to feasible experiments; do not over-commit
- If experiments are not feasible, explain the reason (time, resources, technical constraints)
- Provide an experimental timeline so the reviewer understands the progress
- If already completed, show results immediately to strengthen persuasiveness


---

## Success Patterns (Based on ICLR Spotlight Papers)

Key patterns extracted from successful rebuttals of ICLR 2024 spotlight papers:

### Pattern 1: Acknowledge Strengths, Address Criticism Positively

**Observations**:
- Reviewers typically first acknowledge the paper's strengths (novelty, impact, practical applicability)
- Even spotlight papers receive constructive criticism
- About 20% of papers see their ranking change after rebuttal

**Application strategy**:
```
We thank the reviewer for recognizing [acknowledged strength]. Regarding [concern], we have [specific action taken].
```

**Example**:
> "We thank the reviewer for recognizing the novelty of our game-theoretic formulation. Regarding the brevity of Section 2.2, we have expanded it with 2-3 additional paragraphs providing more intuition for readers without a game theory background."

---

### Pattern 2: Provide Clarity and Intuitive Understanding

**Observations**:
- High-quality papers can still have clarity issues
- Reviewers need to provide intuition for readers from different backgrounds
- Suggestions: expand sections, move technical details to appendix

**Application strategy**:
```
We apologize for the confusion. We have [clarification action]. To make this clearer, we have [additional improvements].
```

**Example**:
> "We apologize for the confusion in Section 3.2. We have completely rewritten this section with detailed mathematical formulation and added Algorithm 1 with pseudocode. We have also moved some technical details to Appendix B to improve readability."

---

### Pattern 3: Thoroughly Justify Experimental Setup

**Observations**:
- Reviewers expect thorough justification for experimental setup
- Need to consider and discuss alternative metrics
- Comprehensive experiments are a common feature of spotlight papers

**Application strategy**:
```
We chose [experimental setup] because [justification]. We have also considered [alternative approach], but [reason for current choice]. We have added [additional experiments] to strengthen our evaluation.
```

**Example**:
> "We chose dataset W because it better represents our target scenario [justification]. We have also considered dataset Z, but it focuses on static graphs while our work targets dynamic graphs. We have added ablation studies showing that our improvement comes from fundamental architectural innovations."

---

### Pattern 4: Proactively Discuss Ethical Considerations

**Observations**:
- For research involving privacy, security, and other sensitive topics, ethical considerations are crucial
- Reviewers pay particular attention to ethical implications
- Spotlight papers typically have thorough ethical discussions

**Application strategy**:
```
We appreciate the concern about ethical implications. We have [ethical consideration actions]. We have also added [ethical safeguards/discussions].
```

**Example**:
> "We appreciate the concern about privacy implications. We have added a comprehensive ethics section discussing potential risks and mitigation strategies. We have also included anonymization experiments and detailed our data handling procedures in Appendix C."

---

### Pattern 5: Emphasize Practical Application Value

**Observations**:
- Reviewers value practical applicability and scalability
- "Easily applicable" and "scalable" are important strengths
- Spotlight papers typically demonstrate practical benefits

**Application strategy**:
```
Our method is [practical benefit]. It is easily applicable because [reason] and scales to [scale] without [limitation].
```

**Example**:
> "Our method is practical and easily applicable to large language models without extensive tuning. It scales efficiently to models with up to 540B parameters, as demonstrated by our experiments. The consistent performance improvements across different model sizes highlight its practical value."

---

## Combining Strategies

In practice, rebuttals typically combine multiple strategies:

### Example 1: Accept + Clarify

**Review comment**:
> "The paper lacks discussion of limitation X, and the authors did not mention related work Y."

**Response**:
> "We thank the reviewer for these valuable comments. Regarding limitation X, we agree this is an important point and have added a dedicated discussion in Section 5.3 (**Accept**). Regarding related work Y, we would like to respectfully clarify that we did discuss this work in Section 2.2 (page 3, paragraph 2). To make this more prominent, we have expanded the discussion and added it to the comparison table (**Clarify**)."

### Example 2: Defend + Experiment

**Review comment**:
> "The authors should use dataset Z instead of dataset W, and should add experiments on task T."

**Response**:
> "We appreciate the reviewer's suggestions. Regarding dataset Z, we respectfully note that dataset W is more suitable for our research question because [reason]. Dataset Z focuses on [scenario A], while our work targets [scenario B] (**Defend**). However, we agree that experiments on task T would strengthen our evaluation. We have conducted additional experiments on task T, and the results show [findings]. These new results have been added to Section 4.4 (**Experiment**)."


---

## Usage Guide

### Strategy Selection Workflow

```
Review comment → Classify (Major/Minor/Typo/Misunderstanding) → Select strategy
|
├─ Major Issues → Experiment (additional experiments) or Defend (sufficient justification)
├─ Minor Issues → Accept (accept improvement) or Clarify (clarify explanation)
├─ Typos/Formatting → Accept (directly accept)
└─ Misunderstandings → Clarify (polite clarification)
```

### Strategy Priority

1. **Prefer Accept**: If the comment is reasonable and the revision cost is low
2. **Use Defend carefully**: Only when there are sufficient reasons
3. **Clarify politely**: Even if the reviewer misunderstood, maintain respect
4. **Be honest about Experiment**: Only commit to feasible experiments

### Tone Principles

**Always maintain**:
- Thank the reviewer for their comments
- Respectful and polite attitude
- Specific citations and evidence
- Constructive responses

**Avoid**:
- "The reviewer is wrong"
- "This is obvious"
- Defensive or aggressive tone
- Vague or evasive answers

---

## Conference-Specific Strategies

Different top conferences have different emphases on rebuttals; understanding these differences helps write more targeted responses.

### NeurIPS

**Conference characteristics**:
- Emphasizes conceptual novelty and theoretical contribution
- Values broader impact and societal influence
- Requires reproducibility checklist

**Rebuttal focus**:
1. **Highlight conceptual innovation** - Emphasize the conceptual novelty of your method
2. **Show broader impact** - Describe the social significance and potential impact of the research
3. **Ensure reproducibility** - Commit to open-sourcing code and data

**Example opening**:
```markdown
We thank the reviewers for their constructive feedback. Our key contributions advance the field by [conceptual innovation]. We have strengthened the paper with [new experiments] and clarified [methodology]. All code and data will be released upon acceptance to ensure reproducibility.
```

**Response strategies**:
- When reviewers question novelty, emphasize conceptual breakthroughs rather than just performance gains
- Proactively discuss broader impact even if the reviewer did not explicitly request it
- Provide detailed experimental settings and hyperparameters to ensure reproducibility

---

### ICML

**Conference characteristics**:
- Emphasizes methodological rigor and theoretical foundations
- Values mathematical proofs and theoretical analysis
- Requires broader impact statement

**Rebuttal focus**:
1. **Show theoretical rigor** - Provide mathematical proofs and theoretical analysis
2. **Emphasize methodological contributions** - Describe the theoretical advantages of the method
3. **Supplement theoretical analysis** - Add theorems, lemmas, or theoretical guarantees

**Example opening**:
```markdown
We appreciate the reviewers' thorough evaluation. We have added theoretical analysis (Theorem 2, Appendix C) proving [property]. Our method's soundness is further validated by [experiments]. We have also expanded the broader impact statement to address [concern].
```

**Response strategies**:
- When reviewers question the method, provide theoretical proofs rather than just experimental results
- Emphasize the theoretical complexity and convergence guarantees of the algorithm
- Connect experimental results with theoretical predictions

---

### ICLR

**Conference characteristics**:
- Emphasizes experimental thoroughness and comprehensive evaluation
- Values honest discussion of limitations
- Requires LLM usage disclosure (if applicable)

**Rebuttal focus**:
1. **Add experiments** - Include the comparison experiments and ablation studies requested by reviewers
2. **Expand limitations discussion** - Honestly acknowledge method limitations
3. **Disclose LLM usage** - If LLMs were used, clearly state how

**Example opening**:
```markdown
We thank the reviewers for their detailed comments. We have conducted additional experiments (Tables 4-6) addressing all concerns. We have also expanded the Limitations section (Section 5.2) and added LLM usage disclosure (Appendix D). These revisions significantly strengthen the empirical validation.
```

**Response strategies**:
- When reviewers request more experiments, prioritize adding them rather than defending
- Proactively expand limitations discussion, demonstrating clear understanding of method boundaries
- If LLMs were used for writing or experiments, honestly disclose and describe specific uses

**ICLR-specific strategies**:

**1. Evidence-supported clarifications are most effective**
- Research shows that clarifications backed by evidence are most strongly correlated with score increases
- Avoid vague or evasive responses, which maintain or lower scores
- Explicitly cite specific sections or line numbers in the original paper

**Example**:
```markdown
Thank you for this concern. We respectfully clarify that we did include this comparison in Section 4.2 (page 6, lines 234-245). To make this more prominent, we have added a dedicated paragraph and included the baseline in Figure 3 for visual comparison.
```

**2. Strategy for borderline papers**
- Rebuttal has the greatest impact on borderline-scored papers (5-6 range)
- If the paper is borderline, even small improvements may affect the final decision
- Focus on aspects that can be quickly improved

**3. Submission timing strategy**
- Submitting mid-period during the rebuttal window may be more effective
- Avoid submitting too early or at the last minute
- Mid-period submission can increase reviewer engagement and score changes

**4. Systematic response structure**
Each response should follow a three-step structure:
1. **Summarize the reviewer's point** - Show that you understood their feedback
2. **State your response** - Clearly describe your position
3. **Provide specific evidence** - Give experiments, explanations, or revision plans

**Example**:
```markdown
**Reviewer's Concern**: The baseline comparison is insufficient.

**Our Response**: We appreciate this feedback. We understand the reviewer's concern about baseline coverage.

**Evidence**: We have added comparisons with three additional baselines (X, Y, Z) in Table 4 (Appendix). Results show our method achieves +2.3% improvement over the strongest baseline Z. We will integrate this into the main paper.
```

**5. Leveraging page limit expansion**
- ICLR 2026 expanded the camera-ready version from 9 to 10 pages
- The extra page can be used to integrate new results or discussions from the rebuttal
- In the rebuttal, commit to adding new content to the final version

**6. Reproducibility statement**
- Strongly recommended to include a reproducibility statement at the end of the main text (before references)
- Discuss efforts made to ensure reproducibility
- Reference relevant sections in the paper, appendix, or supplementary materials

**7. ICLR 2026 scoring system**
- Uses discrete scores: {0, 2, 4, 6, 8, 10}
- 0=Strong Reject, 2=Reject, 4=Weak Reject, 6=Weak Accept, 8=Accept, 10=Strong Accept
- Understanding the scoring system helps judge which range the paper falls in

---

### CVPR

**Conference characteristics**:
- Top computer vision conference, highly competitive
- Strict one-page rebuttal limit
- No external links or large-scale new experiments
- Values visual quality and experimental completeness

**Rebuttal focus**:
1. **Identify "Champion" reviewers** - Find reviewers who support your paper and provide them with strong arguments
2. **Reiterate core contributions** - When addressing criticism, subtly remind reviewers of the paper's key contributions
3. **Show responsiveness** - Clearly state how suggestions will be incorporated in the final version

**Example opening**:
```markdown
We thank all reviewers for their valuable feedback. We are particularly grateful to R2 for recognizing our novel approach to [X]. Regarding the concerns raised, we provide clarifications below and will incorporate all valid suggestions in the camera-ready version.
```

**Response strategies**:
- Identify reviewers with positive attitudes and provide arguments to help them defend the paper in discussion
- While addressing issues, subtly reinforce the paper's core strengths
- Provide clear, convincing clarifications for misunderstandings of key concepts
- Show genuine attention to reviewer suggestions and list specific improvement plans

**Special restrictions**:
- Must use the official template with a strict one-page limit
- No external links (code, video, supplementary materials)
- May include figures and comparison tables based on existing results
- Reviewers should not require large-scale new experiments

---

### ACL

**Conference characteristics**:
- Top natural language processing conference
- Best paper criteria: fascinating, controversial, surprising, impressive, field-changing
- Values the linguistic significance and practical application of methods
- Requires Limitations and Ethics Statement

**Rebuttal focus**:
1. **Small table strategy** - If reviewers request additional results, include small tables in the rebuttal
2. **Enhance understanding** - Goal is to enhance reviewer understanding of the paper, not large-scale rewrites
3. **Highlight impact** - Emphasize the potential impact of the research on the NLP field

**Example opening**:
```markdown
We thank the reviewers for their insightful comments. We have prepared additional analysis to address the raised concerns. Below we provide clarifications and include a small table (Table R1) demonstrating the requested comparison. These results will be integrated into the revised manuscript.
```

**Response strategies**:
- If reviewers request additional data, include a small table in the rebuttal
- Emphasize the linguistic significance and contribution to the NLP community
- Proactively discuss ethical implications, especially for research involving bias and fairness
- Show consideration for different languages and cultural contexts

**Best Paper considerations**:
- Is the paper "fascinating" - Raises exciting new questions or perspectives
- Is it "controversial" - Challenges existing assumptions
- Is it "surprising" - Counter-intuitive but convincing findings
- Is it "impressive" - Technical depth or experimental scale
- Is it "field-changing" - Potential long-term impact

---

## Reference Resources

For more detailed successful cases and templates, see:
- `successful-cases.md` - Real successful rebuttal case library
- `rebuttal-templates.md` - Complete rebuttal templates
- `tone-guidelines.md` - Tone and expression guide
