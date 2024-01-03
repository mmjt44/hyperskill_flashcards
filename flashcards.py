# Write your code here
import json
import os
import random
from collections import OrderedDict
from io import StringIO
from operator import getitem
import argparse

parser = argparse.ArgumentParser()

sio = StringIO()


# Write your code here
def check_if_term_exists(term, flashcards):
    if term in flashcards:
        return True
    return False


def check_if_definition_exists(definition, flashcards):
    for item in flashcards.items():
        if definition in item[1]['definition']:
            return True
    return False


def get_term_for_definition(searched_definition, flashcards):
    for item in flashcards.items():
        if searched_definition == item[1]['definition']:
            return item[0]


def add_flashcard(flashcards):
    string = "The card:"
    print(string)
    sio.read()
    sio.write(string + '\n')
    term = input()
    sio.read()
    sio.write('> ' + term + '\n')
    while check_if_term_exists(term, flashcards):
        string = f"The card \"{term}\" already exists. Try again:"
        print(string)
        sio.read()
        sio.write(string + '\n')
        term = input()
        sio.read()
        sio.write('> ' + term + '\n')

    string = "The definition of the card:"
    print(string)
    sio.read()
    sio.write(string + '\n')
    definition = input()
    sio.read()
    sio.write('> ' + definition + '\n')
    while check_if_definition_exists(definition, flashcards):
        string = f"The definition \"{definition}\" already exists. Try again:"
        print(string)
        sio.read()
        sio.write(string + '\n')
        definition = input()
        sio.read()
        sio.write('> ' + definition + '\n')

    string = f"The pair (\"{term}\":\"{definition}\") has been added."
    print(string)
    sio.read()
    sio.write(string + '\n')

    new_card = {term: {'definition': definition, 'errors': 0}}
    if flashcards is None:
        flashcards = new_card
    else:
        flashcards.update(new_card)
    return flashcards


def remove_flashcard(flashcards):
    string = "Which card?"
    print(string)
    sio.read()
    sio.write(string + '\n')
    selected_card = input()
    sio.read()
    sio.write('> ' + selected_card + '\n')

    if check_if_term_exists(selected_card, flashcards):
        flashcards.pop(selected_card)
        string = "The card has been removed."
        print(string)
        sio.read()
        sio.write(string + '\n')
    else:
        string = f"Can't remove \"{selected_card}\": there is no such card."
        print(string)
        sio.read()
        sio.write(string + '\n')

    return flashcards


def export_flashcards(flashcards, filename=None):
    if filename is None:
        string = "File name:"
        print(string)
        sio.read()
        sio.write(string + '\n')
        filename = input()
        sio.read()
        sio.write('> ' + filename + '\n')
    with open(filename, "w") as fp:
        json.dump(flashcards, fp)

    string = f"{len(flashcards.keys())} cards have been saved."
    print(string)
    sio.read()
    sio.write(string + '\n')


def import_flashcards(flashcards, filename=None):
    string = "File name:"
    print(string)
    sio.read()
    sio.write(string + '\n')
    if filename is None:
        filename = input()
        sio.read()
        sio.write('> ' + filename + '\n')
    if os.path.exists(filename):
        with open(filename, "r") as fp:
            # Load the dictionary from the file
            imported_flashcards = json.load(fp)
        string = f"{len(imported_flashcards.keys())} cards have been loaded."
        print(string)
        sio.read()
        sio.write(string + '\n')
        if flashcards is None:
            flashcards = imported_flashcards
        else:
            flashcards.update(imported_flashcards)
        return flashcards
    else:
        string = "File not found"
        print(string)
        sio.read()
        sio.write(string + '\n')


