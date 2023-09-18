# To activate venv:
. .venv/bin/activate
source venv/bin/activate #works too
current env: myenv/bin/activate

# To actually start server:
gunicorn run:app

# to start pytest
pytest

# to run pytest with code coverage
coverage run -m pytest
coverage report -m
