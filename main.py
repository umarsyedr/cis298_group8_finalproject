import requests
from loader import load_word_list

# ref: https://www.w3schools.com/python/ref_requests_post.asp
# api ref: https://github.com/meetDeveloper/freeDictionaryAPI

def get_definitions(word_list):
    list_with_defs = []
    for word in word_list:
        # put this in env later, although the documentation doesn't say too.
        base_url = "https://api.dictionaryapi.dev/api/v2/entries/en/"
        try:
            response = requests.get(f"{base_url}{word}")
            response.raise_for_status()  # Raise error if response is bad
            data = response.json()
            definition = data[0]["meanings"][0]["definitions"][0]["definition"]
            list_with_defs.append({"word": word, "definition": definition})
            print(f"✓ {word}: {definition[:200]}...")  # Print first 200 chars
        except requests.exceptions.RequestException as e:
            print(f"✗ Error fetching '{word}': {e}")
        except (IndexError, KeyError) as e:
            print(f"✗ Could not parse definition for '{word}': {e}")

    return list_with_defs

# TESTING: Load words from CSV, then get definitions
if __name__ == "__main__":

        # Load medical words
        words = load_word_list("medical_list.csv")
        print(f"\nLoaded words: {words[:5]}...\n")

        # Get definitions for those words and print
        words_with_defs = get_definitions(words)
        print(f"\nTotal words with definitions: {len(words_with_defs)}")

        """"# Load social studies words
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




