#!/usr/bin/env python
from flask import Flask
app = Flask(__name__)
import ConfigParser

def ConfigSectionMap(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1

Config = ConfigParser.ConfigParser()
Config.read("settings.ini")
_port = ConfigSectionMap("Server")['port']
_host = ConfigSectionMap("Server")['host']
_debug = ConfigSectionMap("Server")['debug']=="True"

@app.route("/")
def hello():
    return "Hello World!"
    
if __name__ == "__main__":
    app.run(host=_host, port=int(_port), debug=_debug)