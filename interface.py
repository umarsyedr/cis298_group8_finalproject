import colorama
from colorama import Fore, Style
from utils import check_guess, is_valid_word


# Initialize colorama for cross-platform color support
colorama.init(autoreset=True)


# ref: https://pypi.org/project/colorama/

def display_menu():
    #Display main menu and get user choice
    print("\n" + "=" * 60)
    print("                      VOCABULARY QUIZ")
    print("=" * 60)
    print("\nChoose a word list:")
    print("  1 = Custom vocabulary")
    print("  2 = Medical vocabulary")
    print("  3 = Social Studies vocabulary")
    print("  4 = Quit")
    print("=" * 60)

    choice = input("\nEnter choice (1-4): ").strip()
    return choice


def get_list_name(choice):
    #Map choice to list filename and display name
    lists = {
        "1": ("custom_list.csv", "Custom"),
        "2": ("medical_list.csv", "Medical"),
        "3": ("social_studies_list.csv", "Social Studies")
    }
    return lists.get(choice, (None, None))


def display_start_message(list_name):

    messages = {
        "Custom": "Let's test your custom vocabulary! Ready to go? Let's do it!",
        "Medical": "Time to master some medical terms! You've got this!",
        "Social Studies": "Let's brush up on social studies! Show what you know!"
    }

    message = messages.get(list_name, "Let's get started!")
    print(f"\n {message}\n")


def display_word_prompt(question_num, definition, word_length):
    #Display the quiz prompt with definition and dashes
    print(f"\n{'=' * 60}")
    print(f"Question {question_num}")
    print(f"{'=' * 60}")
    print(f"\n Definition: {definition}")
    print(f"\n Word: {' _ ' * word_length}")
    print(f"\n ({word_length} letters)")
    print(f"{'=' * 60}\n")


def display_feedback(guess, feedback):
    """
    Display feedback with colors:
    G (Green) = correct letter, correct position
    Y (Yellow) = correct letter, wrong position
    X (Gray) = not in word
    """
    feedback_display = []

    for i in range(len(feedback)):
        letter = guess[i].upper()

        if feedback[i] == "G":
            # Green = correct position
            feedback_display.append(f"{Fore.GREEN}{letter}{Style.RESET_ALL}")
        elif feedback[i] == "Y":
            # Yellow = wrong position
            feedback_display.append(f"{Fore.YELLOW}{letter}{Style.RESET_ALL}")
        else:  # "X"
            # Gray = not in word
            feedback_display.append(f"{Fore.LIGHTBLACK_EX}{letter}{Style.RESET_ALL}")

    print("Your guess: " + " ".join(f"[{c}]" for c in feedback_display))


def check_if_correct(guess, secret_word):
    #Check if guess matches secret word
    return guess.lower() == secret_word.lower()


def display_result(word, won):
    #Display quiz result
    if won:
        print(f"\n{Fore.GREEN}✅ CORRECT! The word was: {word.upper()}{Style.RESET_ALL}\n")
    else:
        print(f"\n{Fore.RED}❌ Game Over! The word was: {word.upper()}{Style.RESET_ALL}\n")


def play_quiz(words_with_defs, scores, mode):
    #Main quiz loop
    total_words = len(words_with_defs)
    correct_count = 0
    quit_game = False

    if mode == "2":
        players = list(scores.keys())
        current_player_index = 0

    for question_num, item in enumerate(words_with_defs, 1):
        word = item["word"]
        definition = item["definition"]
        attempts = 5
        won = False
        guessed_letters = set()

        if mode == "2":
            current_player = players[current_player_index]
            print(f"\n {current_player}'s turn!")

        while attempts > 0:
            # Display prompt
            display_word_prompt(question_num, definition, len(word))
            print(f"Attempts remaining: {attempts}")
            print(f"Guessed letters: {', '.join(sorted(guessed_letters)) if guessed_letters else 'None'}")

            # Get user input
            guess = input("Your guess (or QUIT to exit): ").strip()

            # Check for quit
            if guess.upper() == "QUIT":
                if mode == "1":
                    print(
                        f"\n{Fore.CYAN}Thanks for playing! Final score: {correct_count}/{question_num - 1}{Style.RESET_ALL}\n")
                    return
                else:
                    quit_game = True
                    break

            # Validate input
            if not guess or len(guess) != len(word):
                print(f"{Fore.RED}Invalid! Guess must be {len(word)} letters.{Style.RESET_ALL}")
                continue

            if not is_valid_word(guess):
                print(f"{Fore.RED}Invalid word! Please use english words.{Style.RESET_ALL}")
                continue

            # Check if already guessed
            if guess.lower() in [g.lower() for g in guessed_letters]:
                print(f"{Fore.YELLOW}Already guessed that!{Style.RESET_ALL}")
                continue

            guessed_letters.add(guess)

            # Check if correct
            if check_if_correct(guess, word):
                display_result(word, True)
                correct_count += 1

                if mode == "2":
                    scores[current_player] += 1

                won = True
                break

            # Get feedback and display
            feedback = check_guess(word, guess)
            if feedback:
                display_feedback(guess, feedback)
                attempts -= 1
        if quit_game:
            break

        # If didn't win this round
        if not won:
            display_result(word, False)

        if mode == "2":
            current_player_index = (current_player_index + 1) % len(players)

        # Ask if continue
        if question_num < total_words:
            cont = input("Press ENTER to continue to next word...").strip()

    # Final summary
    print(f"\n{'=' * 60}")
    print(f"QUIZ COMPLETE!")
    print(f"{'=' * 60}")
    if mode =="2":
        for player, score in scores.items():
            print(f"{player}: {score}")

        winner = max(scores, key=scores.get)
        print(f"\n WINNNER: {winner}!!!")
    else:
        print(f"Score: {correct_count}/{total_words} ({int(correct_count / total_words * 100)}%)")
    print(f"{'=' * 60}\n")