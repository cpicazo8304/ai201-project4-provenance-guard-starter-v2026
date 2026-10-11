# Acceptance criteria — Provenance Guard

Five criteria that say what "working" means for this service, written in unit 7
**before** you built it.

**All five are yours.** None are given.

An acceptance criterion names a number or something plainly observable. *"The
detector is accurate"* is an opinion — and perfect AI detection isn't possible
anyway, so it's an opinion about something nobody can deliver. *"Of 10 pieces I
wrote myself, at most 1 is labelled high-confidence AI"* is a criterion.

Under each, write a sentence or two on **why that target**. *"I allow at most 1
false positive in 10 because on a writing site a wrong accusation costs more
than a missed detection"* is a real answer.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

**Cover at least three of these five areas.** They're prompts, not a form.

| Area | A question it could answer |
|---|---|
| False positives | How often may a human's writing get called AI? |
| Score spread | How far apart should clearly-AI and clearly-human text score? |
| Label coverage | Is every one of your three labels actually reachable? |
| The appeal path | Does an appeal always change status and always get recorded? |
| Bad input | What happens when `text` is missing, empty, or enormous? |

Two things worth knowing before you pick numbers:

- **The expensive mistake is one-sided.** Missing some AI text costs the site a
  little. Accusing a real writer costs that person a lot. A criterion that
  treats both errors as equally bad is describing a system nobody would ship.
- **Unit 8 tests across three trials, and the target has to hold across all
  three.** Your first signal runs a model, so identical input can score
  differently twice. A target of "at most 1 in 10" against trials of 2, 1, 2 is
  a **miss**.

---
## 1. False Positives

Human writing should get called AI only less than 5% of the time.


**Why this target:**
It is very detrimental to label someone's actual work as AI. This could lose trust in the product/program. For this reason, want to keep it very low. 

---

## 2. Score Spread

Clearly AI text scores at least 0.20 higher than clearly human text on average.

**Why this target:**
There needs to be a large enough gap between clearly AI and clearly human. Don't want them mixing together, which could lead to misclassifications. 


---

## 3. Label Coverage

All 3 labels (AI, human, unsure) are reached at least once in each trial.


**Why this target:**
All the labels should be reached, or there will be a problem when that isn't the case (not given full decision path). It means the system is collapsing casse into only two outcomes or failing to handle uncertain text at all.


---

## 4. The Appeal Path

100% of appeals change status and are logged with a record.


**Why this target:**
An appeal system is only useful if it produces a visible result and keeps an audit trail. If the status does not change or the event is not recorded, the system cannot support fairness or review.


---

## 5. Bad Input

Missing or empty text is rejected; input over 10,000–20,000 characters is rejected or safely truncated.


**Why this target:**
Bad input can break the model or create meaningless results. A clear limit prevents crashes and keeps the service reliable under real-world misuse.


---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 8 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Uncertain cases land in the unsure band

         The system handles uncertain cases well.

         **Why this target:** ...

         > **Revised in unit 8:** Text I judged borderline scores between
         > 0.4 and 0.6 in at least 4 of 5 cases.
         >
         > **Why revised:** "well" gave me nothing to check. I couldn't
         > reach a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "At most 1 of 10 of my own pieces flagged as AI" → "at most 3
            of 10", because 1 of 10 turned out to be hard.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
