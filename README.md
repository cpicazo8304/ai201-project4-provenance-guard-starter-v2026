# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> and in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     Unit 7 asks for the first five sections. Unit 8 adds the five below.

     Everything is pasted as TEXT. A pasted curl response gets full credit;
     a picture of your terminal gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 7 — THE BUILD ═══════════════════════ -->

## What This Does

- HTTP request: receives the submission as JSON.
- JSON parsing and validation: extracts text and creator_id; rejects missing or invalid input.
- Model signal: detector.py estimates how predictable the text is.
- Style signal: stylometry.py measures its surface patterns.
- Combiner: scoring.py combines the two 0–1 signals into one score.
- Labeler: compares the score with the thresholds in config.py and creates a reader-facing label.
- Audit and response: records the decision and returns the label and scores to the caller.

---

## Signals and Scoring

### Signal one — the model signal

**What it measures:** Measures text predictability to the local language model

**Why that might differ between human and AI writing:** AI-generated text may be more predictable because models tend to choose likely next words. 

**What it can't see:** who wrote it. Plain, conventional human writing can also be predictable; unusual AI text can be surprising.

### Signal two — the style signal

**What it measures:** Intended to measure sentence-length variation, vocabulary repetition, and punctuation patterns

**Why that might differ between human and AI writing:**generated text may be more even or repetitive.

**What it can't see:**meaning or authorship. Quotations, edits, or deliberate formatting changes can alter its measurements. The functions are currently stubs.

### The combining rule

**The rule:** I combine the model and style scores with a weighted average. Since the model signal is somewhat lenient about calling text AI-generated and tends to score it lower, the style signal gets more influence. When the signals disagree, the combined score leans toward the style signal.

**The numbers:** `0.35 × model_score + 0.65 × style_score`

**Where it lives:** `scoring.py::combine_signals`

**A case where my two signals split, and what my rule does with it:** If the model score is 0.20 and the style score is 0.80, the combined score is 0.59, so it leans toward the style signal but remains unsure.



---

## Label Variants

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human | 0.00 - 0.35 | We think this was probably written by a person. |
| unsure | 0.35 - 0.60 | We’re not sure whether this was written by a person or by AI. |
| high-confidence AI | 0.60 - 1.00 | We think this was probably written by an AI. |

**Why I worded the "unsure" one this way:**This works because it claims uncertainty without accusing the writer. 



---

## Sample Run

<!-- One submission and one appeal, pasted as text: the request, the response,
     and the log entries. -->

**A submission**

<!-- The response needs content_id, guess, confidence, label, AND both
     signal scores - model_score and style_score. Unit 8's tools read those
     two off the response, so leaving them out costs you next unit's
     diagnostics. -->

```bash
$ curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "The commas are not the problem: the text is already wrapped in quotes, so commas inside it are treated as part of the text. I checked labels.csv and found the rows are missing valid labels:", "creator_id": "158943"}'
```

```json
{
  "confidence": 0.6660214253151155,
  "content_id": "3c40901101ae457e8ca69530936d0ff6",
  "guess": "ai",
  "label": "We think this was probably written by an AI.",
  "model_score": 0.4317,
  "style_score": 0.7921945004847931
}
```

**An appeal**

```bash
$ curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "...", "reasoning": "..."}'
```

```json
{
  "content_id": "3c40901101ae457e8ca69530936d0ff6",
  "message": "Appeal submitted successfully."
}
```

**What the log shows afterwards**

```bash
$ curl "http://127.0.0.1:5000/log?limit=3"
```

