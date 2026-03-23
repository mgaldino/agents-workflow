# Referee Report: "The Best at the Top? Candidate Ranking Strategies under Closed List Proportional Representation"

**Authors:** Benoit S. Y. Crutzen, Hideo Konishi, and Nicolas Sahuguet
**Journal:** Political Science Research and Methods (2024), 12, 706-728
**Reviewer Role:** Senior reviewer for a top political science methods journal
**Date of Review:** March 13, 2026

---

## 1. Summary

This paper develops a game-theoretic model of candidate ranking on party lists under closed-list proportional representation (PR). Two parties each field *n* candidates who differ in competence (modeled as heterogeneous effort costs). Parties rank candidates on their list to maximize electoral success; candidates then choose costly campaign effort. The election is modeled as a team contest (generalized Tullock) where parties' outputs determine seat allocation via a binomial distribution. The paper identifies four sources of incentives for candidates: (i) the prospect of winning a legislative seat, (ii) rank-independent ideological/party benefits, (iii) candidate exposure effects (media, voter attention), and (iv) rank-dependent benefits tied to high offices. The central finding is that incentives are bell-shaped across list positions, peaking at "hot spots" near the party's expected seat share -- not at the top of the list. This means parties do not generally place their best candidates at the top. The paper then derives conditions under which descending-competence ordering becomes optimal: sufficiently steep candidate exposure decay, or sufficiently large rank-dependent benefits for top candidates.

---

## 2. Quality and Design of the Formal Model

**Score: 7/10**

### Importance of the Question

The question addressed -- how should parties rank candidates on closed lists when both competence and incentives matter? -- is genuinely important. Closed-list PR is used in a large number of democracies, and the composition of party lists directly determines the quality of elected legislators. The paper tackles a meaningful puzzle: if top positions are "safe seats," why would parties place their best candidates there, given that safe seats provide weak effort incentives? This tension between competence-based sorting and incentive provision is well-motivated and policy-relevant.

### Parsimony

The baseline model is admirably parsimonious. The core ingredients -- heterogeneous effort costs, quadratic cost functions, a Tullock contest, binomial seat allocation -- are standard and well-chosen. The model isolates the incentive channel cleanly in the baseline (Section 5.1) before layering on additional mechanisms (exposure, rank-dependent payoffs, incumbency, multi-party). This modular structure is a strength.

However, parsimony is somewhat compromised as the paper progresses. The model accumulates several layers: candidate exposure weights (*a_m*), rank-dependent private payoffs (*w_m*), majority-related payoffs (*W*), ideological payoffs (*W*), political capital stocks (*x_mj*), and the number of parties (*J*). While each extension is individually motivated, the cumulative effect is a model with many moving parts, and the paper sometimes reads more like a catalog of comparative statics than a unified theoretical argument.

### Mechanism Isolation

The paper's greatest theoretical contribution is the identification of the bell-shaped incentive function and the "expected seat share hypothesis" (Proposition 3). This is a clean, novel insight: the most competent candidate should be placed not at the top of the list but at the position corresponding to the party's expected seat share. The mechanism is clearly isolated and well-explained.

The subsequent results on when descending-competence ordering is optimal (Propositions 5 and 6) are also valuable, though the conditions are somewhat complex and harder to build intuition around. The condition in Proposition 5, involving ratios of exposure weights, is technically precise but not immediately transparent.

### Concerns

1. **Symmetry assumption as workhorse:** Much of the intuition and all of the figures rely on the symmetric equilibrium (*p_1 = p_2 = 1/2*). While the authors note that results hold more generally, the asymmetric case is largely unexplored. Given that parties of different sizes and popularity are the norm, this is a limitation.

2. **The Tullock contest function:** The choice of a generalized Tullock contest to model elections is convenient but debatable for proportional representation systems. In PR, votes translate more or less proportionally into seats -- the Tullock function introduces a "noise" parameter (gamma) that does substantial work. The restriction gamma < 1/n (Assumption 1) is quite strong for large legislatures and deserves more discussion of its substantive implications.

3. **Independence of seat probabilities:** The assumption that seat-winning probabilities are independent (binomial distribution) is strong. In reality, winning seat *k* makes winning seat *k+1* neither more nor less likely only under specific conditions. The authors should discuss how correlated seat outcomes might affect the bell-shaped incentive structure.

4. **Party objective function:** Parties maximize the number of seats won. This is a natural assumption, but the paper acknowledges (Section 5.6) that voter welfare might diverge from party objectives. A brief discussion of whether the optimal list from a welfare perspective differs from the party-optimal list would strengthen the contribution.

---

## 3. Technical Presentation

**Score: 8/10**

### Notation and Definitions

