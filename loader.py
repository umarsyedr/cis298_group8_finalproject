import csv

# ref: https://docs.python.org/3/library/csv.html

def load_word_list(filepath):
    # Load words from a CSV file
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
