# Formal Model Review: "War and Responsibility"

**Author:** M. Patrick Hulme (Stanford University)
**Venue:** *American Political Science Review* (2026) 120, 1, 267--290
**Reviewer Role:** Senior reviewer, top political science journal
**Date of Review:** March 13, 2026

---

## I. Summary of the Paper

This article develops a formal model of the U.S. war powers to explain a striking empirical regularity: since the Korean War, full-scale wars have only been initiated with formal congressional authorization (an AUMF), while smaller uses of force are virtually always undertaken unilaterally by the president. The paper argues this pattern is driven by "Loss Responsibility Costs" (LRCs)---political penalties imposed on a president by domestic audiences when the president uses force and the intervention ends poorly. Because presidents bear LRCs most heavily when acting without congressional cover, they are deterred from undertaking large-scale conflict unilaterally. For smaller operations, Congress itself prefers to free-ride on the president's unilateral authority, avoiding a vote to preserve blame-avoidance options. The paper presents two models (unilateral action and action with possible formal authorization), extends the latter to incomplete information, derives testable hypotheses framed as necessary conditions, and provides novel empirical evidence including a new dataset of "Congressional Support Scores" based on floor speeches.

---

## II. Evaluation of the Formal Model

### A. Research Question and Importance (Score: 9/10)

The paper addresses a genuinely important and under-theorized puzzle in American politics and international relations: why do presidents consistently seek formal authorization for large wars but act unilaterally for smaller operations? This question sits at the intersection of two major literatures---American political institutions (the "imperial presidency" debate) and international crisis bargaining---and the paper rightly notes that prior work has failed to connect these streams in a satisfying way. The puzzle is empirically well-motivated: Figure 1, showing U.S. combat fatalities by authorization status since 1898, is an immediately compelling visualization that makes the question vivid for the reader. The normative stakes are high (democratic accountability over the use of military force), and the answer has clear policy implications. The only reason this does not receive a perfect score is that the core insight---that blame avoidance drives congressional behavior in the war powers context---has been articulated informally by prior scholars (Schultz 2003; Ely 1995; Weaver 1986), so the contribution is more one of formalization and integration than of entirely novel theoretical intuition.

### B. Model Design and Parsimony (Score: 8/10)

The model is admirably parsimonious. The author builds incrementally: Model I (unilateral action only) strips the game to its bare essentials---a take-it-or-leave-it crisis bargaining game between the president and an adversary state, with the key innovation being LRCs as a function of force employed and congressional sentiment. Model II then layers on the possibility of seeking an AUMF. This sequential construction is pedagogically effective and analytically clean.

**Strengths:**

- The use of the Tullock contest success function (p = f/(f+t)) is a natural and well-established choice for modeling probabilistic conflict outcomes, and it keeps the analysis tractable.
- The LRC specification---kf/beta, where the penalty is proportional to force and inversely proportional to congressional sentiment---is simple, intuitive, and captures the key mechanism economically.
- The distinction between LRCs and audience costs (Figure 2) is clarifying and theoretically important: LRCs are about using force and failing, while ACs are about threatening force and not following through.
- The assumption that Congress prefers to avoid voting (blame avoidance) is well-grounded in the empirical literature.

**Weaknesses and Concerns:**

1. **Congress as a unitary actor.** The model treats Congress (C) as a single player with a single preference parameter beta. In reality, Congress is a collective body with heterogeneous preferences, and the decision to grant an AUMF is itself a complex legislative process. The author acknowledges this simplification but does not explore whether heterogeneity in Congress (e.g., partisan divisions, hawkish vs. dovish factions) would substantively alter the results. A brief discussion or extension addressing this would strengthen the contribution.

2. **The exogeneity of beta.** Congressional sentiment (beta) is treated as an exogenous parameter, but in practice, it is likely influenced by the president's own actions (framing, intelligence briefings, rally-round-the-flag effects). The model cannot speak to strategic manipulation of sentiment by the president, which is empirically important.

3. **The binary nature of authorization.** Formal authorization fully eliminates LRCs in the model. This is a strong assumption. In practice, even with an AUMF, presidents can face significant political costs if a war goes badly (consider Bush 43 and Iraq post-2005). The model could benefit from allowing authorization to *reduce* rather than fully eliminate LRC exposure, which would likely preserve the qualitative results while being more realistic.

4. **No role for the adversary's strategic response to authorization status.** The adversary (S2) does not condition its behavior on whether the president has secured an AUMF. In reality, adversaries may interpret authorization as a signal of resolve (as the author's own discussion of the incentive-rearranging role of AUMFs suggests). This is partially addressed in the incomplete information extension, but deserves more explicit treatment.

### C. Mechanism Isolation (Score: 9/10)

This is one of the paper's strongest features. The LRC mechanism is clearly isolated and its implications are carefully traced. The model demonstrates precisely how LRCs create a wedge between unilateral and authorized force levels (Figure 6 is particularly effective), and how this wedge increases with adversary power. The step from Model I to Model II cleanly shows how the possibility of authorization changes the strategic calculus. The incomplete information extension adds an important wrinkle---a real risk of war---that makes Congress's authorization decision non-trivial. The hypotheses are stated as necessary conditions, which is both theoretically appropriate (the model predicts constraint, not precise point predictions) and methodologically sophisticated.

