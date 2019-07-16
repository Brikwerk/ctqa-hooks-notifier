CD /D %~dp0

python -m pip install virtualenv
python -m virtualenv venv

call "venv/Scripts/activate"
pip install -r requirements.txt

python setup.py