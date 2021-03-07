from typing import List, Any

import hangman_game_body as h

score = 0
score_average = 0
amount_of_rounds = 0
scores = []
times = []
words = []
wrong_guesses = []

next_round = True
while next_round:
    score, time, word, wrong_guess = h.game_body()
    scores.append(h.truncate(score, 2))
    times.append(h.truncate(time, 2))
    words.append(word)
    wrong_guesses.append(wrong_guess)

    amount_of_rounds += 1
    score_average = sum(scores) / amount_of_rounds
    h.screen_clear()

    print(f"Your average score is: {h.truncate(score_average, 2)} points")
    print("Your scores so far:\nRound\tScore\tWord\tTime\tBad guesses")
    for index in range(len(scores)):
        print(f"{index + 1}.\t\t{int(scores[index])}\t{words[index]}\t{times[index]}s\t{wrong_guesses[index]}")
    choice = str(input("Do you want to play again? Type in \'y\' or \'Y\' to continue\n"))
    choice = choice.lower()
    next_round = False
    if choice == "y":
        next_round = True

