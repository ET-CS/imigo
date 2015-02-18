#!/usr/bin/env python
import os
from os import listdir
import glob
import ntpath

from flask import Flask, render_template, request
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

apppath = os.path.dirname(os.path.abspath(__file__))
library = apppath +'/static/library/'

@app.route("/")
def index():
    item = request.args.get('item', '')
    return get_folder(item)

def get_folder(subfolder=''):
    item = library + subfolder 
    if os.path.isfile(item):
	path = ntpath.basename(subfolder)
	path = library+subfolder.replace(path, "")[1:] + '*.jpg'
	rpath = '/static/library/'+subfolder.replace(path, "")[1:] + '*.jpg'
	others = []
	for g in glob.glob(path):
	    item = {}
	    item['name'] = ntpath.basename(g)
	    item['url']='/'+g.replace(library, '')
	    item['full']=g.replace(apppath, '')
	    item['thumb']=item['full'].replace(".jpg", ".thumb.png")
	    others.append(item)
	others = sorted(others, key=lambda item: item['name'])
	return render_template('item.html', item=subfolder, others=others)
    folder = item + '/'
    lib = []
    for f in listdir(folder):
	if not (f=='README.md' or f=='.gitignore' or f=='create_thumbs.sh' or f.endswith('.thumb.png')):
	    item = {}
	    item['name'] = f
	    item['rname'] = subfolder +'/' + f
	    if os.path.isfile(folder+f):
		item['path'] = subfolder + '/' + f
		item['path'] = item['path'].replace('.jpg', '.thumb.png')
	    if os.path.isdir(folder+f):
		for name in glob.glob(folder+f+'/*.thumb.png'):
		    item['thumb'] = ntpath.basename(name)
		    item['path'] = subfolder + f + '/' + item['thumb']
		    break
		if not 'path' in item:
		    for name in glob.glob(folder+f+'/*.jpg'):
			item['thumb'] = ntpath.basename(name)
			item['path'] = subfolder + f + '/' + item['thumb']
		        break
	    lib.append(item)
    # sort
    lib = sorted(lib, key=lambda item: item['name'])
    return render_template('index.html', folder=lib)

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