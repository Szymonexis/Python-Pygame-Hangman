import random
import os
from hangman_sections import Hangman
from timeit import default_timer as timer
from time import sleep


def file_len(file_name):
    with open(file_name) as f:
        for i, l in enumerate(f):  # i -> position, l -> line
            pass
    return i + 1


def screen_clear():
    if os.name == 'posix':  # for mac and linux(here, os.name is 'posix')
        _ = os.system('clear')  # _ - assigment for the function itself
    else:
        _ = os.system('cls')  # for windows platform


def system_pause():
    if os.name == 'posix':  # for mac and linux(here, os.name is 'posix')
        _ = os.system('read -n 1 -s -p \"Press any key to continue...\"')  # _ - assigment for the function itself
    else:
        _ = os.system('pause')  # for windows platform


def truncate(n, decimals=0):
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier


def hangman_picture(wrong_guesses):
    print(Hangman.HANGMANPICS[(len(Hangman.HANGMANPICS) - 1) - wrong_guesses])


def hints_amount(hangman_word):
    if len(hangman_word) > 9:
        amount_of_hints = 3
    elif len(hangman_word) > 5:
        amount_of_hints = 2
    else:
        amount_of_hints = 1
    return amount_of_hints


def hint(hints_left, hangman_word, guessed):
    if hints_left == -1:
        print("You have used up your hints :(")
    else:
        for index in range(len(guessed)):
            if guessed[index] == "_":
                print(f"Hint - type in a letter \'{hangman_word[index]}\'")
                print(f"Hints left: {hints_left}")
                break


def game_body():
    words_file_path = "E:\\Studia\\0.4. Projekty Python\\Hangman\\words.txt"
    words = open(words_file_path, "r")
    amount_of_lines = file_len(words_file_path)
    line_to_read = [0, int(random.random() * amount_of_lines) % amount_of_lines]

    hangman_word = ""
    for position, line in enumerate(words):
        if position in line_to_read:
            hangman_word = line
    hangman_word = hangman_word.rstrip()

    words.close()

    guessed = ""
    for letter in hangman_word:
        if letter != "\n" and letter.isalnum() and not letter.isdigit():
            guessed += "_"
        else:
            guessed += letter

    bad_guesses = []
    guesses = []
    wrong_guesses = len(Hangman.HANGMANPICS) - 1

    print(f"It's a {len(guessed)} letter word\t" + guessed)
    # print(hangman_word)    #for testing purposes
    start = timer()
    hints = hints_amount(hangman_word)
    while guessed != hangman_word and wrong_guesses != 0:
        bad_guess = True
        hint_mode = False

        guess = ""
        while not (len(guess) == 1 or len(guess) == len(hangman_word)) or guess.isdigit():
            guess = str(input(
                "Provide your guess - it needs to be a single letter or the " +
                "whole word (enter \'.h\' for a hint):\n"))
            if guess == ".h":
                hints -= 1
                hint_mode = True
                break

        if not hint_mode:
            guess = guess.lower()

            screen_clear()

            if len(guess) == 1:
                for position in range(len(hangman_word)):
                    if hangman_word[position] == guess:
                        guessed = list(guessed)
                        guessed[position] = guess
                        guessed = "".join(guessed)
                        bad_guess = False

                already_guessed_bad = False
                for letter in bad_guesses:
                    if letter == guess:
                        already_guessed_bad = True

                if bad_guess and not already_guessed_bad:
                    bad_guesses.append(guess)
                    wrong_guesses -= 1

                if guess in guesses:
                    print(f"You already guessed \'{guess}\'")
                else:
                    print(f"Your guess is \'{guess}\'")
                guesses.append(guess)
            else:
                if guess == hangman_word:
                    guessed = guess
                else:
                    already_guessed_bad = False
                    for letter in bad_guesses:
                        if letter == guess:
                            already_guessed_bad = True

                    if bad_guess and not already_guessed_bad:
                        bad_guesses.append(guess)
                        wrong_guesses -= 1

            if len(bad_guesses) == 0:
                print("No bad guesses so far :)")
            else:
                print("Your wrong guesses are:")
                for index in range(len(bad_guesses)):
                    if index != len(bad_guesses) - 1:
                        print(f"{bad_guesses[index]}", end=", ")
                    else:
                        print(f"{bad_guesses[index]}")
            print(f"Mistakes to be made left: {wrong_guesses}")
            print(f"It's a {len(guessed)} letter word\t" + guessed)
            hangman_picture(wrong_guesses)
            print(end="\n\n")
        else:
            hint(hints, hangman_word, guessed)

    end = timer()
    game_time = end - start
    bad_letters = 1

    for word in bad_guesses:  # needed to calculate the score
        bad_letters += len(word)

    if wrong_guesses == 0:
        score = 10 ** 5 * (
                (1 / bad_letters * (1 / (10000 * game_time))) / len(hangman_word))  # score for bad guess scenario
    else:
        score = 10 ** 5 * ((1 / bad_letters * (1000 / game_time)) / len(hangman_word))  # score promotes no bad guesses

    print(f"Game time: {truncate(game_time, 2)}s")

    if wrong_guesses == 0:
        print(f"-------YOU LOST-------\nThe word was \"{hangman_word}\"\nYour score is: {int(score)}")
    else:
        print(f"-------YOU WIN-------\nYour score is: {int(score)}")

    return score, game_time, hangman_word, len(Hangman.HANGMANPICS)-wrong_guesses
