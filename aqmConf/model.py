from subprocess import Popen, PIPE, DEVNULL
from urllib import request

class MainModel():
    def __init__(self, parent=None):
        self.baseURL = "https://github.com/felixslama/aqm"

    def build(self, configPath, releasePath):
        print("Build")
        #process = Popen(["platformio", "run", "-c", str(configPath), "-d", str(releasePath)], stdout=PIPE, stderr=PIPE, stdin=DEVNULL,)
        #(out, err) = process.communicate()

    def check(self):
        print("Check")

    def download(self):
        print("Check")