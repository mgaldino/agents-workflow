# Editorial Letter -- Formal Model Review

**Manuscript**: "War and Responsibility" by M. Patrick Hulme
**Journal**: *American Political Science Review* (2026) 120, 1, 267-290
**References**: Thomson (1999), Board & Meyer-ter-Vehn (2018), Dixit (2015), Varian (1997/2016)

## Decision: Accept

## Consolidated Scores

| Dimension             | Score | Rating    |
|-----------------------|-------|-----------|
| Model Design          | 8/10  | Very Good |
| Technical Presentation| 7/10  | Good      |
| Exposition            | 8/10  | Very Good |
| **Global**            | 8/10  | **Very Good** |

## Editorial Synthesis

This is a strong paper that develops a formal model of the U.S. war powers to explain a genuine empirical puzzle: why have full-scale wars always been undertaken with formal congressional authorization since Korea, while smaller uses of force are routinely conducted unilaterally? The central mechanism -- "Loss Responsibility Costs" (LRCs), i.e., the ex post political costs imposed on a president who uses force and fails -- is cleanly isolated and generates counterintuitive implications, most notably that congressional influence is *stronger* when the president acts unilaterally, not weaker. The model is well-crafted and parsimonious, building from a simple baseline (Model I: unilateral action) to a richer extension (Model II: with formal authorization) and then to incomplete information. The empirical section, featuring novel "Congressional Support Scores" from floor speeches, provides compelling evidence consistent with the model's predictions. The main weakness lies in certain simplifying assumptions (e.g., that formal authorization fully eliminates LRCs, the absent judiciary) that, while defensible, could be more carefully discussed. The technical presentation is generally solid but could benefit from tighter notation management and more formal statement of results. The exposition is excellent -- the paper reads like a well-structured talk, gets to the point quickly, and effectively communicates the key insights.

## Hierarchy Applied: Design > Presentation > Exposition

The design of this model is its greatest strength. The paper identifies a genuinely important puzzle, isolates a clean mechanism (LRCs modulated by congressional sentiment and authorization status), and generates rich comparative statics and testable hypotheses. Because the design is strong, investment in polishing the technical presentation and exposition is well justified. The design is not the bottleneck here; the marginal improvements lie in tightening the technical exposition of the model (particularly the notation and formal statement of results) and in being more explicit about the limitations of key assumptions.

## Priorities for Revision (if applicable)

1. **Strengthen the discussion of the assumption that formal authorization fully eliminates LRCs**: This is arguably the strongest assumption in the model and the paper would benefit from a more sustained discussion of when this might not hold (e.g., the Iraq War AUMF did not fully insulate Bush 43 from political costs).
2. **Tighten notation and formal result statements**: Some results are stated as hypotheses rather than formal propositions. Consider presenting the key equilibrium characterizations as numbered Propositions with clear conditions.
3. **Discuss the role of Congress's policy preferences more explicitly**: The assumption that Congress would "rather not approve the use of force even if it supports the military intervention from a policy perspective" deserves more nuance -- hawks in Congress sometimes actively want authorization to signal resolve.
4. **Address the potential endogeneity of congressional sentiment**: The empirical section measures pre-intervention sentiment, but sentiment itself may be shaped by anticipated presidential action.

## Strategic Recommendation to the Author

This paper has already been accepted at the APSR, which reflects its substantial quality. The model design is strong: it addresses a first-order question in American politics and international relations with a parsimonious and well-motivated formal framework. The mechanism is novel, the insights are transferable, and the empirical evidence is compelling. The suggestions above are primarily refinements that could strengthen future iterations or related work. The paper represents a successful example of integrating formal theory with rich qualitative and quantitative evidence in the study of domestic constraints on the use of force.

---

## Full Report -- Model Design

# Model Design Report (Dixit / Varian / Board)

## Score: 8/10

## The model in one sentence

A crisis bargaining model in which the U.S. president's exposure to "Loss Responsibility Costs" -- ex post political penalties for using force that ends in failure, scaled by the level of force employed and inversely by congressional sentiment -- constrains the scale of unilateral military action and creates incentives to seek formal congressional authorization for the largest uses of force.

