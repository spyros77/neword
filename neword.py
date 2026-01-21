import json
import os
import random

FILENAME = "dictionary.json"

def load_dictionary():
    if os.path.exists(FILENAME):
        with open(FILENAME, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_dictionary(dictionary):
    with open(FILENAME, "w", encoding="utf-8") as f:
        json.dump(dictionary, f, ensure_ascii=False, indent=2)

def quiz_meaning_order(dictionary):
    if not dictionary:
        print("Dictionary empty — add words first.")
        return

    try:
        n = int(input("How many words to quiz on? ").strip())
    except ValueError:
        print("Please enter a valid number.")
        return

    words = list(dictionary.keys())
    random.shuffle(words)

    if n > len(words):
        print(f"Only {len(words)} words available — using all.")
        n = len(words)

    selected = words[:n]
    
    # Get meanings and shuffle them
    meanings = [dictionary[w] for w in selected]
    random.shuffle(meanings)

    print("\n=== Match the meanings to the correct words ===")
    
    # Show the meanings with indices
    for idx, m in enumerate(meanings, start=1):
        print(f"{idx}. {m}")

    score = 0
    print("\nEnter the number of the meaning that matches each word:")

    for w in selected:
        print(f"\nWord: {w}")
        try:
            choice = int(input("Meaning number: ").strip())
        except ValueError:
            print("Invalid — must be a number.")
            continue

        # Validate range
        if 1 <= choice <= len(meanings):
            chosen_meaning = meanings[choice - 1]
            if chosen_meaning == dictionary[w]:
                print("✔ Correct!")
                score += 1
            else:
                print(f"✘ Wrong. Correct meaning: {dictionary[w]}")
        else:
            print("Invalid number — out of range.")

    print("\n=== Quiz Results ===")
    print(f"You matched correctly {score}/{n} words.")

def main():
    dictionary = load_dictionary()
    print("=== Enhanced Dictionary Program ===")

    while True:
        print("\nOptions:")
        print("1. Add a word")
        print("2. Lookup a word")
        print("3. Edit a meaning")
        print("4. Delete a word")
        print("5. Show all words")
        print("6. Quiz mode (match meanings)")
        print("7. Exit")

        choice = input("Choose 1–7: ").strip()

        if choice == "1":
            word = input("Word to add: ").strip().lower()
            meaning = input("Meaning: ").strip()
            dictionary[word] = meaning
            save_dictionary(dictionary)
            print(f"Added: {word} → {meaning}")

        elif choice == "2":
            word = input("Word to lookup: ").strip().lower()
            if word in dictionary:
                print(f"{word} : {dictionary[word]}")
            else:
                print(f"'{word}' not found.")

        elif choice == "3":
            word = input("Word to edit: ").strip().lower()
            if word in dictionary:
                print(f"Current meaning: {dictionary[word]}")
                new_meaning = input("New meaning: ").strip()
                dictionary[word] = new_meaning
                save_dictionary(dictionary)
                print(f"Updated: {word} → {new_meaning}")
            else:
                print(f"'{word}' not in dictionary.")

        elif choice == "4":
            word = input("Word to delete: ").strip().lower()
            if word in dictionary:
                confirm = input(f"Delete '{word}'? (y/n): ").strip().lower()
                if confirm == "y":
                    del dictionary[word]
                    save_dictionary(dictionary)
                    print(f"Deleted '{word}'.")
            else:
                print(f"'{word}' not found.")

        elif choice == "5":
            if not dictionary:
                print("Dictionary is empty.")
            else:
                print("Words in dictionary:")
                for w, m in dictionary.items():
                    print(f"{w} : {m}")

        elif choice == "6":
            quiz_meaning_order(dictionary)

        elif choice == "7":
            print("Goodbye!")
            break

        else:
            print("Invalid choice — try 1–7.")

if __name__ == "__main__":
    main()