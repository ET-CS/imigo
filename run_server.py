#!/usr/bin/env python
from flask import Flask, render_template
from flask.ext.babel import Babel, gettext, ngettext

app = Flask(__name__)
#app.config.from_pyfile('mysettings.cfg')
babel = Babel(app)

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
_rtl = ConfigSectionMap("UI")['rtl']=="True"
_header_background = ConfigSectionMap("UI")['header-background']
_header_logo = ConfigSectionMap("UI")['header-logo']
_header_logo_href = ConfigSectionMap("UI")['header-logo-href']
_footer_url = ConfigSectionMap("Copyright")['url']
_footer_year = ConfigSectionMap("Copyright")['year']
app.config['BABEL_DEFAULT_LOCALE'] = ConfigSectionMap("UI")['lang']
from flask.ext.babel import refresh; refresh()

@app.route("/")
def index():
    return render_template('index.html')

@app.context_processor
def inject_user():
    #, home=gettext(u'Home')
    return dict(
	rtl=_rtl,
	hbg=_header_background,
	hlogo=_header_logo,
	hlogohref=_header_logo_href,
	footer_url=_footer_url,
	footer_year=_footer_year
    )
    
if __name__ == "__main__":
    app.run(host=_host, port=int(_port), debug=_debug)