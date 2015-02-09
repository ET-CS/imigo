# imigo
Image Library

## Install
```
git clone https://github.com/ET-CS/imigo.git
cd imigo
```
Install requirements
```
pip install -r requirements.
``` 

edit `me` in translations abd compile the translations for use:
```
$ pybabel compile -d translations
```

make your `settings.ini` from `settings.ini.example`
```
cp settings.ini.example settings.ini
```
and edit the settings as you wish (port, language, etc)

## Run
Start server using `python run_server,py`.