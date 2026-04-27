from django.shortcuts import render
import csv
import os
import requests

# referenced: https://www.youtube.com/watch?v=NoLF7Dlu5mc
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
# ref: https://stackoverflow.com/questions/25688132/what-is-the-absolute-path-of-base-dir
from django.conf import settings 

list_options = {
    "1": ("custom_list.csv", "Custom"),
    "2": ("medical_list.csv", "Medical"),
    "3": ("social_studies_list.csv", "Social Studies")
}

# copied from loader.py
def load_word_list(filepath):
    words = []
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            if reader is None:
                print(f"Error: Could not read {filepath}")
                return []
            for row in reader:
                word = row.get('word', '').strip()
                definition = row.get("definition", "").strip()
                if word:
                    words.append({"word": word, "definition": definition})
        print(f"Loaded {len(words)} words from {filepath}")
        return words
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.")
        return []
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return []

# copied from main.py

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



@api_view(["GET"])
def get_word_lists(request):
    options = []
    for key, value in list_options.items():
        option = {"id": key, "name": value[1]}
        options.append(option)
    return Response({"lists":options})

@api_view(["POST"])
def load_words(request):
    list_type = request.data.get("list_type")

# ref for relative paths: https://stackoverflow.com/questions/63012796/change-base-directory-to-upper-directory-in-python
    if list_type == "custom":
        path = os.path.join(settings.BASE_DIR, "api", "data", "custom_list.csv")
    elif list_type == "medical":
        path = os.path.join(settings.BASE_DIR, "api", "data", "medical_list.csv")
    elif list_type == "socialstudies":
        path = os.path.join(settings.BASE_DIR, "api", "data", "social_studies_list.csv")    
    words = load_word_list(path)
    wordsanddefinitions = get_definitions(words)
    save_defs(path, wordsanddefinitions)
    return Response({
        "words": wordsanddefinitions
    })

@api_view(["POST"])
def guess_checker(request):
    correct_word = request.data.get("correct_word")
    guess = request.data.get("guess")

    feedback = check_guess(correct_word, guess)
    correct = True
    for i in feedback:
        if i != "G":
            correct = False
            break

    return Response({
        "feedback": feedback,
        "correct": correct
    })
