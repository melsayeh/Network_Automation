from Question import Question

questionPrompt = [
    "How many planet in the Solar System (a/b/c)? \n (a) 8 \n (b) 9 \n (c) 10\n\n",
    "What color is tomato (a/b/c)? \n (a) Green \n (b) Yellow \n (c) Red\n\n",
    "What shape is the sun (a/b/c)? \n (a) Circle \n (b) Square \n (c) Triangle\n\n",
    "What is the capitol of Egypt (a/b/c)? \n (a) Aswan \n (b) Cairo \n (c) Alexandria\n\n"
]

questions = [Question(questionPrompt[0], "a"),
             Question(questionPrompt[1], "c"),
             Question(questionPrompt[2], "a"),
             Question(questionPrompt[3], "b"),
             ]


def runTest(q):
    score = 0
    for question in questions:
        answer = input(question.prompt)
        if answer == question.answer:
            score = score + 1
            print("**** Correct **** \n\n")
        else:
            print("**** Incorrect ****\n\n")
    print("You got " + str(score) + " / " + str(len(questions)))


runTest(questions)
