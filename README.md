# AssetMappr-BE

## Linting:
Install autopep8
```bash
pip install autopep8
pip install pylint
```
To lint a file use:
```bash
autopep8 --in-place --aggressive --aggressive <filename>
```
To check linting issues:
```bash
pylint <filename>
```

## DB Initialization
Fetch and Save Asset Information
```bash
python ./db_init/fetch_and_save_assets.py
```
Create and populate database
```bash
python ./db_init/db_utils.py
```
Note: Mind the relative path.