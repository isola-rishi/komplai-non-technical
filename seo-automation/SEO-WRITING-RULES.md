# SEO Writing Rules: Do's and Don'ts Guide

> **Purpose**: This guide focuses exclusively on sentence-level writing rules to pass Yoast SEO checks. Load this guide before generating any SEO content.

---

## THE TWO CRITICAL RULES

These rules are **non-negotiable**. Content failing either rule will be rejected.

### Rule 1: ZERO Consecutive Sentences Starting with the Same Word

Every sentence **MUST** start with a different word than the sentence before it.

- **Target**: 0 consecutive same-word starts
- **Check**: Compare the first word of each sentence to the first word of the previous sentence
- **If they match**: REWRITE one of them immediately

### Rule 2: Minimum 35% Transition Word Usage

At least 35% of all sentences must begin with a transition word.

- **Target**: 35% or higher
- **Formula**: `(sentences starting with transitions / total sentences) × 100`
- **Pattern**: Use a transition word every 2-3 sentences

---

## TRANSITION WORDS BY CATEGORY

Use these words to start sentences. Rotate through categories to maintain variety.

| Category | Transition Words |
|----------|------------------|
| **Addition** | Additionally, Furthermore, Moreover, Also, In addition, Besides, Equally |
| **Contrast** | However, Nevertheless, Conversely, On the other hand, Yet, Still, Instead |
| **Cause/Effect** | Therefore, Consequently, As a result, Thus, Hence, Accordingly |
| **Sequence** | First, Second, Third, Next, Then, Finally, Subsequently, Afterward |
| **Emphasis** | Indeed, Importantly, Notably, Certainly, Clearly, Significantly |
| **Example** | For example, For instance, Specifically, In particular, Such as |
| **Summary** | Overall, Ultimately, In summary, To conclude, In conclusion |
| **Time** | Currently, Previously, Meanwhile, Initially, Recently, Now |
| **Comparison** | Similarly, Likewise, In comparison, By contrast |

---

## DO's: What You SHOULD Do

### DO: Alternate Sentence Starters Systematically

**Good Pattern:**
```
The process begins with data collection. [Subject: The]
Additionally, teams must verify accuracy. [Transition: Additionally]
Finance leaders often oversee this step. [Subject: Finance]
Therefore, proper training becomes essential. [Transition: Therefore]
```

Each sentence starts with a different word than the one before it.

### DO: Use Transition Words Every 2-3 Sentences

**Target Pattern:**
- Sentence 1: Any starter
- Sentence 2: Transition word
- Sentence 3: Any starter (different from Sentence 2)
- Sentence 4: Transition word
- Repeat...

### DO: Vary Your Subjects

Rotate between different subjects to avoid repetition:
- Finance teams...
- Companies...
- The process...
- Leaders...
- This approach...
- These tools...
- Many organisations...
- Your team...

### DO: Use Questions and Imperatives for Variety

**Questions as starters:**
- "What happens when..."
- "How can teams..."
- "Why does this matter?"

**Imperatives as starters:**
- "Consider the impact..."
- "Start by identifying..."
- "Remember that..."

### DO: Front-Load Transitions Naturally

Place the transition word at the very beginning:

- **Good**: "However, many teams struggle with this."
- **Bad**: "Many teams, however, struggle with this." (transition buried mid-sentence)

---

## DON'Ts: What You Must AVOID

### DON'T: Start Consecutive Sentences with "The"

**BAD:**
```
The team reviews the data weekly.
The process takes about two hours.
The results show clear improvement.
```

**FIXED:**
```
The team reviews the data weekly.
Typically, this process takes about two hours.
Results show clear improvement.
```

### DON'T: Start Consecutive Sentences with "This"

**BAD:**
```
This helps reduce manual work.
This also improves accuracy.
This saves time for the team.
```

**FIXED:**
```
This helps reduce manual work.
Additionally, it improves accuracy.
Teams save significant time as a result.
```

### DON'T: Start Consecutive Sentences with "It"

**BAD:**
```
It automates the reconciliation process.
It identifies discrepancies instantly.
It sends alerts to the team.
```

**FIXED:**
```
It automates the reconciliation process.
Furthermore, discrepancies are identified instantly.
The system sends alerts to the team automatically.
```

### DON'T: Start Consecutive Sentences with "They"

**BAD:**
```
They implemented the new system last month.
They saw results within weeks.
They reported a 40% time reduction.
```

**FIXED:**
```
They implemented the new system last month.
Results appeared within weeks.
Consequently, the team reported a 40% time reduction.
```

### DON'T: Write 3+ Sentences Without a Transition Word

**BAD (no transitions):**
```
Finance teams spend hours on reconciliation.
Manual processes create bottlenecks.
Errors compound throughout the close cycle.
Deadlines become stressful.
```

