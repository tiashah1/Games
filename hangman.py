from words import word_list
import random

def getWord():
    word = random.choice(word_list)
    return word.upper()

def play(word):
    complete_word = "_" * len(word)
    guessed = False
    guessed_letters = []
    guessed_words = []
    tries = 6

    print("Lets play the game!")
    print(display_hangman(tries))
    print(complete_word)
    print("\n")

    while not guessed and tries > 0:
        guess = input("Please guess a letter or word: ").upper()
        if len(guess) == 1 and guess.isalpha():
            if guess in guessed_letters:
                print("You alredady guessed the letter", guess)
            elif guess not in word:
                print(guess, "is not in the word")
                tries -= 1
                guessed_letters.append(guess)
            else:
                print("Correct,", guess, "is in the word!")
                guessed_letters.append(guess)
                word_as_list = list(complete_word)
                indexList = [i for i, letter in enumerate(word) if letter == guess]
                for index in indexList:
                    word_as_list[index] = guess
                complete_word = "".join(word_as_list)
                if "_" not in complete_word:
                    guessed = True
        elif len(guess) == len(word) and guess.isalpha():
            if guess in guessed_words:
                print("You have already guessed the word", guess)
            if guess != word:
                print(guess, "is not the word")
                tries -= 1
                guessed_words.append(guess)
            else:
                guessed = True
                complete_word = word
        else:
            print("Not a valid guess")
        print(display_hangman(tries))
        print(complete_word)
        print("\n")

    if guessed:
        print("Congratulations! You guessed the word")
    else:
        print("You ran out of tries, the correct word was", word)

        
def display_hangman(tries):
    state = [ # final state: head, torso, both arms, and both legs
                """
                   --------
                   |      |
                   |      O
                   |     \|/
                   |      |
                   |     / \
                   -
                """,
                # head, torso, both arms, and one leg
                """
                   --------
                   |      |
                   |      O
                   |     \|/
                   |      |
                   |     / 
                   -
                """,
                # head, torso, and both arms
                """
                   --------
                   |      |
                   |      O
                   |     \|/
                   |      |
                   |      
                   -
                """,
                # head, torso, and one arm
                """
                   --------
                   |      |
                   |      O
                   |     \|
                   |      |
                   |     
                   -
                """,
                # head and torso
                """
                   --------
                   |      |
                   |      O
                   |      |
                   |      |
                   |     
                   -
                """,
                # head
                """
                   --------
                   |      |
                   |      O
                   |    
                   |      
                   |     
                   -
                """,
                # initial empty state
                """
                   --------
                   |      |
                   |      
                   |    
                   |      
                   |     
                   -
                """
        ]
    return state[tries]

def main(): 
    #Generate a random word from the list
    word = getWord()
    play(word)

    while input("Would you like to play again? (Y/N)").upper() == "Y":
        word = getWord()
        play(word)

if __name__ == "__main__":
    main()






