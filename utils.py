# ref: https://docs.python.org/3/tutorial/modules.html
# Moved shared functions to utils.py to avoid circular imports
# ref: https://dictionaryapi.dev/
# Used to validate if a word is a real English word via HTTP request
import requests

word_cache = {}

def is_valid_word(word):
    if word in word_cache:
        return word_cache[word]

    base_url = "https://api.dictionaryapi.dev/api/v2/entries/en/"
    try:
        response = requests.get(f"{base_url}{word}")
        is_valid = response.status_code == 200
        word_cache[word] = is_valid
        return is_valid
    except requests.exceptions.RequestException:
        return False


def check_guess(secret_word, guess):
    secret_word = secret_word.lower()
    guess = guess.lower()

    if len(guess) != len(secret_word):
        return None

    feedback = [""] * len(secret_word)
    used_positions = [False] * len(secret_word)

    for i in range(len(guess)):
        if guess[i] == secret_word[i]:
            feedback[i] = "G"
            used_positions[i] = True

    for i in range(len(guess)):
        if feedback[i] == "":
            for j in range(len(secret_word)):
                if guess[i] == secret_word[j] and not used_positions[j]:
                    feedback[i] = "Y"
                    used_positions[j] = True
                    break
            if feedback[i] == "":
                feedback[i] = "X"

    return feedback