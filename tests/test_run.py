from typer.testing import CliRunner
import os.path

default_theme_path = os.path.join("studentresume", "themes", "default.json")

from studentresume.run import app

runner = CliRunner()

def test_app_basic():
    result = runner.invoke(app, ["sample.resume.json"])
    assert result.exit_code == 0
    assert "Valid JSON" in result.stdout
    assert "Generating resume with sample.resume.json and style modern" in result.stdout
    result = runner.invoke(app, [])
    assert result.exit_code == 2
    assert "Invalid value: Requires a resume JSON file as an argument" in result.stdout
    
def test_app_theme():
    result = runner.invoke(app, ["sample.resume.json", "--theme", "centered"])
    assert result.exit_code == 0
    assert "Valid JSON" in result.stdout
    assert "Generating resume with sample.resume.json and style centered" in result.stdout
    result = runner.invoke(app, ["sample.resume.json", "--theme", "classic"])
    assert result.exit_code == 2
    assert "Invalid value for '--theme' / '-t': classic is not a supported default theme" in result.stdout
    
def test_app_page():
    result = runner.invoke(app, ["testonepage.resume.json", "--onepage"])
    assert result.exit_code == 0
    assert "Valid JSON" in result.stdout
    assert "restricting to one page" in result.stdout
    assert "Generating resume with testonepage.resume.json and style modern" in result.stdout
    
def test_app_invalid_json():
    result = runner.invoke(app, ["invalid.resume.json"])
    assert result.exit_code == 2
    assert "Invalid value: Resume JSON file not found" in result.stdout
    
def test_app_invalid_theme():
    result = runner.invoke(app, ["sample.resume.json", "invalid.theme.json"])
    assert result.exit_code == 2
    assert "Invalid value: Theme JSON file not found" in result.stdout
    
def test_app_valid_theme():
    theme = str(os.path.join("themes", "default.json"))
    print(default_theme_path)
    result = runner.invoke(app, ["sample.resume.json", default_theme_path])
    assert result.exit_code == 0
    assert "Valid JSON" in result.stdout
    assert "Generating resume with sample.resume.json and style custom theme!" in result.stdout