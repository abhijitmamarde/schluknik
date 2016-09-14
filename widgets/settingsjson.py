import json

settings_json = json.dumps([
    {'type': 'bool',
     'title': 'smoker',
     'desc': 'do you want to be asked for cigarette count?',
     'section': 'example',
     'key': 'boolexample'},
    {'type': 'numeric',
     'title': 'age',
     'desc': 'Tell us your age',
     'section': 'example',
     'key': 'numericexample'},
    {'type': 'options',
     'title': 'gender',
     'desc': 'tell us your gender',
     'section': 'example',
     'key': 'optionsexample',
     'options': ['boy', 'girl']},
    {'type': 'string',
     'title': 'elias',
     'desc': 'set name to be displayed',
     'section': 'example',
     'key': 'stringexample'}])

