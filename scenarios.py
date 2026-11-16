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

"""Each essay split into 5 sentence-aligned chunks (a list of 5 strings)."""

AI_CITY_HEAT = [
    (
        "A city can prepare for hotter summers by combining immediate "
        "protections with long-term changes to buildings, streets, and public "
        "services. The first priority is helping residents stay safe during "
        "heat waves. Local governments can open cooling centers in libraries "
        "and community buildings, extend their hours during extreme heat, and "
        "provide reliable transportation to those locations."
    ),
    (
        "Public notices should be available in the languages residents use "
        "and should explain warning signs of heat illness, where to find "
        "water, and how to request help. Cities should also check on older "
        "adults, people with medical conditions, outdoor workers, and "
        "residents who lack air conditioning."
    ),
    (
        "Longer-term planning can reduce how much heat neighborhoods absorb. "
        "Planting and maintaining trees provides shade, while cool roofs and "
        "reflective pavement can lower surface temperatures. These "
        "improvements should be prioritized in areas with little existing "
        "shade, rather than distributed uniformly."
    ),
    (
        "Building codes and assistance programs can help residents improve "
        "insulation and cooling efficiency, which also reduces energy use. "
        "Because extreme heat can strain the electric grid, utilities and "
        "city agencies should prepare backup power for hospitals, cooling "
        "centers, and other essential services. Preparation works best when "
        "it is based on local data and community input."
    ),
    (
        "Officials can map heat exposure, review past emergency calls, and "
        "ask residents which resources are difficult to reach. They should "
        "publish clear responsibilities for each agency and evaluate the plan "
        "after every heat season. No single measure will eliminate heat risk, "
        "but coordinated emergency response and fair investment can make the "
        "effects less dangerous over time."
    ),
]

AI_INTERNSHIP = [
    (
        "Students can prepare for a first internship by learning about the "
        "organization, setting practical goals, and building a few reliable "
        "work habits before the first day. Start by reviewing the "
        "organization's website, recent projects, and the internship "
        "description. This helps you understand the team's work and identify "
        "questions to ask your supervisor."
    ),
    (
        "You do not need to memorize every detail. The goal is to arrive with "
        "enough context to follow conversations and see how your assignments "
        "fit into the larger work. It is also useful to clarify expectations "
        "early. Ask who will assign tasks, how progress should be shared, and "
        "when it is appropriate to request feedback."
    ),
    (
        "Keep a simple record of deadlines, decisions, and questions so that "
        "you do not have to rely on memory. If instructions are unclear, "
        "summarize what you think the task requires and confirm before "
        "spending a long time on the wrong approach. When a task is complete, "
        "share the result and mention any obstacles you encountered."
    ),
    (
        "Professionalism does not mean pretending to know everything. Interns "
        "are there to learn, so it is reasonable to ask for examples, "
        "explanations, or help prioritizing. At the same time, try a first "
        "step independently and describe what you have already checked."
    ),
    (
        "Be considerate of coworkers' time, protect confidential information, "
        "and follow the workplace's communication norms. After each week, "
        "note what you learned, what you want to practice, and what feedback "
        "you received. That reflection can help you make the most of the "
        "placement and give you specific examples to discuss later."
    ),
]

AI_REMOTE_WORK = [
    (
        "Remote workers can stay productive by creating structure around "
        "their day, setting up a dedicated workspace, and communicating "
        "clearly with their team. The first step is choosing a consistent "
        "place to work that is separate from areas used for rest."
    ),
    (
        "A reliable chair, good lighting, and a stable internet connection "
        "can reduce distractions and physical strain. Starting and ending "
        "work at regular times also helps establish a boundary between "
        "professional responsibilities and personal life. Clear communication "
        "is equally important when colleagues are not in the same room."
    ),
    (
        "Teams should agree on which tools to use for urgent messages, "
        "routine updates, and longer discussions. Written updates should "
        "include enough context for others to understand progress without a "
        "meeting. When a task is blocked, it is better to raise the issue "
        "early and suggest possible solutions."
    ),
    (
        "Regular video check-ins can also build trust and make it easier to "
        "resolve misunderstandings. Finally, remote workers benefit from "
        "protecting their well-being. Short breaks during the day can improve "
        "focus, and stepping outside can help separate work time from rest."
    ),
    (
        "It is useful to set limits on after-hours messages and to tell "
        "managers when workloads become unmanageable. Tracking weekly goals "
        "can show what is going well and what needs adjustment. No single "
        "routine works for everyone, but consistent habits and open "
        "communication can make remote work sustainable over the long term."
    ),
]

