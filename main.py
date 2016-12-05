import json
from alpha.lib import Conversation
if __name__ == '__main__':
    with open("database.json") as f:
        data = json.load(f)
    conversation = Conversation.Dialog(data)