## Type of contribution (Board & Meyer-ter-Vehn)

**New lens on established puzzle + new force isolated**: The paper takes the well-known puzzle of the "imperial presidency" in the war powers context and reframes it through the lens of LRCs, a concept the author distinguishes from Fearon's audience costs. The contribution is primarily a new model (new lens) that isolates a previously unformalized political force -- blame avoidance incentives in the war powers -- and generates novel testable predictions. There is also an empirical contribution (novel Congressional Support Scores data).

## Evaluation by Dimension

### MD1. Quality of the Question [Excellent]

The paper addresses a first-order puzzle in American politics: why do presidents consistently seek formal authorization for full-scale wars but routinely act unilaterally for smaller uses of force? This puzzle has motivated decades of debate between "imperial presidency" proponents and skeptics of congressional influence. The question is comprehensible to non-specialists (anyone who follows U.S. politics can grasp the tension). The paper clearly articulates *why* the reader should care: the answer has implications for democratic accountability, separation of powers, and the practical conduct of U.S. foreign policy. The empirical puzzle is vividly illustrated in Figure 1, which immediately hooks the reader. This is a textbook example of Dixit's "big puzzle" criterion and Varian's "look for ideas in the world" advice.

### MD2. Simplicity and KISS [Excellent]

The model is admirably parsimonious. Model I requires only three actors (President, Adversary State, Congress as a passive influence through beta), a simple Tullock contest function for probability of victory, linear payoffs, and a single new parameter (k, the LRC scaling factor). The Schelling-Spence test is clearly passed: if we remove the LRC term, the key results disappear -- the president would no longer be constrained by congressional sentiment when acting unilaterally, and the distinction between authorized and unauthorized force collapses. Model II extends Model I by adding exactly one new decision (Ask/Not Ask for the president) and one new player decision (Grant/Not Grant for Congress), plus one new parameter (a, the cost of asking). The incomplete information extension adds one element of uncertainty (adversary's cost of fighting). The entire model is presentable in under 4 pages. This is well within Board's guideline.

### MD3. Mechanism Isolation [Excellent]

The central mechanism -- LRCs as a constraint on presidential use of force, modulated by congressional sentiment and authorization status -- is cleanly isolated. The model is reduced to the minimum structure needed: a crisis bargaining framework (the standard shell) plus the LRC innovation. Congress's role is modeled as an exogenous sentiment parameter (beta) in Model I, which is the simplest possible representation. In Model II, Congress becomes an active player but only with a binary choice (Grant/Not Grant). The key insight -- that congressional influence is *strongest* when the president acts unilaterally, because LRC exposure is highest -- emerges directly from the mechanism and would not emerge without it. The paper explicitly distinguishes LRCs from audience costs (Figure 2), further sharpening the mechanism.

### MD4. Richness of Insights [Rich]

The model generates multiple insights beyond the initial puzzle:
- **Counterintuitive result 1**: Congressional sentiment is a *stronger* constraint when the president acts unilaterally (the opposite of what "imperial presidency" proponents argue).
- **Counterintuitive result 2**: Unilateral action is often evidence of congressional *influence*, not its absence -- Congress free-rides on the president's willingness to act alone for smaller threats.
- **Necessary condition in kind**: Full-scale wars will only occur with formal authorization (Hypothesis 2a).
- **Necessary condition in degree**: Congressional sentiment caps the force a president will deploy even unilaterally (Hypothesis 1).
- **Congress does not always grant authorization** in the incomplete information model, creating genuine risk of war.
- **The president only seeks authorization when he expects it to be granted**, explaining the high success rate of AUMF requests.
- **Transferability**: The LRC concept is transferable to other contexts where leaders face ex post accountability for policy failures (not just military).

### MD5. Type of Contribution [Strong]

- **New question**: Not entirely new (the war powers debate is old), but a new *formalization* of the question.
- **New model (new lens)**: Yes -- LRCs as distinct from audience costs, and the interplay between authorization status and constraint.
- **Important application**: Yes -- U.S. war powers is a central topic.
- **Isolated political force**: Yes -- blame avoidance in the war powers context.
- **New empirical predictions**: Yes -- necessary conditions in kind and degree, testable with the novel Congressional Support Scores.
- **Technical contribution**: Modest -- the game-theoretic machinery is standard (crisis bargaining with Tullock contest), but applied in a novel way.

### MD6. Construction Process [Mature]

The model shows clear signs of iteration and refinement:
- Builds from simple (Model I) to complex (Model II with authorization, then incomplete information).
- Uses concrete examples throughout (Korea, Vietnam, Iraq, Syria, Panama, ISIS).
- The baseline model (complete information) is solved before introducing incomplete information.
- Comparative statics are presented with clear figures (Figures 4, 6, 7).
- The incomplete information extension is well-motivated (to generate actual risk of war, which is necessary for Congress's authorization decision to be non-trivial).
- The empirical section follows naturally from the model's predictions.
- The paper reads as a mature product of sustained intellectual engagement, not a first draft.

## Overall Design Verdict

This is a well-designed model that attacks a first-order puzzle in American politics with an elegant and parsimonious formal framework. The mechanism (LRCs) is cleanly isolated, the insights are rich and often counterintuitive, and the model generates clear testable predictions that the author then evaluates with novel data. The design is the paper's strongest asset.

## Constructive Suggestions

1. **Relax the assumption that formal authorization fully eliminates LRCs**: Consider a partial insulation version where authorization reduces but does not eliminate LRCs. This would add realism (presidents with AUMFs still face political costs, as Bush 43 discovered with Iraq) and could generate additional comparative statics.
2. **Consider endogenizing the cost of asking (a)**: Currently a is exogenous, but it likely varies with political context (e.g., unified vs. divided government). Making a a function of political conditions could generate additional predictions.
3. **Discuss the model's implications for the War Powers Resolution more explicitly**: The model assumes the WPR is irrelevant, but discussing *why* the model predicts this (and whether the WPR could become relevant under modified assumptions) would strengthen the institutional analysis.
4. **Consider a brief discussion of how the model applies outside the U.S. context**: Parliamentary systems have different war powers dynamics, and discussing how LRCs would operate differently could broaden the paper's appeal.

---

## Full Report -- Technical Presentation

# Technical Presentation Report (Thomson / Board)

## Score: 7/10

## Model Structure

**Players**: President (P), Adversary State (S_2), Congress (C -- passive in Model I, active in Model II). **Actions**: P offers deal d in [0,1]; S_2 accepts or rejects; if rejected, P chooses force f in [0,F]; in Model II, P first chooses Ask/Not Ask, then C chooses Grant/Not Grant. **Information**: Complete in Models I and II (baseline); incomplete in extension (S_2's cost of fighting c is private). **Preferences**: P values object at 1, bears fighting cost sf, and LRC kf/beta upon defeat; C values object at beta, bears fighting cost sf (when authorized); S_2 values object at 1, bears fighting cost c. **Timing**: Sequential (see extensive form in Figures 3 and 5). **Equilibrium concept**: Subgame Perfect Equilibrium (complete info); Bayesian Perfect Equilibrium (incomplete info).

## Scorecard

| Dimension | Verdict | Comment |
|-----------|---------|---------|
| D2. Model Presentation | Adequate | Clear baseline + extensions structure; game tree figures help considerably |
| D3. Notation | Adequate | Generally clear but some choices could be more mnemonic |
| D4. Definitions | Needs Improvement | LRCs defined informally; key concepts lack formal definition blocks |
| D5. Statement of Results | Needs Improvement | Results stated as "Hypotheses" rather than Propositions/Theorems |
| D6. Proofs | Adequate | Relegated to appendix; main text provides good intuition |
| D7. Figures and Diagrams | Excellent | Game trees (Figs 3, 5), comparative statics plots (Figs 4, 6, 7), and empirical figures (Figs 8, 9) are all effective |
| D8. Assumptions and Logical Structure | Adequate | Assumptions clearly listed and motivated, though some deserve more scrutiny |
| D9. Examples and Applications | Excellent | Rich historical examples woven throughout |

## Detailed Analysis

### D4. Definitions [Needs Improvement]

**Diagnosis**: The central concept of "Loss Responsibility Costs" is defined informally in the text and contrasted with audience costs in Figure 2, but it never receives a formal definition with typographic emphasis. The mathematical form (kf/beta) appears in the payoff section but is not given as a standalone definition. Similarly, key terms like "Congressional Support Score," "necessary condition in kind," and "necessary condition in degree" are used but not formally defined.

**Impact**: The reader must piece together the exact definition of LRCs from scattered textual descriptions. For a concept that is the paper's central innovation, this is a missed opportunity.

**Suggestion**: Provide a boxed or bolded Definition of LRCs early in the paper, specifying both the verbal content and the mathematical form. Follow Thomson's advice: "Be unambiguous when you define a new term."

**Reference**: Thomson (1999), Section 4.

### D5. Statement of Results [Needs Improvement]

**Diagnosis**: The paper's formal results are stated as "Hypothesis 1," "Hypothesis 2a," and "Hypothesis 2b." While this framing makes sense for the empirical testing that follows, it obscures the formal results *of the model*. The key equilibrium characterizations -- e.g., the optimal force level f* as a function of parameters, the conditions under which the president seeks authorization, the conditions under which Congress grants it -- are embedded in the text rather than stated as numbered Propositions.

**Impact**: A reader looking for the model's main results cannot quickly locate them. The "Hypothesis" framing blurs the line between what the model *proves* and what the paper *tests*. Board recommends the sequence: "Define p. Define q. Theorem: Every p is q." Here, the model's results are stated more discursively.

**Suggestion**: Add formal Propositions for the key equilibrium results (e.g., Proposition 1: characterization of f* in Model I; Proposition 2: equilibrium of Model II under complete information; Proposition 3: equilibrium of the incomplete information game). Then derive the Hypotheses as empirical implications of these Propositions.

**Reference**: Board & Meyer-ter-Vehn (2018), Section on "Results."

### D3. Notation

**Diagnosis**: Most notation is reasonable (P for President, S_2 for adversary, d for deal, f for force, beta for congressional sentiment). However, some choices are less mnemonic: k for the LRC scaling parameter is arbitrary; using both s (cost sensitivity) and c (adversary's fighting cost) requires the reader to remember which cost belongs to whom. The paper uses beta both as a parameter (congressional sentiment) and as part of Congress's valuation of the object -- the dual role is explained but requires close attention.

**Impact**: Minor. The notation is functional but not optimally guessable (Thomson's criterion).

**Suggestion**: Consider renaming k to something more suggestive (e.g., lambda for "loss" or rho for "responsibility"). Ensure each parameter's mnemonic link is explicit when introduced.

**Reference**: Thomson (1999), Section 3: "The best notation is notation that can be guessed."

## Notation Inventory

| Symbol | Meaning | Introduced | Used in | Problem? |
|--------|---------|------------|---------|----------|
| P | President | p. 273 (Model I) | Throughout | No |
| S_2 | Adversary State | p. 273 | Throughout | Mildly confusing subscript (why 2?) |
| C | Congress | p. 273 | Model II | No |
| d | Deal offered | p. 273 | Throughout | No |
| f | Force employed | p. 273 | Throughout | No |
| F | Maximum force | p. 273 | Throughout | No |
| t | Adversary power | p. 273 | Throughout | No |
| p | Probability of victory (f/(f+t)) | p. 273 | Throughout | Overloaded with P (President) |
| beta | Congressional sentiment | p. 273 | Throughout | Also Congress's object valuation |
| s | Cost sensitivity | p. 273 | Throughout | No |
| c | Adversary's fighting cost | p. 273, 277 | Incomplete info | No |
| k | LRC scaling parameter | p. 274 | Throughout | Not mnemonic |
| a | Cost of asking for authorization | p. 275 | Model II | No |
| c-bar | Upper bound of c distribution | p. 277 | Incomplete info | No |

## Result-by-Result Analysis

### Hypothesis 1 (Necessary condition in degree)

- **Statement**: Sentiment in Congress toward the use of force serves as a constraint on the maximum scale of force presidents utilize.
- **Formal basis**: Derived from Model I comparative statics (df*/dbeta > 0, with f* having a ceiling).
- **Takeaway**: Clear and compelling. Congressional sentiment caps presidential force even absent formal authorization.
- **Board format compliance**: Stated as a testable hypothesis rather than a formal proposition -- effective for the empirical section but obscures the formal result.

### Hypothesis 2a (Necessary condition in kind)

- **Statement**: The largest uses of force (full-scale wars) will only be undertaken pursuant to formal authorization from Congress.
- **Formal basis**: Derived from Model II comparison of f* (unilateral) vs. f* (with AUMF).
- **Takeaway**: Clear, important, and well-supported by the historical record.

### Hypothesis 2b (Smaller uses of force undertaken unilaterally)

- **Statement**: Smaller uses of force will be undertaken unilaterally (even when Congress informally supports the use of force).
- **Formal basis**: Derived from Congress's incentive to avoid going "on the record" for smaller threats.
- **Takeaway**: Important complement to 2a -- explains why unilateral action is the norm for smaller interventions.

## Constructive Suggestions

1. **Add formal Propositions** for the equilibrium characterizations of each model variant. Then derive the Hypotheses as empirical corollaries. This would sharpen the distinction between formal results and testable predictions. (Board)
2. **Provide a formal Definition block for LRCs** with both verbal and mathematical content, set off typographically. (Thomson, Section 4)
3. **Rename the probability of victory variable** from p to something that does not collide with the President label P. A common choice is pi or w (for "win"). (Thomson, Section 3)
4. **Add a brief proof sketch** in the main text for the key comparative static (df*/dbeta > 0), even if the full proof is in the appendix. The reader should see the mathematical intuition, not just the verbal one. (Thomson, Section 5)
5. **Consider adding a summary table** of the three model variants (Model I, Model II complete info, Model II incomplete info) showing players, actions, information, and key results side by side.

---

## Full Report -- Exposition

# Exposition Report (Varian / Thomson / Board)

## Score: 8/10

## Evaluation by Dimension

### ME1. Structure of the Paper [Excellent]

The paper follows a clean logical structure: Introduction (puzzle + preview of argument) --> Literature Review ("The Debated Imperial Presidency," "Loss Responsibility Costs") --> Model (Model I --> Model II --> Incomplete Information) --> Empirical Assessment --> Discussion --> Conclusion. The main theoretical results are presented by approximately page 12-13 of the 24-page article (Hypotheses 1 and 2a/2b), comfortably within Board's "before page 15" guideline. The paper gets to the point quickly: the first two paragraphs of the introduction present the puzzle, and by the end of the first page the reader knows the central argument. The baseline model (Model I) is fully solved before extensions are introduced. The flow from theory to empirics is natural and well-signposted.

### ME2. Introduction [Excellent]

The introduction is a model of clarity. It opens with the puzzle (unilateral force is common; full-scale wars always get authorization -- why?), states the argument (LRCs make presidents highly reticent to undertake major conflict unilaterally), previews the two contributions (theoretical model + novel empirical evidence), and positions the paper within the literature. The Kennedy epigraph ("Defeat is an orphan") elegantly encapsulates the mechanism. The introduction does not suffer from excessive "throat-clearing" about the importance of the topic; it trusts the reader to recognize that war powers are important. The structure follows Varian's prescription: puzzle --> model and intuition --> literature. The contribution is clear within the first three paragraphs. There is no "laundry list" of implications.

### ME3. Writing and Style [Very Good]

The writing is generally clear, direct, and well-paced. Sentences are of reasonable length. Technical terms are used correctly. The paper does not begin sentences with symbols. Voice and tense are consistent. Footnotes are used judiciously and contain substantive information (not tangential digressions). The paper makes effective use of historical quotations from presidents, legislators, and advisors to illustrate the mechanism, which enlivens the prose considerably.

**Minor issues**:
- Some passages in the model section could be more concise. The verbal explanations of the game tree mechanics (pp. 273-274) are thorough but occasionally redundant given the clarity of Figure 3.
- The term "Loss Responsibility Costs" is somewhat cumbersome. While the author has chosen this terminology deliberately (to distinguish from audience costs), the acronym "LRCs" is used heavily and the reader must remember what it stands for.
- The literature review sections (pp. 269-272) are comprehensive but could be tightened. Some of this material could be relegated to footnotes.

### ME4. Length and When to Stop [Adequate]

At 24 pages (pp. 267-290), the paper is a standard-length APSR article. The theoretical model occupies approximately 7 pages (pp. 272-279), which is appropriate. The empirical section is about 8 pages (pp. 279-287). The paper includes several tables of qualitative evidence (Tables 2-5) that are valuable but collectively take up significant space. Proofs are appropriately placed in appendices. The main text does not contain extensive mathematical derivations. The paper could have been marginally tighter in the literature review and transition sections, but overall the length is justified by the combination of formal theory and empirical evidence.

### ME5. Use of Examples and Intuition [Excellent]

This is where the paper truly excels. The author weaves historical examples throughout -- not just in the empirical section but in the theory section as well. Key examples include:
- **Truman and Korea**: The founding puzzle (unilateral full-scale war, massive political fallout).
- **LBJ and the Gulf of Tonkin Resolution**: Illustrates why presidents seek formal authorization ("only if Congress was in on the takeoff would it take responsibility for any 'crash landing'").
- **Bush 41 and the Gulf War**: Sought formal approval so lawmakers could not "paint their asses white and run with the antelopes."
- **Obama and Syria 2013**: Illustrates the "negative case" -- deterrence by lack of authorization.
- **Panama 1989 and ISIS 2014**: Congress pushes for action while refusing to formally authorize -- perfect illustration of congressional free-riding.
- **J. William Fulbright**: Quoted to illustrate the counterintuitive result that congressional constraint is *strongest* under unilateral action.

Each major theoretical result is accompanied by intuition stated in plain English. The comparative statics are illustrated with clear figures (Figures 4, 6, 7). The scatter plot in Figure 9 is particularly effective at visualizing the "necessary condition in degree" prediction.

## Overall Exposition Verdict

The exposition is a major strength of this paper. It follows best practices from Varian, Thomson, and Board almost textbook-style: the introduction hooks the reader immediately, the model is presented clearly with helpful game-tree figures, results are accompanied by plain-English intuition, and historical examples are woven throughout to ground the theory in reality. The paper reads like a well-structured talk. The main areas for improvement are marginal: tightening the literature review, adding formal Proposition statements for the model's results, and minor notation improvements.

## Top 5 Suggestions for Improvement

1. **Restructure the model results as formal Propositions, not just Hypotheses**: The current framing blurs the line between what the model proves and what the paper tests. Add Propositions for the equilibrium characterizations, then derive the Hypotheses as empirical implications. This would make the paper's formal contribution more visible and easier to cite.

2. **Tighten the literature review**: The sections "The Debated Imperial Presidency" and "Loss Responsibility Costs" (pp. 269-272) are thorough but could be condensed by approximately one page without loss of content. Some of the more detailed engagement with individual works could move to footnotes.

3. **Add a formal Definition block for LRCs**: As the paper's central concept, LRCs deserve a clear, typographically distinct definition. Currently the concept is introduced gradually across several paragraphs; a single crisp definition early on (with subsequent elaboration) would help.

4. **Consider a brief "Model Summary" table**: After the incomplete information model, a one-page table comparing the three model variants (Model I, Model II complete, Model II incomplete) -- with players, actions, information, key results, and hypotheses generated -- would provide a useful reference for the reader.

5. **Address potential endogeneity of congressional sentiment earlier**: The paper measures pre-intervention sentiment, but a sophisticated reader will immediately wonder whether sentiment is shaped by anticipated presidential action. Addressing this concern in the model section (not just the empirical section) would preempt the objection.
