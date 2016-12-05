class Dialog:
    def __init__(self, data):
        """
            Takes the conversation data structure created using json.load()
        """
        pass
    
    def getAvailableActions(self):
        """
            Returns a list of strings with the names of available actions
        """
        pass
    
    def submitAction(self, action):
        """
            Takes an action as a string and executes it if valid
        """
        pass
    
    def getResponse(self):
        """
            Returns the AI's current string response
        """
        pass
    
    def getDebugInfo(self):
        pass