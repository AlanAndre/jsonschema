import json
import jsonschema
from jsonschema import validate
import os


def get_schema(schema_file):
    """This function loads the given schema available"""
    try:
        with open(f'schema/{schema_file}.schema', 'r') as file:
            schema_file = json.load(file)
        return schema_file
    except FileNotFoundError:
        print(f'{event}     No such schema file\n')


def validate_json(json_data, schema_name):
    """REF: https://json-schema.org/ """
    # Describe what kind of json you expect.
    execute_api_schema = get_schema(schema_name)
    try:
        validate(instance=json_data, schema=execute_api_schema)
    except TypeError:
        pass
    except jsonschema.exceptions.ValidationError as err:
        print(err)
        err = "Given JSON data is InValid"
        return False, err

    message = "Given JSON data is Valid"
    return True, message


def get_json(json_file):
    """Convert json to python object."""
    with open(f'event/{json_file}', 'r') as j_file:
        json_data = json.load(j_file)
        if json_data:
            json_event = json_data.get('event')  # what type of event
            json_data = json_data.get('data')
            return json_data, json_event
    return json_data, None


def validate_it(json_name):
    json_data = get_json(json_name)
    is_valid, msg = validate_json(json_data[0], json_data[1])
    print(f'{event}:    {msg}\n')


schemas = []
for _, _, i in os.walk('schema'):
    for schema in i:
        schemas.append(schema)

events = []
for _, _, i in os.walk('event'):
    for event in i:
        events.append(event)

for event in events:
    validate_it(event)
