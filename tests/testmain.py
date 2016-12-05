import unittest
import main

class testMethods(unittest.TestCase):

    def testDisplayChoices(self):
        choices = ["this is a choice", "this is another choice", "don't pick this, its garbo", "even more choice"]
        main.display_choices(choices)

    def testGetChoice(self):
        choices = ["this is a choice", "this is another choice", "don't pick this, its garbo", "even more choice"]
        choice = main.get_choice(choices)
        print('your choice was' + choice)