def ask_flashcards(flashcards):
    string = "How many times to ask?"
    print(string)
    sio.read()
    sio.write(string + '\n')
    number_of_cards = int(input())
    sio.read()
    sio.write('> ' + str(number_of_cards) + '\n')
    for i in range(number_of_cards):
        term, definition = random.choice(list(flashcards.items()))
        string = f"print the definition of \"{term}\":"
        print(string)
        sio.read()
        sio.write(string + '\n')
        answer = input()
        sio.read()
        sio.write('> ' + answer + '\n')
        if flashcards[term]['definition'] == answer:
            string = "Correct!"
            print(string)
            sio.read()
            sio.write(string + '\n')
        elif check_if_definition_exists(answer, flashcards):
            correct_term = get_term_for_definition(answer, flashcards)
            string = f"Wrong. The right answer is \"{flashcards[term]}\", but your definition is correct for \"{correct_term}\"."
            print(string)
            sio.read()
            sio.write(string + '\n')
            # Update errors for card
            updated_card = {term: {'definition': flashcards[term]['definition'], 'errors': int(
                flashcards[term]['errors']) + 1}}
            flashcards.update(updated_card)
        else:
            string = f"Wrong. The right answer is \"{flashcards[term]['definition']}\"."
            print(string)
            sio.read()
            sio.write(string + '\n')
            # Update errors for card
            updated_card = {term: {'definition': flashcards[term]['definition'], 'errors': int(
                flashcards[term]['errors']) + 1}}
            flashcards.update(updated_card)
        i = i + 1


def log_answering(sio):
    string = "File name"
    print(string)
    sio.read()
    sio.write(string + '\n')
    log_filename = input()
    sio.read()
    sio.write('> ' + log_filename + '\n')
    with open(log_filename, mode='w') as f:
        f.write(sio.getvalue())
    string = "The log has been saved."
    print(string)
    sio.read()
    sio.write(string + '\n')


def get_hardest_card(flashcards):
    # using OrderedDict() + sorted()
    # Sort nested dictionary by key
    result = OrderedDict(sorted(flashcards.items(),
                                key=lambda x: getitem(x[1], 'errors'),
                                reverse=True))

    # select first row - highest errors
    term_list = []
    if len(result) > 0:
        error_number = int(list(result.items())[0][1]['errors'])
        if error_number > 0:
            for key, value in result.items():
                if value['errors'] == error_number:
                    term_list.append(key)

            if len(term_list) == 1:
                string = f"The hardest card is \"{term_list[0]}\". You have {error_number} errors answering it."
            elif len(term_list) > 1:
                list_of_terms = ','.join(f'"{w}"' for w in term_list)
                string = f"The hardest card are {list_of_terms}"

            print(string)
            sio.read()
            sio.write(string + '\n')
        else:
            string = "There are no cards with errors."
            print(string)
            sio.read()
            sio.write(string + '\n')
    else:
        string = "There are no cards with errors."
        print(string)
        sio.read()
        sio.write(string + '\n')


def reset_stats(flashcards):
    for item in flashcards.items():
        updated_flashcard = {
            item[0]: {'definition': item[1]['definition'], 'errors': 0}}
        flashcards.update(updated_flashcard)

    string = "Card statistics have been reset."
    print(string)
    sio.read()
    sio.write(string + '\n')


if __name__ == '__main__':
    flashcards = {}
    export_to = None
    parser.add_argument("--import_from")
    parser.add_argument("--export_to")

    args = parser.parse_args()

    if args.import_from is not None:
        import_from = args.import_from
        import_flashcards(flashcards, filename=import_from)

    if args.export_to is not None:
        export_to = args.export_to


    while True:
        sio.read()
        string = "Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):"
        print(string)
        sio.write(string + '\n')
        action = input()
        sio.read()
        sio.write('> ' + action + '\n')
        if action == "exit":
            string = "Bye bye!"
            print(string)
            sio.read()
            sio.write(string + '\n')
            if export_to is not None:
                export_flashcards(flashcards, filename=export_to)

            break

        if action == "add":
            flashcards = add_flashcard(flashcards)
            continue

        if action == "remove":
            flashcards = remove_flashcard(flashcards)
            continue

        if action == "export":
            export_flashcards(flashcards)
            continue

        if action == "import":
            flashcards = import_flashcards(flashcards)
            continue

        if action == "ask":
            ask_flashcards(flashcards)
            continue

        if action == "log":
            log_answering(sio)
            continue

        if action == 'hardest card':
            get_hardest_card(flashcards)
            continue

        if action == 'reset stats':
            reset_stats(flashcards)
            continue