AI_LANGUAGE_LEARNING = [
    (
        "Adults can learn a new language more effectively by setting "
        "realistic goals, practicing consistently, and using a mix of "
        "learning methods. Short daily sessions are generally more useful "
        "than occasional long ones, because regular exposure helps vocabulary "
        "and grammar stay fresh in memory."
    ),
    (
        "Learners should begin with the most common words and phrases, since "
        "these appear frequently in everyday conversation. Setting a specific "
        "target, such as holding a five-minute conversation within three "
        "months, can make progress easier to measure. Listening and speaking "
        "should be part of practice from the beginning."
    ),
    (
        "Podcasts, videos, and music in the target language can improve "
        "comprehension and help learners become familiar with natural rhythm "
        "and pronunciation. Language exchange partners and tutors offer "
        "opportunities to speak and receive feedback. Mistakes are a normal "
        "part of the process, and learners should view them as useful "
        "information rather than failures."
    ),
    (
        "Writing short journal entries can also help reinforce new vocabulary "
        "and sentence structures. Motivation often depends on connecting the "
        "language to personal interests. Reading articles about hobbies, "
        "cooking from recipes, or following creators in the new language can "
        "make study more enjoyable."
    ),
    (
        "Learners should review older material regularly so that earlier "
        "lessons are not forgotten. It can also be helpful to track progress "
        "in a notebook or app and celebrate small milestones. Although "
        "fluency takes time, steady effort and varied practice can lead to "
        "meaningful improvement."
    ),
]

AI_PERSONAL_BUDGET = [
    (
        "Young adults can build healthy financial habits by creating a simple "
        "budget, tracking their spending, and setting aside money for "
        "emergencies. The first step is to list monthly income and regular "
        "expenses, such as rent, groceries, transportation, and "
        "subscriptions."
    ),
    (
        "Comparing these totals shows how much money remains for savings or "
        "other goals. Many people find it helpful to divide spending into "
        "needs, wants, and savings so that priorities are clear. An emergency "
        "fund provides protection against unexpected costs like medical bills "
        "or car repairs."
    ),
    (
        "A common recommendation is to save enough to cover three to six "
        "months of essential expenses, although smaller goals can be a useful "
        "starting point. Automatic transfers to a savings account can make "
        "saving easier because the decision is made only once."
    ),
    (
        "Individuals with debt should understand the interest rates they are "
        "paying and consider paying off higher-interest balances first, while "
        "still making minimum payments on all accounts. It is also important "
        "to review a budget regularly and adjust it as circumstances change. "
        "A new job, a move, or a change in tuition can all affect how much "
        "money is available."
    ),
    (
        "Reading the terms of credit cards and loans can prevent costly "
        "surprises. Setting specific goals, such as saving for a trip or "
        "building a down payment, can improve motivation. Financial habits "
        "take time to develop, but small and consistent actions can create "
        "stability and confidence over the years."
    ),
]

HUMAN_ESSAY_1 = [
    (
        "Currently, I work for CodePath as a Tech Fellow for the second class "
        "in the AI engineering pathway, supporting a community of computer "
        "science students at varying experience levels. CodePath's mission is "
        "to equip college students and early-career professionals with the "
        "technical skills needed to take their next step."
    ),
    (
        "Within the first two weeks, I noticed a recurring problem: a subset "
        "of students were disengaged, whether it be staying silent in "
        "breakout rooms, skipping polls, or avoiding participation in group "
        "discussions. Given that half of the class time focuses on working "
        "with others, this disengagement could be a barrier to their growth."
    ),
    (
        "This was anticipated in our training, so I came prepared with "
        "strategies. If an entire group was disengaged, I'd address the room "
        "directly by explaining why collaboration matters and how to do it "
        "effectively. If it was just one or two students, I'd message them "
        "privately, check in on their situation, and encourage participation "
        "in a way that was supportive and non-critical."
    ),
    (
        "I also used simple ice breakers like introductions to lower the "
        "barrier to engagement. Not every student responded immediately, but "
        "my goal was always to at least plant the seed by giving them the "
        "reasons why collaboration is essential so that over time, they'd "
        "grow more comfortable working with others."
    ),
    (
        "Because of this, I saw groups shift from individually working in "
        "silence to asking each other questions and building on each other's "
        "ideas. Getting someone from silence to confidence made the effort "
        "worth it."
    ),
]

