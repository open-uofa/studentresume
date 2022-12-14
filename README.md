# studentresume


## Installation

Please first create a venv:

For windows users:

```console
python -m venv [VENV_NAME]
```

to activate:

```console
.\venv\scripts\activate
```

---

for linux/mac users

```console
virtualenv venv --python=python3
```

to activate:

```console
source venv/bin/activate
```


## Usage

## To generate a resume

```console
studentresume [OPTIONS] [RESUME_JSON] [THEME_JSON]
```

For a detailed help message and optional flags, please use:

```console
studentresume --help
```

## Additional info for contributors

Clone the repo:

```console
git clone git@github.com:open-uofa/studentresume.git
```

Navigate to the repo:

```console
cd studentresume
```

Install the package using [Poetry](https://python-poetry.org/) (preferred):

```console
poetry install
```

If authenticated to publish to pypi
```console
poetry publish --build
```

---

provided files:

sample.resume.json - a sample resume.json

schema.json - the schema for resume.json files

theme-schema.json - the schema for theme.json files

../themes/* - location of default theme files

requiredFields.json - required fields if required is true then field must exist with the listed fields being filled if required false if the field is present then the listed fields must be filled

---

studentresume stands on the backs of giants [ReportLab](https://docs.reportlab.com/reportlab/userguide), [Typer](https://typer.tiangolo.com/), [rich](https://docs.reportlab.com/reportlab/userguide), [JSON Resume](https://github.com/jsonresume), and [NerdFonts](https://www.nerdfonts.com/#home)

## License

This project is licenced under the terms of the MIT license
