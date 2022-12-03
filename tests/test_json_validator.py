from studentresume.json_validator import is_valid_resume, is_valid_theme

import os.path

sample_resume_path = os.path.join("studentresume", "sample.resume.json")
default_theme_path = os.path.join("studentresume", "themes", "default.json")


def test_is_valid_resume():
    
    # test with sample resume
    with open(sample_resume_path, encoding="utf8") as f:
        json_string = f.read()
    assert is_valid_resume(json_string) is True

    # test with non-json string
    invalid_json = "This is not valid json"
    assert is_valid_resume(invalid_json) is False

    # test with valid json but not a resume
    invalid_resume_json = "{ 'name': 'John Doe' }"
    assert is_valid_resume(invalid_resume_json) is False

def test_is_valid_theme():

    # test with sample theme
    with open(default_theme_path, encoding="utf8") as f:
        json_string = f.read()
    assert is_valid_theme(json_string) is True

    # test with non-json string
    invalid_json = "This is not valid json"
    assert is_valid_theme(invalid_json) is False

    # test with valid json but not a theme
    invalid_theme_json = "{ 'name': 'John Doe' }"
    assert is_valid_theme(invalid_theme_json) is False