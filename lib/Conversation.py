import math

#TODO: Split into multiple files maybe

class Helpers:
    """
        
    """
    #TODO: implement helpers
    def __init__(self):
        pass
    
class Personality:
    """
        Contains the set of available NPC personalities along with the currently selected one
    """
    def __init_(self):
        self.personalities = {}
        self.selected = ""
    
    def parse(self, data):
        for name, values in data.items():
            if 
    
    def apply(self, values):
        """
            Apply personality modifiers to NPC state values
        """
        pass

class WorkingMemory:
    """
        Represents the current working memory for the dialog
        Includes used actions, NPC state, and unlocked social cues
    """
    def __init__(self):
        self.usedActions = set()
        self.npcState = {}
        self.cues = set()
        
    def parse(self, data):
        """
            Parse working memory from json data
        """
        try:
            self.npcState = data["state"]
            self.cues = set(data["cues"])
        except KeyError:
            print("Error while parsing working memory.")
            return False
        return True
    
    def addUsedAction(self, action):
        """
            Mark given action as used
        """
        self.usedActions.add(action)
    
    def adjustState(self, state, value):
        """
            Adjust given state by value while keeping it normalized
        """
        self.npcState[state] = min(1, max(0, self.npcState[state] + value))
        
    def addCue(self, cue):
        """
            Add given social cue to unlocked set
        """
        self.cues.add(cue)

class Response:
    """
        Represents a possible NPC response to a player action
    """
    def __init__(self):
        self.text = ""
        self.value = "0"
        self.unlockedCues = []
        
    def parse(self, data):
        """
            Parse response from json data
        """
        try:
            self.text = data["text"]
            self.value = data["value"]
            self.unlockedCues = data["cues"]
        except KeyError:
            print("Error while parsing responses.")
            return False
        return True
        
    def getValue(self, wme):
        """
            Evaluates this response based on the NPC's state
        """
        return eval(self.value, {"__builtins__" : None }, wme.npcState)

class Action:
    """
        Represents a player action
    """
    def __init__(self):
        self.text = ""
        self.requiredCues = []
        self.canRepeat = False
        self.helpers = []
        self.responses = []
    
    def parse(self, data):
        """
            Parse action from json data
        """
        try:
            self.text = data["text"]
            self.requiredCues = data["cues"]
            self.canRepeat = data["canRepeat"] == "True"
            self.helpers = data["helpers"]
            self.responses = []
            for responseData in data["responses"]:
                newResponse = Response()
                if newResponse.parse(responseData):
                    self.responses.append(newResponse)
                else:
                    return False
        except KeyError:
            print("Error while parsing action.")
            return False
        
        return True
    
    def canPerform(self, wme):
        """
            Check this action can be performed
        """
        # check for required social cues
        for requiredCue in self.requiredCues:
            if not requiredCue in wme.cues:
                return False
        
        # check for action repeat
        if self in wme.usedActions and not self.canRepeat:
            return False
        
        return True
    
    def perform(self, wme):
        """
            Perform this action if possible
        """
        # check action can be performed
        if self.canPerform(wme):
            #TODO: adjust npc state using helpers and personality
            
            # add action to set of used actions
            wme.addUsedAction(self)            
            
            # choose most appropriate response using eval
            bestResponse = None
            bestResponseValue = -math.inf
            for response in self.responses:
                value = response.getValue(wme)
                if value > bestResponseValue:
                    bestResponse = response
                    bestResponseValue = value
            
            # add response's unlocked social cues
            for unlockedCue in bestResponse[0].unlockedCues:
                wme.addCue(unlockedCue)
            
            # return response text
            return bestResponse[0].text

class Dialog:
    """
        Represents a dialog between an NPC and the player
    """
    def __init__(self, data):
        """
            Takes the dialog data structure created using json.load()
        """
        self.active = True        
        
        try:
            self.wme = WorkingMemory()
            if not self.wme.parse(data["Start"]):
                self.active = False
            
            self.actions = []
            for actionData in data["Actions"]:
                newAction = Action()
                if newAction.parse(actionData):
                    self.actions.append(newAction)
                else:
                    self.active = False
            
            self.response = data["Opening"]
        except KeyError:
            print("Error while parsing dialog.")
            self.active = False
        
        self.__updateAvailableActions()
        
    def __updateAvailableActions(self):
        self.availableActions = {}
        for action in self.actions:
            if action.canPerform(self.wme):
                self.availableActions[action.text] = action
        
    def isActive(self):
        """
            Returns True if the dialog is ongoing
        """        
        return self.active
    
    def getAvailableActions(self):
        """
            Returns a list of strings with the names of available actions
        """
        return self.availableActions.keys()
    
    def submitAction(self, action):
        """
            Takes an action as a string and executes it if valid
        """
        if not action in self.availableActions:
            return False
        
        chosenAction = self.availableActions[action]
        
        if not chosenAction.canPerform(self.wme):
            return False
        
        self.response = chosenAction.perform(self.wme)
        self.__updateAvailableActions()
        return True
    
    def getResponse(self):
        """
            Returns the AI's current string response
        """
        return self.response
    
    def getDebugInfo(self):
        """
            Returns dialog debugging information
        """
        #TODO: implement debug info
        return ""