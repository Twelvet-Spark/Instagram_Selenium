import configparser

class ConfigFile:
    def __init__(self, filename):
        self.filename = filename
        self.settings = []
        self.parameters = []
        self.parser = configparser.ConfigParser()

    def getConfigInfo(self, sectionName, keyName):
        self.parser.read(self.filename)
        self.settings = self.parser[f"{sectionName}"]
        for i in range(0, len(keyName)):
            self.parameters.append(self.settings[f"{keyName[i]}"])
        return self.parameters