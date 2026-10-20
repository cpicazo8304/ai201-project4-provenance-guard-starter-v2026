"""
What your test runs. ← UNIT 8, MILESTONE 3

Each of your five criteria needs something run against it. A criterion about
false positives needs your own writing. One about label coverage needs inputs
across the score range. One about the appeal path needs a real content_id.

Working that out is Milestone 3's first step, and this file is where you write
it down. `run_eval.py` runs everything here three times.

Each criterion has a scenario below. Replace or expand the example inputs to
match your own criteria and writing.

A scenario carries **either** of these:

    "texts"   a list of strings. Each is sent as {"text": ..., "creator_id": ...}
              with a creator_id made up for you. Use this for most criteria.

    "bodies"  a list of whole request bodies, sent exactly as written. Use this
              when the malformed request IS the point — empty text, no `text`
              field at all, something enormous. A bad-input criterion needs it,
              because you cannot express "the field is missing" as a string.

    "appeal_reasoning"  optional text. When present, run_eval.py appeals each
              successful submission and checks the audit log for under_review.
"""

SCENARIOS = [
    {
        "name": "my own writing",
        "criterion": 1,
        # Add more of your own writing here for a meaningful estimate of a
        # false-positive rate; this sample alone only gives a coarse check.
        "texts": [
            (
                "What drove me was knowing that technical skills alone won't "
                "get someone hired or keep them in a role. As a student myself "
                "for another course in the same pathway, I understand that the "
                "ability to communicate with a teammate, speak up in a meeting, "
                "or push back on an idea respectfully are skills students need "
                "to practice before they enter the workforce. I wanted to give "
                "them a safe environment to build that muscle."
            ),
        ],
    },
    {
        "name": "score spread",
        "criterion": 2,
        "texts": [
            (
                "A strong learning environment helps students develop both "
                "technical knowledge and professional communication skills. "
                "By practicing collaboration, clear discussion, and respectful "
                "disagreement, learners can build confidence before entering "
                "the workplace. These experiences support individual growth "
                "and help teams solve problems more effectively."
            ),
            (
                "What drove me was knowing that technical skills alone won't "
                "get someone hired or keep them in a role. As a student myself "
                "for another course in the same pathway, I understand that the "
                "ability to communicate with a teammate, speak up in a meeting, "
                "or push back on an idea respectfully are skills students need "
                "to practice before they enter the workforce. I wanted to give "
                "them a safe environment to build that muscle."
            ),
        ],
    },
    {
        "name": "label coverage",
        "criterion": 3,
        "texts": [
            (
                "A strong learning environment helps students develop both "
                "technical knowledge and professional communication skills. "
                "By practicing collaboration, clear discussion, and respectful "
                "disagreement, learners can build confidence before entering "
                "the workplace. These experiences support individual growth "
                "and help teams solve problems more effectively."
            ),
            (
                "What drove me was knowing that technical skills alone won't "
                "get someone hired or keep them in a role. As a student myself "
                "for another course in the same pathway, I understand that the "
                "ability to communicate with a teammate, speak up in a meeting, "
                "or push back on an idea respectfully are skills students need "
                "to practice before they enter the workforce. I wanted to give "
                "them a safe environment to build that muscle."
            ),
            (
                "I like the idea, although I am not completely sure it will "
                "work in every class. Students need time to practice, but some "
                "may be uncomfortable speaking up at first. A small group "
                "activity could help; the instructor can observe what happens "
                "and adjust the next session based on the feedback."
            ),
        ],
    },
    {
        "name": "appeal path",
        "criterion": 4,
        "texts": [
            (
                "What drove me was knowing that technical skills alone won't "
                "get someone hired or keep them in a role. As a student myself "
                "for another course in the same pathway, I understand that the "
                "ability to communicate with a teammate, speak up in a meeting, "
                "or push back on an idea respectfully are skills students need "
                "to practice before they enter the workforce. I wanted to give "
                "them a safe environment to build that muscle."
            ),
        ],
        "appeal_reasoning": (
            "I wrote this submission myself and would like a person to review "
            "the decision."
        ),
    },
    {
        "name": "bad input",
        "criterion": 5,
        "bodies": [
            {"text": "", "creator_id": "eval_bad_empty"},
            {"creator_id": "eval_bad_missing"},
            {"text": None, "creator_id": "eval_bad_null"},
            {"text": "word " * 4001, "creator_id": "eval_bad_over_limit"},
        ],
    },
]


def validate() -> list[str]:
    """
    Complain about anything malformed, before a long run rather than during.

    A "bodies" scenario is deliberately exempt from the empty check — an empty
    string is the whole point of a bad-input case, and refusing to run one
    would make that criterion untestable.
    """
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("name"):
            problems.append(f"scenario {i} has no name")

        texts = scenario.get("texts")
        bodies = scenario.get("bodies")

        if texts and bodies:
            problems.append(
                f"scenario {i} ('{scenario.get('name')}') has both texts and "
                f"bodies — pick one"
            )
            continue

        if bodies:
            for j, body in enumerate(bodies, 1):
                if not isinstance(body, dict):
                    problems.append(
                        f"scenario {i}, body {j} is not a dict — bodies are whole "
                        f"request bodies, like {{'text': '', 'creator_id': 'x'}}"
                    )
            continue

        if not texts:
            problems.append(f"scenario {i} has no texts and no bodies")
            continue

        for j, text in enumerate(texts, 1):
            if not str(text).strip():
                problems.append(
                    f"scenario {i}, text {j} is empty — if an empty submission is what "
                    f"you're testing, use 'bodies' instead of 'texts'"
                )
            elif str(text).startswith("REPLACE ME"):
                problems.append(
                    f"scenario {i} ('{scenario.get('name')}'), text {j} is still "
                    f"the placeholder"
                )
    return problems
