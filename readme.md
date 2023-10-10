# setup
1. activate your python env (3.10+)
1. `poetry install` in this repo
    - `pip install poetry` if don't have poetry
1. in `config` dir, make a copy of one of the yml files, based on your system. **name it `config.yml`**, in the same folder
2. edit the config file to point to your desired paths

# usage
in `bin` folder, `python sync.py`. the correct action will be selected based on your configuration