HUMAN_ESSAY_2 = [
    (
        "During my second year at UT Austin, I was part of the Bridging "
        "Disciplines Program for Smart Cities, a program known for mixing "
        "people from different backgrounds. For the title course, we were "
        "tasked with developing a technical solution to a city-level problem."
    ),
    (
        "I was grouped with government and community planning upperclassmen, "
        "making me not only the only technical person but also the least "
        "experienced. It was unlike anything I had done before. I was used to "
        "CS projects targeting specific mathematical concepts, not real-world "
        "applications."
    ),
    (
        "I had to learn new skills while also communicating technical ideas "
        "to non-technical majors, which was something I had never practiced. "
        "Throughout the semester, we had to present our progress in the "
        "project. For our first presentation, our technical solution wasn't "
        "fully fleshed out, so there weren’t many slides tailored towards my "
        "strengths."
    ),
    (
        "I had prepared a few notes relating to statistics on traffic safety "
        "in Austin, but when it was my turn to speak, I didn’t start off "
        "strong and my confidence dropped immediately. My mind went blank. "
        "Everything that I had prepared beforehand vanished. After class, I "
        "felt awful, but I made myself a promise that I would never go blank "
        "again."
    ),
    (
        "I stopped relying on improvisation and started genuinely preparing "
        "by studying the concepts deeply, practicing how I'd articulate "
        "ideas, and finding multiple ways to explain the same thing so that "
        "even if I stuttered or paused, I could recover and keep going. "
        "Preparation became my safety net, not a backup plan."
    ),
]

HUMAN_ESSAY_3 = [
    (
        "Computer science was never my first choice. I was set on becoming an "
        "aerospace engineer, but my eyes were opened by Mr. Jimenez, the AP "
        "computer science and calculus teacher. It was a normal day in school "
        "when I walked to my Pre-AP Algebra I class, but I noticed something "
        "was different about today’s class when I entered the room. A teacher "
        "by the name of Mr."
    ),
    (
        "Jimenez was at the front of class preparing a presentation. Once the "
        "whole class was ready, Mr. Jimenez began to talk about computer "
        "science, and how it would benefit our country’s technology. He "
        "explained that computer science requires for someone to be excellent "
        "at problem solving, which is why he decided to introduce computer "
        "science to the Pre-AP I class."
    ),
    (
        "I was intrigued by how much I fit the profile to become a computer "
        "scientist/software engineer. Ever since I was a child, I had always "
        "excelled in math because of how much fun problem solving was. I "
        "remember when I was a child doing jigsaw puzzles."
    ),
    (
        "The feelings of fulfillment and contentment created in the "
        "completion of these puzzles is what I feel today when I problem "
        "solve. For these reasons, I decided that I wanted to take the "
        "computer science classes. Throughout my sophomore year, I "
        "participated in the Pre-AP and AP Computer Science Principles "
        "classes."
    ),
    (
        "I learned how to create functions, algorithms, if/then statements, "
        "and how to define variables. These were just the basics of computer "
        "science, but I had so much fun during these classes, and am excited "
        "for what the future holds for computer science."
    ),
]

HUMAN_ESSAY_4 = [
    (
        "A football team does not have twenty-two quarterbacks on their team. "
        "Not everyone can be the leader Tom Brady is. A basketball team does "
        "not have ten Lebron James to lead a team. Everyone just needs to "
        "play a part in order for the team to be successful."
    ),
    (
        "Throughout my years in high school, I have played my part and set an "
        "example for others to do the same in order for society and myself to "
        "reach success. As a former band member, I have gained these "
        "qualities that has shaped me into a diligent leader that will "
        "benefit me in UT."
    ),
    (
        "Starting from my freshman year, I was part of the performing group "
        "of my high school band, so I had to wake up early, practice nearly "
        "every day, and work with the rest of my section to play the way our "
        "band directors wanted to."
    ),
    (
        "I was never a drill instructor or drum major for the band, but I "
        "still contributed extensively by being responsible and practicing my "
        "french horn regularly, so the band directors wouldn’t have to look "
        "my way for any reforms in my section’s marching or playing. I "
        "practiced my instrument so much that I was able to make the "
        "All-Region Band in my freshman and junior years, while making the "
        "district band in my sophomore year."
    ),
    (
        "For this reason, my band directors were able to recognize me as a "
        "leader and had me lead my section for our concert band. I was never "
        "an outspoken person, but I was still recognized as a leader because "
        "I did what was best for the concert and marching band by working "
        "diligently to become a better musician. That is how groups win "
        "competitions."
    ),
]

