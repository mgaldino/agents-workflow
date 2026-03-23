# Editorial Letter -- Formal Model Review

**Manuscript**: "The best at the top? Candidate ranking strategies under closed list proportional representation"
**Authors**: Benoit S. Y. Crutzen, Hideo Konishi, and Nicolas Sahuguet
**Journal**: Political Science Research and Methods (2024), 12, 706-728

**References**: Thomson (1999), Board & Meyer-ter-Vehn (2018), Dixit (2015), Varian (1997/2016)

## Decision: R&R minor

## Consolidated Scores

| Dimension             | Score | Rating       |
|-----------------------|-------|--------------|
| Model Design          | 7/10  | Good         |
| Technical Presentation| 7/10  | Good         |
| Exposition            | 7/10  | Good         |
| **Global**            | **7/10** | **Good**  |

## Editorial Synthesis

This paper addresses a genuine and empirically relevant puzzle: why do parties under closed-list proportional representation not always place their most competent candidates at the top of the list? The authors develop a game-theoretic model of electoral competition framed as a team contest, where candidates choose campaign effort and parties strategically rank candidates on their list. The central insight -- that effort incentives are hump-shaped across list positions, peaking around the expected seat share rather than at the top -- is novel and counterintuitive. The model is well-constructed, building on Crutzen et al. (2020) with meaningful extensions (candidate heterogeneity, exposure effects, rank-dependent benefits, multi-party competition). The technical execution is solid, with clear propositions and proofs relegated appropriately to the appendix. The exposition is professional and well-structured for a published article.

The principal strength of the paper lies in the clean identification of the tension between competence-based ranking and incentive-based ranking, and the derivation of explicit conditions under which each prevails. The principal weakness is that the model's extensions (Sections 5.2-5.5) are treated somewhat additively -- each modifying one feature at a time -- rather than building toward a unified, richer framework. This makes the paper feel more like a catalogue of comparative statics than a deep exploration of a single, rich mechanism.

## Hierarchy Applied: Design > Presentation > Exposition

The design of the model is the paper's strongest asset: the puzzle is real, the mechanism is clearly isolated, and the baseline model is parsimonious. The design is strong enough to justify the paper's existence and merits publication. The technical presentation is competent but not exceptional -- notation is generally clear, though the proliferation of superscripts and subscripts (particularly with the "mj" notation) creates visual clutter. The exposition is adequate and follows standard conventions, but the introduction could be tighter. Because the design is solid, investing in improving the presentation and exposition would yield meaningful returns. Design is not the bottleneck here.

## Priorities for Revision (if applicable)

1. **Tighten the connection between extensions**: The paper currently treats candidate exposure (5.2), rank-dependent benefits (5.3), incumbency (5.4), and number of parties (5.5) as independent modifications. A brief discussion of how these forces interact -- or an acknowledgment of when they reinforce vs. counteract each other -- would substantially strengthen the contribution.

2. **Sharpen the introduction**: The current introduction takes nearly 3 pages before arriving at the model's key insight. A restructured introduction that leads with the counterintuitive result (best candidates not at the top) and then explains the mechanism would be more compelling.

3. **Strengthen the welfare discussion**: Section 5.6 acknowledges the difficulty of welfare analysis but is too brief. Given the tension between party-optimal ranking (for electoral success) and voter-optimal ranking (for competent representation), even a partial welfare characterization would add significant value.

4. **Add a worked numerical example early**: Before the general model, a simple 3-candidate, 3-seat example showing the incentive hump would dramatically improve accessibility and follow Varian's advice to "work an example first."

5. **Clarify the regularity condition's economic content**: Assumption 1 (gamma < 1/n) is presented technically but its economic meaning -- that the contest is sufficiently noisy -- deserves more intuitive discussion.

## Strategic Recommendation to the Author

This is a solid paper that has already been published in a good field journal (PSRM). The model design is clean, the puzzle is genuine, and the results are interesting. For future extensions or related work, the authors should consider: (a) endogenizing party objectives beyond pure seat maximization, (b) exploring the interaction effects between the various extensions rather than treating them additively, and (c) developing the welfare implications more fully. The core mechanism -- effort incentives peaking at marginal seats creating a tension with competence-based ranking -- is a genuinely useful insight for the literature on electoral systems and candidate selection.