```json
{
  "count": 5,
  "entries": [
    {
      "combined_score": 0.12715,
      "confidence": "your_confidence_here",
      "content_id": "8bccca4c7f624064a10c5b89d69d613e",
      "creator_id": "158943",
      "guess": "your_guess_here",
      "label": "your_label_here",
      "model_score": 0.2543,
      "status": "submitted",
      "style_score": 0.0,
      "text": "I am an AI language model trained by OpenAI. I can help answer questions, summarize text, or draft emails in a clear, professional style.",
      "timeframe": 1791773490.6570644,
      "timestamp": "2026-10-12T02:51:30+00:00"
    },
    {
      "combined_score": 0.12715,
      "confidence": "your_confidence_here",
      "content_id": "dee63f6f675a4548bb048a677eff7652",
      "creator_id": "158943",
      "guess": "your_guess_here",
      "label": "your_label_here",
      "model_score": 0.2543,
      "status": "submitted",
      "style_score": 0.0,
      "text": "I am an AI language model trained by OpenAI. I can help answer questions, summarize text, or draft emails in a clear, professional style.",
      "timeframe": 1791776366.6367726,
      "timestamp": "2026-10-12T03:39:26+00:00"
    },
    {
      "combined_score": 0.21585,
      "confidence": "your_confidence_here",
      "content_id": "53bc3c16a8d0421a91cd2162a2e61753",
      "creator_id": "158943",
      "guess": "your_guess_here",
      "label": "your_label_here",
      "model_score": 0.4317,
      "status": "submitted",
      "style_score": 0.0,
      "text": "The commas are not the problem: the text is already wrapped in quotes, so commas inside it are treated as part of the text. I checked labels.csv and found the rows are missing valid labels:",
      "timeframe": 1791776448.7375565,
      "timestamp": "2026-10-12T03:40:48+00:00"
    },
    {
      "combined_score": 0.6660214253151155,
      "confidence": 0.6660214253151155,
      "content_id": "3c40901101ae457e8ca69530936d0ff6",
      "creator_id": "158943",
      "guess": "ai",
      "label": "We think this was probably written by an AI.",
      "model_score": 0.4317,
      "status": "submitted",
      "style_score": 0.7921945004847931,
      "text": "The commas are not the problem: the text is already wrapped in quotes, so commas inside it are treated as part of the text. I checked labels.csv and found the rows are missing valid labels:",
      "timeframe": 1791779056.2631078,
      "timestamp": "2026-10-12T04:24:16+00:00"
    },
    {
      "content_id": "3c40901101ae457e8ca69530936d0ff6",
      "creator_id": "158943",
      "event": "appeal",
      "reasoning": "I was responding to an assingment.",
      "status": "under_review",
      "timestamp": "2026-10-12T04:29:27+00:00"
    }
  ]
}
```

---

## How I Used AI

**Moment 1**

- *What I asked for:* Help explaining how to combine the model and style signals when the model score is too lenient.
- *What came back:* A suggestion to use a weighted average and give more weight to the style signal.
- *What I changed:* I chose weights of 0.35 for the model and 0.65 for style, then updated the rule in my README and config.

**Moment 2**

- *What I asked for:* Help wording the unsure label so it would not sound accusatory.
- *What came back:* “We’re not sure whether this was written by a person or by AI.”
- *What I changed:* I chose a short, neutral statement that communicates uncertainty without blaming the writer.

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** ___ per minute, ___ per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```

```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->



**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json

```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:



---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json

```

**Diagnoses**

<!-- For each miss AND each broken attack: the stage and the mechanism.

     Your service has five stages: the route, signal one, signal two, the
     combining rule, and the label mapping.

     Not a diagnosis:  "The evasion attacks got through."
     A diagnosis:      "Four evasion inputs got through. All four had typos
                        added to AI-generated text. My second signal measures
                        word variety, and typos raise word variety — so it read
                        them as more human. My combining rule weights that
                        signal at 0.6, so it dragged the whole score down."

     Look for a pattern. Five failures on one signal is one problem, not five. -->



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->



**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->



---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->



**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

       [ ] criteria.md has five numbered criteria, each naming a target
       [ ] Each has a reason underneath
       [ ] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [ ] Two signals that measure DIFFERENT things, each with a named blind spot
       [ ] Three label variants, all reachable, written out in full
       [ ] POST /appeal changes status and writes to the log
       [ ] Signals and Scoring names scoring.py::combine_signals
       [ ] Sample Run: a submission AND an appeal, as pasted text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

       [ ] Rate limiting on /submit, with your numbers justified
       [ ] The pasted run of status codes showing 429
       [ ] Audit log with all nine fields, recording rejections too
       [ ] The attack set run IN FULL, every input with an outcome
       [ ] Ten audit log entries pasted as text
       [ ] Five criteria across three trials
       [ ] A diagnosis for every miss and every broken attack — stage AND mechanism
       [ ] One improvement, with Attack Run — After
       [ ] What's Still Broken, including the production trade
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