HUMAN_ESSAY_5 = [
    (
        "I have always been a determined person who has never been fulfilled "
        "at my current accomplishments. I have always strived for more and "
        "found ways to improve myself. I was able to use these qualities "
        "throughout my years in band."
    ),
    (
        "During my freshman year of high school, I was part of the performing "
        "group of my school’s marching band, but when concert season came "
        "around the corner, I was moved down to the lower bands because I was "
        "a freshman. This move by the band directors motivated me to make the "
        "All-Region Band because we were told that making All-Region Band "
        "would move us to the top bands."
    ),
    (
        "For more than four weeks, I practiced at home and during lunch. It "
        "was not only to prove that I was good enough to be in the top bands, "
        "but I knew that practicing my instrument would make me a better "
        "person overall. By practicing daily, I became a more responsible and "
        "determined individual."
    ),
    (
        "When the day came to compete in the All-Region Band competition, I "
        "played my instrument as best as I could in front of judges. Once the "
        "scores came out, I nearly had a heart attack from the realization "
        "that I made the All-Region Band."
    ),
    (
        "I held my head up a high and was congratulated by my colleagues, but "
        "no one congratulated me more than myself. My band directors still "
        "did not move me up to the top bands because they preferred seniors, "
        "who were more experienced, but I was still jubilant since I grew as "
        "a person in those few weeks."
    ),
]

AI_EXAMPLES = AI_CITY_HEAT + AI_INTERNSHIP + AI_REMOTE_WORK + AI_LANGUAGE_LEARNING + AI_PERSONAL_BUDGET
HUMAN_EXAMPLES = HUMAN_ESSAY_1 + HUMAN_ESSAY_2 + HUMAN_ESSAY_3 + HUMAN_ESSAY_4 + HUMAN_ESSAY_5


CLEARLY_HUMAN = HUMAN_ESSAY_3 + HUMAN_ESSAY_4
CLEARLY_AI = AI_EXAMPLES

SCENARIOS = [
    {
        "name": "false positives",
        "criterion": 1,
        # All 25 human chunks; at most 3 may come back labeled AI.
        "texts": HUMAN_EXAMPLES,
    },
    # {
    #     "name": "admin check",
    #     "criterion": 2,
    #     # Whole request bodies, because a missing or bad admin_id is the point.
    #     # NOTE: field names are my guess; match them to your admin endpoint.
    #     "bodies": [
    #         {"content_id": "eval_admin_ok", "admin_id": "admin_1", "text": HUMAN_ESSAY_1[0], "label": "human", "label_source": "reviewer"},
    #         {"content_id": "eval_admin_missing", "text": HUMAN_ESSAY_1[0], "label": "human", "label_source": "reviewer"},
    #         {"content_id": "eval_admin_empty", "admin_id": "", "text": HUMAN_ESSAY_1[0], "label": "human", "label_source": "reviewer"},
    #         {"content_id": "eval_admin_none", "admin_id": None, "text": HUMAN_ESSAY_1[0], "label": "human", "label_source": "reviewer"},
    #         {"content_id": "eval_admin_unknown", "admin_id": "not_a_real_admin", "text": HUMAN_ESSAY_1[0], "label": "human", "label_source": "reviewer"},
    #     ],
    # },
    {
        "name": "dataset label and source",
        "criterion": 3,
        # All 50 examples (25 AI + 25 human), each of which should end up with
        # a valid label and source.
        "texts": AI_EXAMPLES + HUMAN_EXAMPLES,
    },
    {
        "name": "score spread",
        "criterion": 4,
        # Clearly AI vs clearly human; the AI average should be at least 0.20 higher.
        "texts": CLEARLY_AI + CLEARLY_HUMAN,
    },
    {
        "name": "safe fallback with too little data",
        "criterion": 5,
        # A mix of both kinds. Run this against a dataset with fewer than 5
        # examples per label; every style score should be exactly 0.5.
        "texts": AI_CITY_HEAT[:2] + HUMAN_ESSAY_1[:2] + HUMAN_ESSAY_3[:1],
    },
]


SCENARIOS = [
    {
        "name": "my own writing",
        "criterion": 1,
        # These five essays are the human-writing samples for false-positive checks.
        "texts": HUMAN_EXAMPLES,
    },
    {
        "name": "score spread",
        "criterion": 2,
        "texts": [
            AI_CITY_HEAT,
            AI_INTERNSHIP,
            HUMAN_ESSAY_1,
            HUMAN_ESSAY_2,
        ],
    },
    {
        "name": "label coverage",
        "criterion": 3,
        "texts": [
            AI_CITY_HEAT,
            AI_INTERNSHIP,
            HUMAN_ESSAY_1,
            HUMAN_ESSAY_3,
        ],
    },
    {
        "name": "appeal path",
        "criterion": 4,
        "texts": [
            HUMAN_ESSAY_1,
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