---

## Full Report -- Model Design

# Model Design Report (Dixit / Varian / Board)

## Score: 7/10

## The model in one sentence

A game-theoretic model of closed-list PR elections where parties rank heterogeneous candidates on a list, candidates exert costly campaign effort in a team Tullock contest, and the party's optimal ranking strategy trades off competence-based ordering against effort-incentive maximization driven by hump-shaped incentives across list positions.

## Type of contribution (Board & Meyer-ter-Vehn)

**New lens on existing question + isolation of a political force**. The question of how parties rank candidates is not new, but the model provides a novel mechanism (effort incentives from a team contest structure) that yields the counterintuitive prediction that the most competent candidates should be placed at the expected seat share position rather than at the top. This complements Buisseret et al. (2022), who derive a similar ranking prediction through a pure competence/voting channel without incentives.

## Evaluation by dimension

### MD1. Quality of the question [Excellent]

The question emerges from a genuine empirical puzzle: parties in closed-list PR systems are empirically observed to rank candidates in decreasing order of competence (Cox et al. 2021, Buisseret et al. 2022), yet the standard incentive logic suggests this may not be optimal because top-of-list positions are "safe" and create weak effort incentives. The paper explicitly motivates this with a real-world anecdote from Belgian politics (the Sophie Wilmes/Hadja Lahbib case). The question is accessible to non-specialists: "Should parties put their best candidates at the top of the list?" is immediately understandable. The paper clearly answers why the reader should care: the quality of elected representatives depends on how parties resolve this competence-incentive trade-off.

### MD2. Simplicity and KISS [Adequate]

The baseline model (Section 3-4) is admirably parsimonious: two parties, n candidates per party, quadratic effort costs, Tullock contest, binomial seat distribution. The model can be stated in under 4 pages. However, the paper then introduces five separate extensions (W payoff, exposure weights, rank-dependent benefits, incumbency, multi-party), each modifying one element at a time. While each extension is simple individually, the cumulative effect is that the paper addresses many questions rather than one deeply. The Schelling-Spence test is partially satisfied: the hump-shaped incentive structure disappears if you remove the contest structure or the heterogeneity in effort costs, confirming that these are essential components. The exposure weights and rank-dependent benefits feel like additional ingredients rather than consequences of the core mechanism.

### MD3. Mechanism isolation [Adequate]

The core mechanism -- effort incentives peak at the marginal seat position because that is where a candidate's effort has the highest marginal impact on winning an additional seat -- is clearly isolated in the baseline model (Proposition 3). The structure is minimal: two parties suffice, and the Tullock contest provides a clean reduced-form for electoral competition. However, the mechanism is partially obscured by the subsequent extensions, which introduce additional forces (media exposure, office benefits) that operate through different channels. The paper would benefit from a clearer statement of which extensions reinforce vs. counteract the baseline mechanism.

### MD4. Richness of insights [Adequate]

The model generates several interesting insights: (1) the "expected seat share hypothesis" -- best candidates placed at the expected seat share position, not at the top; (2) rank-independent benefits (ideology, W) do not affect optimal ranking -- a clean invariance result; (3) candidate exposure can reverse the baseline prediction and lead to competence-based ranking; (4) rank-dependent office benefits can also restore competence-based ranking for top positions; (5) popular parties are more likely to rank by competence. These are genuine insights, several are counterintuitive (especially 1 and 2), and some generate testable predictions. However, the comparative statics are mostly of the threshold variety (when is condition X satisfied?) rather than revealing deeper trade-offs.

### MD5. Type of contribution [New lens + empirical predictions]

The paper offers a new theoretical lens (team contest with heterogeneous candidates) on an existing empirical question (how parties rank candidates). It isolates a specific political force (effort incentive structure from contest competition). It generates novel empirical predictions (expected seat share hypothesis, popular parties more likely to rank by competence). The contribution is incremental rather than transformative -- it extends Crutzen et al. (2020) and complements Buisseret et al. (2022) -- but it is a meaningful addition.

### MD6. Construction process [Mature]

The paper shows clear signs of iteration and refinement: (a) it builds explicitly on the authors' own prior work (Crutzen et al. 2020); (b) the baseline-then-extensions structure suggests systematic exploration; (c) the symmetric equilibrium case (p = 1/2) is used effectively as a workhorse example before general results; (d) Figures 1-4 provide helpful illustrations of the key mechanisms. The construction follows Varian's advice to start simple and generalize. The paper could have pushed harder on working a concrete numerical example before the general model, but the overall construction is mature.

