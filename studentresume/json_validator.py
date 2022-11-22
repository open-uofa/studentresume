"""
Todo:
    * Differentiate between invalid json and invalid json resume, ValidationError and SchemaError
    * Create separate functions for cli validation and api validation (which returns a json response)
    * Create more helpful error messages based on our decided optional vs required fields
"""
import json
import os.path

from jsonschema import validate


def _is_valid_json(json_string: str) -> bool:
    """
    Returns True if the json_string is valid json, False otherwise.
    """
    try:
        json.loads(json_string)
    except ValueError as e:
        print(e)
        return False
    return True


def is_valid_resume(json_string: str) -> bool:
    """
    Returns True if the json_string is a valid json resume as defined
    in the schema file, False otherwise.
    """
    schema_file = os.path.join(os.path.dirname(__file__), "schema.json")
    with open(schema_file, encoding="utf8") as f:
        schema = json.load(f)

    if _is_valid_json(json_string):
        try:
            validate(json.loads(json_string), schema)
        except Exception as e:
            print(e)
            return False
        return True
    return False



if __name__ == '__main__':
    """
    Test that sample.resume.json is a valid json resume (which it should be)
    """
    with open("sample.resume.json", encoding="utf8") as f:
        json_string = f.read()
    print(is_valid_resume(json_string))

