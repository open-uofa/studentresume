from json import loads
from rich import print
from typing import Optional
from pathlib import Path
import os.path
import typer

try:
    from json_validator import is_valid_resume, is_valid_theme
    from resume import Resume
except ImportError:
    from .json_validator import is_valid_resume, is_valid_theme
    from .resume import Resume


app = typer.Typer()

def get_file(file, is_package_file=True):
    if is_package_file:
        file = os.path.join(os.path.dirname(__file__), file)

    try:
        with open(file, encoding="utf8") as f:
            data = f.read()
            return data
    except FileNotFoundError:
        print("File not found")
        return 1

def theme_callback(value: str):
    if value != "modern" and value != "twocol" and value != "centered":
        raise typer.BadParameter(f"{value} is not a supported default theme")
    return value

#not sure if I did this right autocomplete isnt working for me
def complete_theme():
    return ["modern", "twocol", "centered"]


@app.command()
def main(resume_json: Path = typer.Argument(None, help="Path to resume JSON file"), 
         theme_json: Optional[Path] = typer.Argument(None, help="Path to JSON theme file"),
         theme: Optional[str] = typer.Option("modern", "--theme", "-t", 
                                             help="default theme name (modern, twocol, centered", 
                                             callback=theme_callback, shell_complete=complete_theme),
         onepage: bool = typer.Option(False, help="enforce single page resume")):
    if resume_json is None:
        raise typer.BadParameter("Requires a resume JSON file as an argument")
    if not resume_json.exists():
        print("[bold red]File not found[/bold red]")
        raise typer.BadParameter("Resume JSON file not found")
    if theme_json != None and not theme_json.exists():
        raise typer.BadParameter("Theme JSON file not found")
    resume_string = get_file(resume_json, False)
    if not is_valid_resume(resume_string):
        raise typer.BadParameter("Invalid JSON")
    print("[bold green]Valid JSON[/bold green]")
    resume = Resume(False)
    if theme == "modern" and theme_json == None:
        resume.apply_theme(loads(get_file(os.path.join("themes", "default.json"))))
    elif theme == "twocol":
        resume.apply_theme(loads(get_file(os.path.join("themes", "default3.json"))))
    elif theme == "centered":
        resume.apply_theme(loads(get_file(os.path.join("themes", "default2.json")))) 
    elif theme_json != None:
        theme = "custom theme!"
        if not is_valid_theme(theme_json.read_text()):
            raise typer.BadParameter("Invalid theme JSON")
        resume.apply_theme(loads(get_file(theme_json, False)))
    print("[bold green]restricting to one page[/bold green]") if onepage else None
    resume.set_page(1 if onepage else None)   
    print(f"[bold green]Generating resume with[/bold green][bold blue] {resume_json}[/bold blue][bold green] and style [/bold green][bold blue]{theme}[/bold blue]")
    resume.generate_resume(loads(resume_string))

if __name__ == "__main__":
    app()
    #typer.run(main)