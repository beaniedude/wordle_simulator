# This program solves the wordle based on your inputs

from wordle_simulator import update_lists
from wordle_simulator import update_possible_words
from wordle_simulator import most_common_letter
import random

def get_word_optimised(possible_words,correct,result):
    ignore_letter = [letter[0] for letter in result if letter[1] != 'wrong']
    #instead of just returning a random choice - looks at the letter that is most common
    #finding the places that have not been guessed correction
    positions = [0,1,2,3,4]
    if correct == []:
        1+1#no correct letters guessed - the "positions" remain unchanged
    else:
        for place in correct:
            #we remove the places to look at for the correct guesses
            positions.remove(place[0])
    common_letter = most_common_letter(possible_words,ignore_letter)
    #we have the most common letter in the word (outside of correct ones)
    likely_words = [word for word in possible_words if common_letter in word]
    ignore_letter.append(common_letter)
    past_likely_words = ['']
    #just so the code runs
    #ideally want to repeat this process a few times but ignoring the correct letters and the just used most_common_letter
    #gotta check if it returns an empty result or not (it won't return an empty set though... gotta check if it changes from the last one)
    #repeat until it is an empty set and then take a random choice of the set just before the empty set
    while likely_words != past_likely_words:
    #runs until empty set and then prints out a random word from when the set was last not empty
        past_likely_words = likely_words
        common_letter = most_common_letter(likely_words,ignore_letter)
        ignore_letter.append(common_letter)
        likely_words = [word for word in likely_words if common_letter in word]
        #need to make it so that when we rerun it doesn't query the same letter
    #now we select one word of the likely_words
    return random.choice(past_likely_words)

def convert_result(guess_word,result_word):
    count = 0
    # format - letter, status for that location
    result = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
    for letter in guess_word:
        result[count][0] = letter
        if result_word[count] == 'g':
            result[count][1] = 'correct'
        elif result_word[count] == 'y':
            result[count][1] = 'nearly_correct'
        elif result_word[count == 'b']:
            result[count][1] = 'wrong'
        count += 1
    return result

# setting up possible_words
possible_words = []
# reading in list of 5 letter words
with open('fivewords.txt') as f:
    for line in f:
        possible_words.append(line.strip())

guessed = 0
while guessed == 0:
    guess_word = input('Enter your 5 letter guess word')
    while len(guess_word) != 5:
        guess_word = input('Please enter a 5 letter guess word')
    print('What was the result for the word?')
    result_word = input('"g" for green, "b" for black, "y" for yellow')
    if result_word == 'ggggg':
        print('Congratulations!')
        guessed = 1
        exit()
    result = convert_result(guess_word,result_word)
    correct, nearly_correct, wrong = update_lists(result)
    possible_words = update_possible_words(correct, nearly_correct, wrong, possible_words)
    if len(possible_words) == 0:
        print('Something went wrong...')
        exit()
    print(f'There are {len(possible_words)} to choose from.')
    print(possible_words)
    print(f'Why not try the word {get_word_optimised(possible_words, correct, result)}?')