## Overall verdict on design

The model design is solid. The question is excellent -- genuine, empirically motivated, and accessible. The baseline mechanism is clean and the core insight (hump-shaped incentives) is novel and counterintuitive. The main weakness is the additive extension structure: the paper addresses many variations of the question rather than going deep on one. This breadth is not a fatal flaw -- each extension is motivated by real institutional features -- but it prevents the paper from achieving the depth of insight that comes from fully exploring a single mechanism. The design is strong enough to support a good publication in a field journal.

## Constructive suggestions

1. **Integrate extensions into a unified framework**: Rather than treating exposure, office benefits, incumbency, and multi-party as separate modifications, consider a unified model that nests all of them and derive conditions for competence-based ranking in that general environment.

2. **Lead with a concrete example**: Before the general model, present a 3-candidate example (e.g., n=3, one seat expected) that demonstrates the hump-shaped incentive structure and the counterintuitive ranking result. This would follow Varian's "work an example first" advice.

3. **Deepen the seat share hypothesis**: The expected seat share hypothesis is the paper's signature result. Consider exploring its robustness more deeply -- what happens with asymmetric parties? With correlated seat outcomes? -- rather than adding independent extensions.

4. **Clarify the relationship to Buisseret et al. (2022)**: Both papers predict that parties may rank by competence but through completely different mechanisms (incentives vs. voter calculus). A deeper comparison of when each mechanism dominates would sharpen the contribution.

---

## Full Report -- Technical Presentation

# Technical Presentation Report (Thomson / Board)

## Score: 7/10

## Model structure

**Players**: Two parties (j = 1, 2) each with n candidates; party leadership (designs the list) and candidates (choose effort). **Actions**: Party leadership assigns candidates to list positions (mapping alpha_j); candidates choose effort levels e_ij >= 0. **Information**: Complete information (candidates know the list, their costs, and the contest structure). **Preferences**: Candidates maximize expected benefits minus effort costs; party leadership maximizes expected seats. **Timing**: t=1 nomination (party ranks candidates), t=2 campaign (effort choice), t=3 election (seats allocated). **Equilibrium concept**: Subgame perfect Nash equilibrium, solved by backward induction.

## Scorecard

| Dimension | Verdict | Comment |
|-----------|---------|---------|
| D2. Model presentation | Adequate | Canonical order followed; baseline under 4 pages; extensions well-separated |
| D3. Notation | Needs improvement | Heavy subscript/superscript load; "mj" notation creates visual clutter |
| D4. Definitions | Adequate | Key objects defined clearly; some implicit definitions could be more explicit |
| D5. Statement of results | Adequate | Propositions clearly stated; some could benefit from sharper takeaway messages |
| D6. Proofs | Adequate | Appropriately placed in appendix; good ratio of math to natural language |
| D7. Figures and diagrams | Adequate | Four informative figures; labels could be more descriptive |
| D8. Assumptions and logical structure | Adequate | Assumption 1 clearly stated; role well-explained; regularity condition derived |
| D9. Examples and applications | Needs improvement | Symmetric case (p=1/2) used well; more concrete numerical examples needed |

## Detailed analysis

### D3. Notation [Needs improvement]

**Diagnosis**: The notation carries a heavy load of subscripts and superscripts. The central objects involve double subscripts (e_mj for effort of candidate in position m of party j, c_mj for cost), and several key quantities stack multiple super/subscripts: M_j^m, M_j^{maj}, P_j^k, C_k^n, Lambda_j^m. The "mj" subscript convention, where m is the position and j is the party, is workable but creates visual density. Additionally, alpha_j denotes both the list mapping and (via alpha_j(m) = i) the assignment of candidate i to position m, which requires careful parsing.