**FIXED (transitions added):**
```
Finance teams spend hours on reconciliation.
Consequently, manual processes create bottlenecks.
Errors compound throughout the close cycle.
As a result, deadlines become stressful.
```

### DON'T: Use the Same Transition Word Repeatedly

**BAD:**
```
Additionally, teams benefit from automation.
Additionally, errors decrease significantly.
Additionally, reporting becomes faster.
```

**FIXED:**
```
Additionally, teams benefit from automation.
Furthermore, errors decrease significantly.
As a result, reporting becomes faster.
```

---

## BEFORE/AFTER EXAMPLES

### Example 1: Fixing "The" Repetition

**BEFORE (FAILS - 3 consecutive "The" starts):**
```
The continuous close approach transforms how finance teams operate. The traditional month-end crunch becomes obsolete. The process distributes work evenly across the period. The team experiences less stress and fewer errors.
```

**AFTER (PASSES):**
```
The continuous close approach transforms how finance teams operate. As a result, the traditional month-end crunch becomes obsolete. Work distributes evenly across the period. Consequently, teams experience less stress and fewer errors.
```

**What changed:**
- Sentence 2: Added "As a result" transition, changed "The" to "the" (lowercase, not a starter)
- Sentence 3: Changed subject from "The process" to "Work"
- Sentence 4: Added "Consequently" transition, changed "The team" to "teams"

---

### Example 2: Fixing Low Transition Word Percentage

**BEFORE (FAILS - only 1/5 sentences = 20% transitions):**
```
Automation reduces manual data entry. Teams can focus on analysis instead. Errors decrease when humans aren't typing numbers. Reports generate faster. However, implementation requires planning.
```

**AFTER (PASSES - 3/5 sentences = 60% transitions):**
```
Automation reduces manual data entry. Consequently, teams can focus on analysis instead. Furthermore, errors decrease when humans aren't typing numbers. Reports generate faster. However, implementation requires planning.
```

**What changed:**
- Sentence 2: Added "Consequently" at start
- Sentence 3: Added "Furthermore" at start
- Now 3 of 5 sentences (60%) start with transitions

---

### Example 3: Fixing "This" Repetition

**BEFORE (FAILS - 4 consecutive "This" starts):**
```
This technology learns from historical patterns. This enables predictive anomaly detection. This helps teams catch errors before close. This reduces rework significantly.
```

**AFTER (PASSES):**
```
This technology learns from historical patterns. As a result, predictive anomaly detection becomes possible. Teams can catch errors before close. Subsequently, rework decreases significantly.
```

**What changed:**
- Sentence 2: Removed "This enables" → Added "As a result" + restructured
- Sentence 3: Removed "This helps" → Changed subject to "Teams"
- Sentence 4: Removed "This reduces" → Added "Subsequently" + restructured

---

### Example 4: Comprehensive Rewrite

**BEFORE (FAILS - multiple violations):**
```
The finance team struggled with month-end close. The process took 15 days on average. The CFO wanted faster results. They implemented continuous close methodology. They saw immediate improvements. They reduced close time to 5 days. The ROI exceeded expectations.
```

**Problems identified:**
- Lines 1-3: Three consecutive "The" starts
- Lines 4-6: Three consecutive "They" starts
- Only 0/7 sentences (0%) start with transitions

**AFTER (PASSES):**
```
The finance team struggled with month-end close. Previously, the process took 15 days on average. Naturally, the CFO wanted faster results. They implemented continuous close methodology. Subsequently, improvements appeared immediately. Close time dropped to just 5 days. As a result, ROI exceeded expectations.
```

**What changed:**
- Sentence 2: Added "Previously" transition
- Sentence 3: Added "Naturally" transition
- Sentence 5: Added "Subsequently" + restructured
- Sentence 6: Changed subject to "Close time"
- Sentence 7: Added "As a result" transition
- Now 4/7 sentences (57%) start with transitions

---

### Example 5: Fixing Buried Transitions

**BEFORE (transitions present but not at sentence start):**
```
The system, however, requires configuration.
Teams often, therefore, need training.
Results are, consequently, dependent on setup.
```

**AFTER (transitions moved to front):**
```
However, the system requires configuration.
Therefore, teams often need training.
Consequently, results depend on proper setup.
```

---

### Example 6: Natural Flow with Variety

**BEFORE (robotic, same pattern):**
```
AI analyses transactions. AI identifies patterns. AI flags anomalies. AI learns from corrections. AI improves over time.
```

**AFTER (natural, varied):**
```
AI analyses transactions to identify patterns. Subsequently, the system flags anomalies for review. Each correction teaches the algorithm something new. Over time, accuracy improves dramatically. This creates a virtuous cycle of continuous improvement.
```

---

### Example 7: Converting a List-Heavy Section

**BEFORE (choppy, no flow):**
```
Benefits of continuous close include:
Real-time visibility. Reduced errors. Faster reporting. Better decisions. Less stress.
```

