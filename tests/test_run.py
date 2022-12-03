from typer.testing import CliRunner
import os.path

default_theme_path = os.path.join("studentresume", "themes", "default.json")
sample_resume_path = os.path.join("studentresume", "sample.resume.json")
one_page_resume = os.path.join("studentresume", "testonepage.resume.json")

from studentresume.run import app

runner = CliRunner()

def test_app_basic():
    result = runner.invoke(app, [sample_resume_path])
    assert result.exit_code == 0
    assert "Valid JSON" in result.stdout
    assert "Generating resume with sample.resume.json and style modern" in result.stdout
    result = runner.invoke(app, [])
    assert result.exit_code == 2
    assert "Invalid value: Requires a resume JSON file as an argument" in result.stdout
    
def test_app_theme():
    result = runner.invoke(app, [sample_resume_path, "--theme", "centered"])
    assert result.exit_code == 0
    assert "Valid JSON" in result.stdout
    assert "Generating resume with sample.resume.json and style centered" in result.stdout
    result = runner.invoke(app, [sample_resume_path, "--theme", "classic"])
    assert result.exit_code == 2
    assert "Invalid value for '--theme' / '-t': classic is not a supported default theme" in result.stdout
    
def test_app_page():
    result = runner.invoke(app, [one_page_resume, "--onepage"])
    assert result.exit_code == 0
    assert "Valid JSON" in result.stdout
    assert "restricting to one page" in result.stdout
    assert "Generating resume with testonepage.resume.json and style modern" in result.stdout
    
def test_app_invalid_json():
    result = runner.invoke(app, ["invalid.resume.json"])
    assert result.exit_code == 2
    assert "Invalid value: Resume JSON file not found" in result.stdout
    
def test_app_invalid_theme():
    result = runner.invoke(app, [sample_resume_path, "invalid.theme.json"])
    assert result.exit_code == 2
    assert "Invalid value: Theme JSON file not found" in result.stdout
    
def test_app_valid_theme():
    result = runner.invoke(app, [sample_resume_path, default_theme_path])
    assert result.exit_code == 0
    assert "Valid JSON" in result.stdout
    assert "Generating resume with sample.resume.json and style custom theme!" in result.stdout