---

## III. Technical Presentation

### A. Notation and Definitions (Score: 7/10)

The notation is mostly clear and consistent, but there are some areas that could be tightened:

1. **Player labeling:** The adversary state is labeled S2, which is functional but somewhat arbitrary. More substantively, the president is sometimes denoted P and sometimes referred to generically as "the executive." Consistency would help.

2. **The parameter space:** Key parameters (s, t, c, k, beta, a, F, c-bar) are introduced across several pages. A single summary table of parameters and their interpretations would greatly aid the reader, especially given that the proofs are relegated to the supplementary material.

3. **The cost of fighting for the president (sf) vs. the cost for S2 (c):** These are specified quite differently---one is proportional to force used, the other is a fixed parameter. The asymmetry is not strongly motivated beyond tractability. Why does the adversary not also face force-dependent fighting costs?

4. **Boundary conditions:** The paper occasionally notes parameter restrictions (e.g., beta > 0, interior solutions holding) in footnotes. These conditions deserve more prominent treatment, perhaps in a formal assumption block.

### B. Proofs and Derivations (Score: 6/10)

The proofs are entirely relegated to Appendix I of the Supplementary Material, which is standard for APSR but makes independent verification difficult for the reader of the main text. The paper does provide intuitive descriptions of the solution process, which is appropriate for the venue. However:

1. **The main text contains no formal propositions or theorems.** The results are stated as "Hypotheses" (1, 2a, 2b), which blends the theoretical predictions with their empirical operationalization. It would strengthen the paper to separate these: state formal results (propositions) derived from the model, and then separately discuss their empirical operationalization as hypotheses.

2. **The complete information result that Congress always authorizes** is somewhat obvious once stated (zero probability of war means no downside for Congress), and the author acknowledges this. The real theoretical action is in the incomplete information model, but this receives comparatively less space in the main text.

3. **The incomplete information model's solution** is described in only one paragraph. The Bayesian Perfect Equilibrium concept is invoked but the structure of beliefs and updating is not discussed. For a paper published in the discipline's flagship journal, more detail on the equilibrium characterization---even if the full derivation is in the appendix---would be appropriate.

4. **Comparative statics** are presented graphically (Figures 4, 6, 7) rather than analytically. While the figures are clear and effective, stating at least the key comparative statics results as formal claims (with signs of relevant partial derivatives) would strengthen the technical presentation.

### C. Figures (Score: 8/10)

The figures are generally well-designed and serve the paper effectively.

- **Figure 1** (uses of force by authorization status) is excellent---immediately compelling and well-labeled.
- **Figure 2** (AC vs. LRC distinction) is a clean, simple table that clarifies an important conceptual point.
- **Figure 3** (extensive form of Model I) is clear and follows standard conventions.
- **Figure 4** (force as a function of beta) effectively illustrates the key comparative static from Model I.
- **Figure 5** (extensive form of Model II) is necessarily complex but well-organized with the three subgames side by side.
- **Figure 6** (unilateral vs. AUMF force levels) is one of the most informative figures---the divergence between the curves as adversary power increases powerfully illustrates the mechanism.
- **Figure 7** (equilibrium force and authorization status) adds the equilibrium selection overlay to Figure 6, and the use of darkened vs. light lines to indicate observed behavior is clever.
- **Figure 8** (expected scatter plot pattern for necessary condition in degree) is a useful pedagogical device.
- **Figure 9** (the actual scatter plot) is the empirical centerpiece and is well-constructed, though dense. The use of dot size for crises not involving combat is a nice touch.

Minor suggestions: Figure 7 is arguably too dense and might benefit from being split into two panels. The parameter values used in the numerical illustrations (footnotes 18, 21, 26) should be discussed more systematically---are the qualitative patterns robust to parameter changes?

---

## IV. Exposition and Communication

### A. Paper Structure (Score: 8/10)

The paper follows a logical and effective structure:

1. Motivating puzzle (with Figure 1)
2. Literature review ("The Debated Imperial Presidency")
3. Conceptual discussion of LRCs
4. Formal model (Models I and II, plus incomplete information extension)
5. Empirical assessment
6. Conclusion

This is well-organized. The literature review is thorough without being exhaustive, and the conceptual discussion of LRCs effectively motivates the formal assumptions before they appear. The transition from theory to empirics is smooth. One structural suggestion: the section on "Factors Influencing the President's Exposure to Loss Responsibility Costs" (pp. 271--272) and "An Indispensable Role for Formal Authorization from Congress" (p. 272) could be tightened---some of this material repeats points made earlier or previews model results in informal language that is then repeated more precisely in the model section.

### B. Introduction and Motivation (Score: 9/10)

The introduction is strong. The opening paragraph immediately establishes the puzzle and stakes. The Kennedy epigraph is apt. The empirical puzzle is clearly stated: why have full-scale wars only been authorized while smaller uses of force are consistently unilateral? The abstract effectively previews the argument. The introduction also does a good job of signaling both the theoretical and empirical contributions. The only weakness is that the introduction could more explicitly preview the model's key mechanism in one crisp sentence before moving to the literature review.