**AFTER (flowing prose):**
```
Continuous close delivers multiple benefits for finance teams. First, real-time visibility replaces outdated monthly snapshots. Additionally, errors decrease because issues surface immediately. Reporting accelerates from weeks to days. Consequently, leaders make better decisions with current data. Perhaps most importantly, the team experiences less end-of-month stress.
```

---

### Example 8: Technical Content Rewrite

**BEFORE (FAILS):**
```
The API connects to your ERP system. The integration pulls transaction data automatically. The system processes entries in real-time. The dashboard displays results instantly. The alerts notify you of discrepancies.
```

**AFTER (PASSES):**
```
The API connects to your ERP system seamlessly. From there, transaction data flows automatically into the platform. Processing happens in real-time. Meanwhile, dashboards display results instantly. Whenever discrepancies arise, alerts notify your team immediately.
```

---

### Example 9: Persuasive Content Rewrite

**BEFORE (FAILS):**
```
You need better close processes. You deserve real-time visibility. You want to eliminate spreadsheet chaos. You can achieve this with automation. You should consider continuous close.
```

**AFTER (PASSES):**
```
You need better close processes. Fortunately, real-time visibility is now achievable. Spreadsheet chaos can become a thing of the past. With the right automation, transformation happens faster than expected. Therefore, continuous close deserves serious consideration.
```

---

### Example 10: Statistics-Heavy Content

**BEFORE (FAILS):**
```
73% of CFOs report close delays. 68% cite manual processes as the cause. 52% have considered automation. 41% implemented changes in 2024. 89% of those saw positive ROI.
```

**AFTER (PASSES):**
```
A striking 73% of CFOs report close delays. Furthermore, 68% cite manual processes as the primary cause. Interestingly, 52% have already considered automation solutions. Of those, 41% implemented changes in 2024. Importantly, 89% of implementers saw positive ROI within the first year.
```

---

## SELF-CHECK FORMULA

Before submitting any content, perform these checks:

### Check 1: Consecutive Sentence Starts

```
1. List the first word of every sentence
2. Compare each word to the previous word
3. If ANY two adjacent words match = FAIL
4. Rewrite until all adjacent pairs are different
```

**Visual Method:**
```
Sentence 1: [The] ←
Sentence 2: [The] ← MATCH! Rewrite Sentence 2
Sentence 3: [Additionally]
Sentence 4: [Teams]
Sentence 5: [Teams] ← MATCH! Rewrite Sentence 5
```

### Check 2: Transition Word Percentage

```
1. Count total sentences in the content
2. Count sentences starting with transition words
3. Calculate: (transition count / total count) × 100
4. If result < 35% = FAIL
5. Add more transition words until ≥ 35%
```

**Example Calculation:**
```
Total sentences: 20
Transition starters: 5
Percentage: (5 / 20) × 100 = 25% = FAIL

After adding 3 more transitions:
Transition starters: 8
Percentage: (8 / 20) × 100 = 40% = PASS
```

---

## QUICK REFERENCE CHECKLIST

Before submitting content, verify:

- [ ] **Zero consecutive same-word starts** - Every sentence begins differently from the previous one
- [ ] **35%+ transition words** - At least 1 in 3 sentences starts with a transition
- [ ] **No repeated transitions** - Don't use the same transition word twice in a row
- [ ] **Transitions at sentence start** - Not buried mid-sentence
- [ ] **Varied subjects** - Rotate between "Teams", "The process", "Leaders", "Companies", etc.
- [ ] **Mix of sentence types** - Include questions and imperatives for variety

---

## COMMON PROBLEMATIC PATTERNS TO WATCH

| Pattern | Why It Fails | Quick Fix |
|---------|--------------|-----------|
| "The... The... The..." | Same word repetition | Add transitions, change subjects |
| "This... This..." | Demonstrative pronoun repetition | Restructure with different subjects |
| "It... It..." | Pronoun repetition | Name the actual subject |
| "They... They..." | Pronoun repetition | Use company/team names |
| "We... We..." | First person repetition | Vary with transitions |
| Long stretch without transitions | Below 35% threshold | Insert "Furthermore", "Additionally", etc. |
| Mid-sentence transitions | Doesn't count for Yoast | Move transition to sentence start |

---

## IMPLEMENTATION NOTES

When using this guide with AI content generation:

1. **Reference this document** in your prompt by URL or include key sections
2. **Request explicit verification** that both rules pass before content submission
3. **Ask for the calculation** of transition word percentage in the response
4. **Request a first-word list** to verify no consecutive matches

**Sample prompt addition:**
```
Before submitting, verify:
1. List the first word of every sentence and confirm no two adjacent words match
2. Calculate transition word percentage: [X sentences with transitions] / [Y total sentences] = [Z%]
3. Confirm Z ≥ 35%
```
