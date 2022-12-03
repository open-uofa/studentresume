# studentresume

---

## installation

please first create a venv:

for windows users

```console
python -m venv [VENV_NAME]
```

to activate:

```console
venv\scripts\activate
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

---

after activating install requirements

for users:

```console
python -m pip install -r requirements.txt
```

for devs/contributors:

```console
python -m pip install -r requirements-dev.txt
```

---

## usage

## To generate a resume

```console
python run.py [OPTIONS] [RESUME_JSON] [THEME_JSON]
```

for a detailed help message and optional flags please use

```console
python run.py --help
```

---

## addintional info for contributors

studentresume stands on the backs of giants [ReportLab](https://docs.reportlab.com/reportlab/userguide), [Typer](https://typer.tiangolo.com/), [rich](https://docs.reportlab.com/reportlab/userguide), and [NerdFonts](https://www.nerdfonts.com/#home)

## License

---

This project is licenced under the terms of the MIT license
