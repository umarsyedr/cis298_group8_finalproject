import requests
import csv
from loader import load_word_list
from interface import display_menu, get_list_name, display_start_message, play_quiz


# ref: https://www.w3schools.com/python/ref_requests_post.asp
# api ref: https://github.com/meetDeveloper/freeDictionaryAPI

# kinda unrelated to the cache commit, but a really good vid for understanding caching: https://www.youtube.com/watch?v=W6b6J1svbj8

# for cache, a helper basicaly
# ref: https://docs.python.org/3/library/csv.html
def save_defs(filepath, words_with_defs):
    with open(filepath, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["word", "definition"])
        writer.writeheader()
        writer.writerows(words_with_defs)

def get_definitions(word_list):
    list_with_defs = []
    # put this in env later, although the documentation doesn't say too.
    base_url = "https://api.dictionaryapi.dev/api/v2/entries/en/"
    
    for word in word_list:
        if word.get("definition"):
            list_with_defs.append(word)
            continue
        try:
            # had to change this because its a dict now which helps with caching
            response = requests.get(f"{base_url}{word['word']}")
            response.raise_for_status()  # Raise error if response is bad
            data = response.json()
            definition = data[0]["meanings"][0]["definitions"][0]["definition"]
            list_with_defs.append({"word": word['word'], "definition": definition})
            print(f"{word['word']}: {definition}")
        except requests.exceptions.RequestException as e:
            print(f"Error fetching '{word['word']}': {e}")
        except (IndexError, KeyError) as e:
            print(f"Could not parse definition for '{word['word']}': {e}")

    return list_with_defs

def check_guess(secret_word, guess):
    secret_word = secret_word.lower()
    guess = guess.lower()

    if len(guess) != len(secret_word):
        print("Guess must be of the same length as the word")
        return None

    feedback = [""] * len(secret_word)
    used_positions = [False] * len(secret_word)

    #For correct position
    for i in range(len(guess)):
        if guess[i] == secret_word[i]:
            feedback[i] = "G"
            used_positions[i] = True

    #For correct letter wrong position
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


# TESTING: Load words from CSV, then get definitions
"""if __name__ == "__main__":

        # Load medical words
        words = load_word_list("medical_list.csv")
        print(f"\nLoaded words: {words[:5]}...\n")

        # Get definitions for those words and print
        words_with_defs = get_definitions(words)
        print(f"\nTotal words with definitions: {len(words_with_defs)}")
        save_defs("medical_list.csv", words_with_defs)

        # Load social studies words
        words = load_word_list("social_studies_list.csv")
        print(f"\nLoaded words: {words[:5]}...\n")

        # Get definitions for those words and print
        words_with_defs = get_definitions(words)
        print(f"\nTotal words with definitions: {len(words_with_defs)}")

        # Load custom list
        words = load_word_list("custom_list.csv")
        print(f"\nLoaded words: {words[:5]}...\n")

        # Get definitions for those words and print
        words_with_defs = get_definitions(words)
        print(f"\nTotal words with definitions: {len(words_with_defs)}")"""

# Main Program
if __name__ == "__main__":
    while True:
        # Show menu
        choice = display_menu()

        if choice == "4":
            print("\n Thanks for playing! Goodbye!\n")
            break

        # Get list filename
        filepath, list_name = get_list_name(choice)

        if not filepath:
            print("Invalid choice. Try again.\n")
            continue

        # Load words
        print(f"\nLoading {list_name} vocabulary...")
        words = load_word_list(filepath)

        if not words:
            print(f"Could not load {list_name} list. Try again.\n")
            continue

        # Get definitions (API or cached)
        print(f"Loading definitions...")
        words_with_defs = get_definitions(words)

        # Save definitions back to file (caching for next time)
        save_defs(filepath, words_with_defs)

        # Show motivational message
        display_start_message(list_name)

        # Run the quiz
        play_quiz(words_with_defs)