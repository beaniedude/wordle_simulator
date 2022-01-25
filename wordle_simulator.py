#Let's do Wordle!
import random
import statistics

def guess_word_checker(guess_word, goal_word):
    count = 0
    # format - letter, status for that location
    result = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
    for letters in guess_word:
        result[count][0] = letters
        if letters == goal_word[count]:
            result[count][1] = 'correct'
        elif letters in goal_word:
            result[count][1] = 'nearly_correct'
        else:
            result[count][1] = 'wrong'
        count += 1
    return result


def update_lists(result):
    count = 0
    # format: location - the letter
    correct=[]
    nearly_correct=[]
    wrong=[]
    for letters in result:
        if letters[1] == 'correct':
            correct.append([count, letters[0]])
        elif letters[1] == 'nearly_correct':
            nearly_correct.append([count, letters[0]])
        elif letters[1] == 'wrong':
            wrong.append([count, letters[0]])
        count += 1
    return correct, nearly_correct, wrong


def update_possible_words(correct, nearly_correct, wrong, possible_words):
    # format: [location (0,1,2,3, or 4), the letter]
    for letters in correct:
        # narrows down the word based on what letters have been guessed correctly
        possible_words = [word for word in possible_words if word[letters[0]] == letters[1]]
    for letters in nearly_correct:
        # if the letters are somewhere - but not in the location
        location = [0, 1, 2, 3, 4]
        location.remove(letters[0])
        # removing list of words that have the letter in this spot
        possible_words = [word for word in possible_words if word[letters[0]] != letters[1]]
        # looking up list of words which has the letter in other location
        possible_words = [word for word in possible_words if
                          word[location[0]] == letters[1] or word[location[1]] == letters[1] or word[location[2]] ==
                          letters[1] or word[location[3]] == letters[1]]
    for letters in wrong:
        # get the words that do not have the wrong letters
        possible_words = [word for word in possible_words if letters[1] not in word]
    return possible_words


def get_word(possible_words):
    return random.choice(possible_words)

def most_common_letter(possible_words,ignore_letter):
    list_of_letters=[]
    for words in possible_words:
        #removing duplicates to make it a tiny bit fair
        words=list(set(words))
        for letters in words:
            #step through the letters
            #ignoring all the ignored letters
            if letters not in ignore_letter:
                list_of_letters.append(letters)
    #for each place what is the most common letter?
    #most common letter in each place - if vowel use that etc maybe?
    if list_of_letters==[]:
        return ''
    else:
        return statistics.mode(list_of_letters)

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
        print(f"Filtering based on the most common letter: '{common_letter}'. {str(len(likely_words))} words to choose from.")
        print(likely_words)
        #need to make it so that when we rerun it doesn't query the same letter
    #now we select one word of the likely_words
    return random.choice(past_likely_words)

def simulate(guess_word, goal_word, possible_words):
    print('the goal word is: '+goal_word)
    print('the guess word is: ' + guess_word)
    # creating/resetting first sets
    guessed_words = []
    # setting guessed word
    guessed_words.append(guess_word)
    while guess_word != goal_word:
        result = guess_word_checker(guess_word, goal_word)
        print(result)
        correct,nearly_correct,wrong = update_lists(result)
        possible_words = update_possible_words(correct, nearly_correct, wrong, possible_words)
        print(f'List of {str(len(possible_words))} possible words to choose from:')
        print(possible_words)
        guess_word = get_word_optimised(possible_words,correct,result)
        guessed_words.append(guess_word)
        print(f'Therefore your randomly chosen word for guess number {str(len(guessed_words))} is {guess_word}.')
    return guessed_words


# setting up possible_words
possible_words = []
# reading in list of 5 letter words
with open('fivewords.txt') as f:
    for line in f:
        possible_words.append(line.strip())

# going through all the possible words to find the best starting word
#starting_word = []
#for word in possible_words:
#    number_of_tries = []
#    listoflength = []
#    i = 0
#    while i < 1:
#        goal_word = get_word(possible_words)
#        guess_word = word
#        number_of_tries.append(simulate(guess_word, goal_word, possible_words))
#        i += 1
#    for length in number_of_tries:
#        listoflength.append(len(length))
#    starting_word.append([statistics.median(listoflength), word])

#df = pd.DataFrame(starting_word)
#df.to_csv('data.csv')

number_of_tries = []
listoflength = []
goal_word = ''
guess_word = ''
number_of_tries.append(simulate(guess_word, goal_word, possible_words))
print(f'Congratulations you got it in {str(len(number_of_tries[0]))} tries!')
print(number_of_tries)
