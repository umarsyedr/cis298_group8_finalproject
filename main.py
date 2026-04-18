import requests

# ref: https://www.w3schools.com/python/ref_requests_post.asp
# api ref: https://github.com/meetDeveloper/freeDictionaryAPI
def get_definitions(word_list):
    list_with_defs = []
    for word in word_list:
        # put this in env later, although the documentation doesn't say too.
        base_url = "https://api.dictionaryapi.dev/api/v2/entries/en/"
        response = requests.get(f"{base_url}{word}")
        data = response.json()
        definition = (data[0]["meanings"][0]["definitions"][0]["definition"])
        list_with_defs.append({"word": word, "definition": definition})
        print(list_with_defs)
# TESTING GET_DEFINITIONS
# example_words = ["Cool", "Apple"]
# print(get_definitions(example_words))