**Impact**: The notation is functional but not guessable (Thomson's criterion). A reader encountering M_j^{maj} for the first time cannot guess its meaning. The stacking of indices makes equations like (1) and (2) visually demanding.

**Suggestion**: Consider reducing the index load where possible. When working in the symmetric case (which is the primary illustration), the j subscript could be dropped. Introduce mnemonic abbreviations: e.g., use "Seats(m)" instead of M_j^m for "marginal impact of winning m seats." Define key composite objects (like Lambda_j^m) with memorable names.

**Reference**: Thomson (1999), Section 3: "The best notation is notation that can be guessed."

### D9. Examples and applications [Needs improvement]

**Diagnosis**: The paper uses the symmetric equilibrium (p_1 = p_2 = 1/2) as its main illustration, which is effective. Figures 1-4 provide geometric intuition. However, there is no worked numerical example with specific candidate costs, effort levels, and ranking outcomes. The reader never sees the mechanism operate with concrete numbers.

**Impact**: The absence of a concrete example forces the reader to build intuition entirely from the general formulas and the figures. A simple example (e.g., 3 candidates, specific costs c_1 < c_2 < c_3, expected 1 seat) showing how effort levels and incentives map to the optimal ranking would make the key insight immediately tangible.

**Suggestion**: Add a worked example with n = 3 or n = 5 candidates, specific quadratic cost parameters, and trace through: (a) equilibrium efforts for a given list order, (b) the party's electoral output under different orderings, (c) the optimal list. This follows Varian's advice: "Start by looking at examples... The simplest case is usually enough."

**Reference**: Varian (1997/2016): "Work an example"; Thomson (1999), Section 4: use examples to illustrate definitions.

## Notation inventory

| Symbol | Meaning | Introduced | Used through | Issue? |
|--------|---------|-----------|-------------|--------|
| n | Number of legislative seats (odd) and candidates per party | p.710 | Throughout | Dual role (seats = candidates) could confuse |
| e_ij | Effort of candidate i in party j | p.710 | Throughout | Standard |
| c_ij | Marginal cost of effort | p.710 | Throughout | Standard |
| K(e_mj) | Quadratic effort cost = (1/2)c_mj * e_mj^2 | p.710 | Throughout | OK |
| alpha_j | List mapping (position to candidate) | p.710 | Section 3-4 | Functional notation requires care |
| m_j | Position of candidate i (= alpha_j(m) = i) | p.710 | Throughout | Introduced via alpha |
| a_m | Media/exposure weight for position m | p.710 | Throughout | OK, a_1 = 1 normalized |
| E_j | Party j's electoral output | p.710 | Throughout | OK |
| p_j | Tullock winning probability per seat | p.711 | Throughout | OK |
| gamma | Return to scale parameter | p.711 | Throughout | OK |
| P_j^k | Probability of winning exactly k seats | p.711 | Throughout | Binomial, clear |
| V | Benefit of being elected | p.711 | Throughout | OK |
| W | Rank-independent winning benefit | p.711 | Sections 3, 5.1 | OK |
| W_m | Rank-dependent winning benefit | p.711 | Sections 3, 5.3 | Dual W and W_m potentially confusing |
| w_m | Rank-dependent private payoff | p.711 | Sections 3, 5.3 | w vs W distinction subtle |
| k^C | Number of top brass candidates | p.711 | Sections 3, 5.3 | OK |
| k^{maj} | Majority threshold = (n+1)/2 | p.712 | Throughout | OK |
| B_mj | Benefit function for candidate at position m, party j | p.712 | Throughout | OK |
| M_j^m | Weight = sum_{k=m}^{n} mu_j^k | p.712-713 | Throughout | Not immediately guessable |
| M_j^{maj} | Weight for majority = k^{maj} * C_{k^{maj}}^n * p^{k^{maj}} * (1-p)^{n-k^{maj}+1} | p.712 | Throughout | Heavy notation |
| Lambda_j^m | Implicit incentive function | p.714 | Section 4.2 onward | Central object, name not mnemonic |

## Result-by-result analysis

| Result | Type | Statement clarity | Takeaway | Proof location |
|--------|------|-------------------|----------|----------------|
| Prop 1 | Existence/characterization | Clear | Unique Nash equilibrium of campaign stage exists; effort proportional to incentives/cost ratio | Appendix |
| Prop 2 | Optimality | Clear | Optimal list assigns low-cost candidates to high-incentive positions | Appendix |
| Prop 3 | Characterization (baseline) | Clear | **Key result**: Best candidate placed at expected seat share position, not at top | Appendix |
| Prop 4 | Invariance | Clear | W does not affect ranking -- clean result | Appendix |
| Prop 5 | Sufficient condition | Adequate | Exposure declining fast enough implies competence-based ranking | Appendix |
| Prop 6 | Sufficient condition | Adequate | Office benefits large enough implies competence-based ranking for top k^C | Appendix |

**Takeaway messages**: Propositions 3 and 4 have the clearest takeaway messages. Proposition 3's "expected seat share hypothesis" is memorable and the paper correctly highlights it. Proposition 4's invariance result is clean and surprising. Propositions 5 and 6 are stated as sufficient conditions and their takeaways are less sharp -- they say "if X is large enough, then Y" without characterizing the threshold's economic magnitude.

## Constructive suggestions

1. **Reduce notational density**: Introduce mnemonic names for key composite objects (M_j^m, Lambda_j^m). When working in the symmetric case, drop the j subscript. Consider a notation table early in the paper.

2. **Add a worked numerical example**: A concrete example with specific parameter values would dramatically improve accessibility. Place it after Proposition 3 to illustrate the expected seat share hypothesis.

3. **Sharpen takeaway messages for Propositions 5 and 6**: Instead of "if exposure weights decline fast enough," quantify: "the list leader must receive at least X times the exposure of the second-ranked candidate." Figure 2 helps but the text should state the quantitative implication more directly.

4. **Clarify the dual use of W and w_m**: The benefit W (rank-independent, all candidates) and w_m (rank-dependent, top candidates) serve different roles but have similar notation. Consider renaming one (e.g., W -> Omega for ideological benefit, keeping w_m for office perks).

5. **Add axis labels to figures**: Figure 1's y-axis is labeled "y" and x-axis "x" rather than "Incentive (Lambda_m)" and "List position (m)." Same for Figures 3-4. Figure 2 is better labeled but could be more explicit.

---

## Full Report -- Exposition

# Exposition Report (Varian / Thomson / Board)

## Score: 7/10

## Evaluation by dimension

### ME1. Structure of the paper [Adequate]

The paper follows a conventional structure: Introduction (Section 1, ~3 pages), Related Literature (Section 2, ~2 pages), Model (Section 3, ~3 pages), Solving the Model (Section 4, ~2 pages), Optimal List with extensions (Section 5, ~8 pages), Conclusion (Section 6, ~1 page), Appendix (~5 pages). The logical flow is correct: Model -> Equilibrium efforts -> Optimal list (baseline) -> Extensions -> Conclusion. The baseline result (Proposition 3, the expected seat share hypothesis) appears on page 715, which satisfies Board's criterion of "main result before page 15." However, the introduction takes nearly 3 full pages before arriving at the model's setup, spending considerable space on institutional context and motivation. The baseline is resolved before extensions, which is good practice.

### ME2. Introduction [Needs improvement]

The introduction has several strengths: it identifies the puzzle clearly (paragraph 2: parties may not place best candidates at top), it connects to empirical evidence (Cox et al. 2021, Buisseret et al. 2022), and it previews all main results. However, it suffers from being too long and too front-loaded with context. The first paragraph spends 6 lines on the general importance of candidate selection before narrowing to closed-list PR. The preview of results takes over a full page (from "The collective efforts..." on p.707 through the end of the intro on p.709), reading somewhat like a laundry list of findings across the extensions. By Board's standard -- "If you really know what your paper is about, you shouldn't find it hard to explain this in a couple of paragraphs" -- the introduction could be tightened significantly. The core contribution (effort incentives are hump-shaped, creating a tension with competence-based ranking) could be stated in 2-3 paragraphs, with the extensions briefly mentioned rather than individually summarized.

### ME3. Writing and style [Adequate]

The writing is professional and generally clear. Sentences are of moderate length -- not excessively long but not always short either. The paper does not begin sentences with mathematical symbols (a common error caught by Thomson). Technical terms are used correctly (Tullock contest, binomial distribution, backward induction, Nash equilibrium). Voice and tense are consistent. The paper is reasonably succinct -- at 23 pages including appendix and references, it is within standard bounds. Proofs are appropriately placed in the appendix (following Varian's "put the tedious stuff in the appendix"). Footnotes are used with moderate frequency (14 in the main text) -- some could be integrated into the text (e.g., footnotes 8 and 9 contain substantive modeling choices that deserve main-text discussion).

### ME4. Length and when to stop [Adequate]

The paper is 23 pages total, with the main text spanning pages 706-723 (18 pages of content) and the appendix spanning pages 724-728 (5 pages). The core model and baseline result occupy about 10 pages (Sections 3-5.1), which is lean. The extensions (Sections 5.2-5.5) add about 7 pages, and each makes a distinct point. The welfare discussion (Section 5.6) is very brief (~0.5 pages) and acknowledges its own limitations -- this is honest and appropriate. The conclusion is concise (1 page). Overall, the paper does not overstay its welcome. The main risk is that the extensions section, taken as a whole, may dilute the impact of the baseline result by spreading the reader's attention across many variations. Following Varian's "once you've made your point, stop" and "quality average > sum," the paper might be stronger if one or two extensions were cut or relegated to supplementary material.

### ME5. Use of examples and intuition [Adequate]

The paper provides intuition after each formal result, which is good practice. The Belgian political anecdote (Sophie Wilmes/Hadja Lahbib) is an effective motivating example in Section 5.3. Figures 1-4 provide geometric intuition for the hump-shaped incentive structure and the effects of various parameters. The symmetric equilibrium (p = 1/2, n = 21) serves as a running example. However, the paper lacks a concrete numerical example that walks through the mechanism step by step with specific parameter values. Board's dictum -- "Every result should be explained in simple English unless it is obvious or technical" -- is mostly satisfied, but some results (particularly Propositions 5 and 6 with their sufficient conditions involving ratios of exposure weights and office benefits) would benefit from more concrete illustration. The paper does not use geometric examples (Thomson's preference for geometric over numerical examples) except through the figures.

## Overall verdict on exposition

The exposition is professional and follows standard conventions for a published article in a good field journal. The paper's structure is logical, the writing is clear, and the proofs are appropriately placed. The main areas for improvement are: (1) the introduction should be tightened to convey the core insight more quickly and avoid the laundry-list summary of extensions; (2) a worked numerical example early in the paper would dramatically improve accessibility; (3) the figures should have more descriptive axis labels. The exposition does not hinder the paper's contribution but also does not elevate it -- with tighter communication, the paper's genuinely interesting insights would land with greater force.

## Top 5 suggestions for improvement

1. **Restructure the introduction around the core insight**: Lead with the counterintuitive result ("Contrary to intuition, parties should not place their best candidates at the top of the list") in the first paragraph, then explain why (hump-shaped incentives from team contest). Move the detailed preview of extensions to a "plan of the paper" paragraph at the end of the introduction. Currently, the reader must process 2+ pages of context and results summary before understanding the paper's key mechanism. (Board: "Get to the point.")

2. **Add a concrete worked example after Proposition 3**: Present a simple case -- say n = 5 candidates, two parties, specific cost parameters (c_1 = 1, c_2 = 2, c_3 = 3, c_4 = 4, c_5 = 5) -- and trace through the equilibrium to show: (a) the hump-shaped incentive function, (b) the optimal list placing the best candidate at position 3 (the expected seat share). This would make the expected seat share hypothesis viscerally clear. (Varian: "Start by looking at examples.")

3. **Improve figure labels**: Replace generic "x" and "y" axis labels in Figures 1, 3, and 4 with substantive labels (e.g., "List position m" and "Equilibrium effort incentive Lambda_m"). Add brief captions explaining what the reader should observe in each figure. Currently, the captions are minimal (e.g., "Effort incentives and list rank") and the figures require reading the surrounding text to interpret.

4. **Integrate key footnotes into the main text**: Footnotes 8 (party popularity weight rho) and 9 (concavity vs. Assumption 1) contain substantive modeling choices. These should be in the main text, ideally near the relevant model components, so the reader understands these choices are deliberate. (Thomson: footnotes should contain genuinely parenthetical material.)

5. **Tighten the transition from baseline to extensions**: After Proposition 3, add a brief roadmap paragraph: "Proposition 3 establishes that, in the baseline model, parties do not rank candidates in decreasing order of competence. We now investigate four institutional features that may restore competence-based ranking: candidate exposure (5.2), rank-dependent office benefits (5.3), incumbency (5.4), and multiparty competition (5.5)." This would frame the extensions as a coherent investigation rather than a sequence of modifications.
