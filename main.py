import json
import time
from lib import Conversation


def display_choices(choices):
    """
    Takes a list of strings, and displays them
    as enumerated dialog options.
    """
    for choice in enumerate(choices):
        print(str(choice[0] + 1) + ": " + choice[1])


def say(npc_name, sentence):
    """
    Takes an npc's name and his/her dialog as
    strings, and prints them in a conversational
    format.
    """
    print(npc_name + ': ' + sentence)


def get_choice(choices, conversation):
    """
    Takes a list as input, corresponding element
    of that list after getting a valid integer input
    from player. Inputting 'debug' or 'd' prints
    debug information on the state of the conversation
    """
    user_choice = None
    while user_choice is None:
        try:
            user_input = input("Choice: ")
            if user_input == 'debug' or user_input == 'd':
                print(conversation.getDebugInfo())
            else:
                user_choice = int(user_input)
                if choices.__len__() < user_choice or user_choice < 1:
                    print('Error, try again')
                    user_choice = None
        except ValueError:
            print('Error, try again')
    return user_choice


if __name__ == '__main__':
    with open("database.json") as f:
        data = json.load(f)
    conversation = Conversation.Dialog(data)
    say('Cooper', conversation.getResponse())
    while conversation.is_active:
        choices = conversation.getAvailableActions()
        display_choices(choices)
        action_index = get_choice(choices, conversation) - 1
        say('Cooper', '...')
        time.sleep(1)
        conversation.submitAction(choices[action_index])
        say('Cooper', conversation.getResponse)
