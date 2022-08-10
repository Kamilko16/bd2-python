import os
import pickle


# class Save():
#     def saveData(self, data):
#         f = open('save.data', 'wb')
#         pickle.dump(data, f)
#
#     def readData(self):
#         f = open('save.data', 'rb')
#         return bytearray(f.read())

class Scores():
    def __init__(self):
        self.scores = []
        self.readScores()

    def sort(self):
        def x(e):
            return e[1]

        self.scores.sort(reverse=True, key=x)

    def addScore(self, score):
        self.scores.append(score)
        self.sort()
        self.saveScores()


    def readScores(self):
        if os.path.exists('scores.data'):
            f = open('scores.data', 'rb')
            self.scores = pickle.load(f)
            f.close()

    def saveScores(self):
        f = open('scores.data', 'wb')
        pickle.dump(self.scores, f)
        f.close()


class Settings():
    def __init__(self):
        self._settings_default = {'music_volume': 100, 'effects_volume': 100}
        self._settings = {}
        self.readSettings()

    def writeSettings(self):
        f = open('settings.ini', 'w')
        for setting in self._settings:
            f.write(setting + '=' + str(self._settings[setting]) + '\n')
        f.close()

    def readSettings(self):
        if not os.path.exists('settings.ini'):
            self._settings = self._settings_default.copy()
            self.writeSettings()
        else:
            f = open('settings.ini', 'r')
            lines = f.read().split('\n')
            lines.pop()
            for line in lines:
                setting = line.split('=')
                if setting[1].isnumeric():
                    self._settings[setting[0]] = int(setting[1])
                else:
                    self._settings[setting[0]] = setting[1]
            f.close()

    def getSetting(self, name):
        if self._settings.get(name) is None:
            self._settings[name] = self._settings_default[name]
        return self._settings[name]

    def setSetting(self, name, value):
        self._settings[name] = value