The notation is generally clear and consistent throughout the paper. Key objects are well-defined:
- Cost functions *K(e_mj) = (1/2) c_mj e_mj^2*
- Party output *E_j = sum a_m e_mj*
- Winning probability *p_j* via the Tullock contest
- Binomial seat allocation *P_j^k*
- Benefit function *B_mj*
- Implicit incentive function *Lambda_j^m*

The use of double subscripts (*mj* for position *m* on party *j*'s list) is initially confusing, particularly because *m* refers to a list position and *i* to a candidate identity, with the mapping *alpha_j* connecting them. The notation *c_mj* (the cost of the candidate in position *m* on party *j*'s list) conflates position and identity in a way that requires careful reading.

### Propositions and Proofs

The paper contains six propositions and several supporting lemmas. The propositions are clearly stated and logically ordered. The proof structure is sound:

- **Proposition 1** (equilibrium existence and characterization) is the technical backbone. The proof in the Appendix is detailed and rigorous, covering first-order conditions, second-order conditions, existence (via Brouwer's fixed point theorem), and uniqueness (via the regularity condition).

- **Proposition 2** (optimal list follows the implicit incentive function) is established via comparative statics. The proof is elegant in its simplicity -- changing a cost parameter changes effort and output in the same direction under the regularity condition.

- **Propositions 3-6** are applications of Proposition 2 to specific parameter configurations. The proofs are concise and correct.

One technical concern: the regularity condition *gamma(p_{-j} eta_j + p_j eta_{-j}) < 1* is introduced in the Appendix but plays a crucial role. Its economic interpretation -- that aggregate effort elasticity is bounded -- deserves more prominence in the main text.

### Figures

The four figures are well-chosen and effectively illustrate the key results:
- Figure 1 (bell-shaped incentive curve) is the paper's most important visual and clearly conveys the core insight.
- Figure 2 (exposure weight ratio condition) effectively illustrates Proposition 5.
- Figures 3 and 4 (effect of large vs. small *w_m*) nicely show how rank-dependent payoffs shift the incentive curve.

However, the figures could be improved:
- Axis labels are minimal ("x" and "y" in Figures 1, 3, 4). More descriptive labels ("List rank" and "Incentive Lambda_j^m") would aid readability.
- No figure illustrates the asymmetric case, which would help readers understand how the results change when parties differ.

---

## 4. Exposition and Communication

**Score: 7/10**

### Paper Structure

The paper follows a logical structure: Introduction -> Related Literature -> Model -> Solving the Model -> Optimal List (with subsections for each extension) -> Conclusion. This is appropriate and well-organized. The backward induction solution approach (campaign stage first, then nomination stage) is natural and clearly presented.

The modular structure of Section 5 -- starting with the simplest case (5.1) and progressively adding complications (exposure in 5.2, rank-dependent payoffs in 5.3, incumbency in 5.4, multiple parties in 5.5) -- is pedagogically effective.

### Introduction

The introduction is solid but somewhat lengthy (approximately 3 pages). It previews all results, which is helpful for orientation but reduces the sense of discovery when reading the analysis. The motivating example from Belgian politics (the Chardon interview) is a nice touch but could be more tightly integrated. The introduction would benefit from a clearer statement of the paper's single most important takeaway early on.

### Writing Style

The writing is generally clear and professional. Technical exposition is precise without being overly formal. The authors do a good job of providing intuition alongside formal results.

Areas for improvement:
1. **Redundancy:** Several key points are made multiple times (e.g., the bell-shaped nature of incentives is explained in the introduction, in Section 4.2, in Section 5.1, and again in the conclusion). Some consolidation would tighten the paper.
2. **Passive constructions:** The paper occasionally relies on passive voice where active voice would be clearer (e.g., "It is established that..." rather than "We establish that...").
3. **Transition between sections:** The connections between the various extensions in Section 5 could be made more explicit. Currently, each subsection is somewhat self-contained, and the reader may lose sight of the overall argument.

### Use of Examples

The paper makes effective use of real-world examples, particularly:
- The Belgian anecdotes (Chardon interview, the Sophie Wilmes/Hadja Lahbib case) effectively motivate the rank-dependent benefits extension.
- The Irish constitutional requirement that ministers be parliament members nicely illustrates institutional reasons for rank-competence alignment.

The paper could benefit from a more extended numerical example walking through the full model solution for a small case (e.g., n = 5 candidates, 2 parties), showing explicitly how the list is constructed.

---

## 5. Additional Substantive Comments

### Strengths

1. **Novel and counterintuitive baseline result:** The expected seat share hypothesis (Proposition 3) is a genuinely novel contribution that challenges the naive intuition that parties should always place their best candidates at the top.

2. **Empirical relevance:** The paper engages seriously with empirical evidence (Cox et al. 2021, Buisseret et al. 2022) and derives testable predictions. The conditions for descending-competence ordering (Propositions 5 and 6) can, in principle, be taken to data.

3. **Relationship to the literature:** The paper positions itself well relative to Buisseret et al. (2022), which derives a similar prediction (marginal rank hypothesis) but through a pure selection mechanism without incentives. The complementarity between the two approaches is clearly articulated.

4. **Solid technical execution:** The proofs are rigorous, the equilibrium analysis is thorough, and the regularity conditions are carefully derived.

### Weaknesses

1. **Limited welfare analysis:** Section 5.6 acknowledges that welfare analysis is difficult in this framework but does not go far enough. The tension between party-optimal and voter-optimal lists is the most policy-relevant aspect of the paper and deserves more attention, even if only through discussion.

2. **No empirical application or calibration:** While the paper is purely theoretical, a simple calibration exercise -- using real data on candidate exposure, party seat shares, etc. -- would greatly enhance the paper's impact. What do the conditions in Propositions 5 and 6 imply quantitatively for real-world party lists?

3. **Binary party competition:** The two-party baseline is limiting. Section 5.5 extends to *J* parties but only briefly. Given that most closed-list PR systems feature multi-party competition, this extension deserves fuller treatment.

4. **Static model:** The model is a one-shot game. In practice, candidate ranking involves repeated interactions, reputation building, and dynamic career concerns. Acknowledging this limitation more explicitly and discussing how dynamics might alter the results would be valuable.

5. **Candidates as homogeneous in all but cost:** Candidates differ only in their effort cost parameter *c_ij*. In reality, candidates may also differ in their "baseline appeal" or quality in ways not captured by effort cost. The incumbency extension (Section 5.4) partially addresses this through political capital *x_mj*, but this dimension could be developed further.

---

## 6. Minor Issues

1. Page 710: The assumption of quadratic costs (footnote 7) is motivated by tractability. It would be helpful to note briefly whether the main results (especially the bell-shaped incentive function) survive under more general convex cost functions.

2. Page 711: Assumption 1 (gamma < 1/n) becomes very restrictive for large *n*. For a 150-seat legislature with two parties fielding 150 candidates each, this requires gamma < 1/150. What does this mean substantively for the level of electoral noise?

3. Page 714: The implicit incentive function Lambda_j^m is the paper's key analytical object, but it is introduced somewhat abruptly. A more gradual derivation with intuition at each step would help.

4. Page 715: Proposition 3 states the expected seat share hypothesis for the case W = w_m = 0 and a_i = 1. The conditions are quite restrictive. The paper should discuss more explicitly how robust this result is to small perturbations.

5. Page 721: The extension to J > 2 parties replaces the majority-winning payoff with expected seat share proportional payoffs. This is a meaningful change in the model's structure and deserves more discussion of its implications.

6. The paper does not discuss the possibility of multiple equilibria beyond establishing uniqueness under the regularity condition. What happens when the regularity condition is violated?

---

## 7. Scores Summary

| Dimension | Score (1-10) | Comments |
|-----------|:---:|---------|
| **Quality and Design of the Formal Model** | 7 | Important question, clean baseline mechanism, but accumulation of extensions dilutes focus |
| **Technical Presentation** | 8 | Rigorous proofs, clear notation (with minor issues), effective figures |
| **Exposition and Communication** | 7 | Well-structured, good use of examples, but somewhat redundant and introduction too long |
| **Overall Assessment** | **7.5** | A solid, well-executed theory paper that makes a genuine contribution to understanding candidate ranking under closed-list PR |

---

## 8. Overall Assessment

This is a competent and interesting formal theory paper published in a strong field journal (PSRM). The central contribution -- the bell-shaped incentive structure and the expected seat share hypothesis -- is novel, clearly derived, and empirically relevant. The paper makes a genuine advance in understanding the strategic logic behind party list construction under closed-list proportional representation.

The model is well-designed in its baseline form, and the progressive extension structure is pedagogically effective. The technical execution is rigorous. The main limitations are: (1) the accumulation of extensions gives the paper a somewhat encyclopedic quality at the expense of a single sharp narrative; (2) the welfare implications are underdeveloped; and (3) the model's quantitative implications for real-world party lists remain unexplored.

The paper would benefit from: (a) tightening the introduction and reducing redundancy throughout; (b) developing a simple numerical/calibration example; (c) expanding the welfare discussion; and (d) improving figure labeling. These are suggestions for refinement rather than fundamental objections -- the paper's core contribution is sound and the analysis is correctly executed.

**Recommendation:** This paper merits publication in a top political science methods journal. It represents a meaningful contribution to the formal theory of electoral institutions and candidate selection.