### C. Writing Style (Score: 8/10)

The writing is clear, professional, and generally well-suited to the APSR audience. The author effectively uses historical examples (Johnson and the Gulf of Tonkin, Bush 41 and the Gulf War, Obama and Syria) to motivate and illustrate theoretical points. The Fulbright quote on p. 275 is particularly effective. Technical material is presented accessibly without sacrificing precision. A few minor points:

- Some paragraphs in the model section could be shorter. The paper occasionally belabors points that the model has already made precisely.
- The term "Loss Responsibility Costs" is somewhat cumbersome. While it accurately describes the concept, a shorter label might have aided readability (though at this point the term is established in the published version).
- The paper does well at explaining the model to a non-technical audience, which is important for APSR's broad readership.

### D. Use of Examples and Empirical Evidence (Score: 9/10)

This is a notable strength. The paper does not merely present a model and gesture at reality; it provides substantial empirical evidence organized around the necessary condition framework. The positive cases (Table 2), negative cases (Table 3), and the detailed discussion of cases like Panama, ISIS, Korea, Syria, and others are rich and persuasive. Table 4 (unilateral uses often cited as evidence of imperial presidency) is a particularly effective rhetorical device, showing that these cases actually had informal congressional support. Table 5 (negative cases of deterrence) is also compelling. The Congressional Support Scores, while novel data, are introduced somewhat briskly in the main text (the details are in Supplementary Material Appendix II). Given their novelty and importance, a few more sentences describing the methodology in the main text would be warranted.

---

## V. Overall Assessment

### Scores Summary

| Dimension | Score (1--10) |
|---|---|
| Research Question and Importance | 9 |
| Model Design and Parsimony | 8 |
| Mechanism Isolation | 9 |
| Notation and Definitions | 7 |
| Proofs and Derivations | 6 |
| Figures | 8 |
| Paper Structure | 8 |
| Introduction and Motivation | 9 |
| Writing Style | 8 |
| Use of Examples and Evidence | 9 |
| **Overall** | **8.1** |

### Overall Evaluation

This is a strong paper that makes a genuine contribution to our understanding of the war powers and executive-legislative relations in the United States. Its central insight---that Loss Responsibility Costs create an incentive structure in which presidents are de facto constrained by congressional sentiment even (indeed, especially) when acting unilaterally, and that this explains the pattern of authorization for large wars and unilateral action for smaller operations---is important and well-articulated. The formal model is parsimonious, the mechanism is clearly isolated, the empirical evidence is unusually rich for a formal theory paper, and the writing is accessible. The paper successfully bridges the American politics and international security literatures in a way that has been called for but rarely achieved.

The main weaknesses are in the technical presentation: proofs are entirely off-loaded to supplementary material, formal results are not stated as propositions separate from empirical hypotheses, the incomplete information model deserves more space, and several modeling choices (unitary Congress, exogenous sentiment, full elimination of LRCs under authorization) merit more thorough discussion or robustness analysis. The notation, while functional, could be presented more systematically.

### Principal Constructive Suggestions

1. **Separate propositions from hypotheses.** State the model's formal results as numbered propositions with clear conditions, then discuss their empirical operationalization separately as hypotheses. This is standard in formal theory papers and would strengthen the contribution.

2. **Expand discussion of the incomplete information model.** This is where the most interesting theoretical action occurs (Congress faces a real trade-off, the president strategically decides whether to seek authorization). It deserves at least another page of treatment, including a clearer statement of the equilibrium structure.

3. **Add a parameter table.** A single table summarizing all parameters, their interpretations, and any restrictions would significantly aid readability.

4. **Discuss robustness to modeling assumptions.** Specifically: (a) What happens if authorization reduces but does not eliminate LRCs? (b) How would heterogeneous congressional preferences affect the results? (c) What if the adversary conditions its acceptance decision on authorization status?

5. **Strengthen the connection between model and data.** The Congressional Support Scores are a valuable innovation, but the link between the model's beta parameter and the empirical measure could be drawn more explicitly. What does the model predict about the functional form of the relationship between sentiment and force levels? Can this be tested more precisely than through necessary condition analysis?

6. **Consider endogenizing congressional sentiment.** Even a brief extension or discussion addressing how a president might strategically influence beta (through framing, intelligence sharing, or rally effects) would address an obvious objection and potentially yield additional insights.

7. **Engage more explicitly with Schultz (1998).** The relationship to Schultz's domestic opposition and signaling model is discussed in footnotes but deserves more central treatment, as it is the closest formal antecedent. How exactly do the models differ in structure and predictions?

### Verdict

This paper merits publication in a top journal. Its combination of a clearly motivated puzzle, a parsimonious formal model that isolates a compelling mechanism, and unusually rich empirical evidence for a formal theory paper represents an important contribution. The weaknesses identified above are addressable and do not undermine the core argument. The paper offers an alternative to the imperial presidency narrative that is both more theoretically coherent and more empirically supported, and it should generate productive debate in both the American politics and international security literatures. Its publication in APSR is well-deserved.
