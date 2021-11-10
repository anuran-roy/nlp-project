# Offline speech recognition-enabled assistant

This is a simple offline voice recognition-based assistant purely built on Python3. It uses Vosk as the backend. A wrapper **s2t_class.py** has been implemented from scratch that recognizes text from speech using Vosk APIs. The main app **excelmod.py** contains the functions required to make the voice commands work. The file **config.yaml** maps the commands to their respective functions as a collection of key-value pairs. The corresponding keywords then trigger their respective functions.

## 3rd party modules used

1. [Vosk API by Alphacephei](https://github.com/alphacep/vosk-api)
2. [Vosk small American English model](http://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip)
3. OpenPyXL

## How to use

1. Clone the repository.
2. (Optional but recommended) Create a virtual environment using *venv* or *virtualenv*.
3. Install dependencies using ``pip install -r requirements.txt``
5. Run ``python excelmod.py``
6. Enjoy!
