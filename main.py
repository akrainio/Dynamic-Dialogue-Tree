import json
import time
from lib import Conversation


def display_choices(choices):
    for choice in enumerate(choices):
        print(str(choice[0] + 1) + ": " + choice[1])

def say(string):
    print('Cooper: ' + string)

def get_choice(choices):
    user_choice = None
    while user_choice is None:
        try:
            user_input = input("How would you like to respond?")
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
    say(conversation.getResponse())
    while conversation.is_active:
        choices = conversation.getAvailableActions()
        display_choices(choices)
        action_index = get_choice(choices) - 1
        say('...')
        time.sleep(1)
        conversation.submitAction(choices[action_index])
        say(conversation.getResponse)
