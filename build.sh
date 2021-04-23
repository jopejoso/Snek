[ -d "snekapp" ] && rm -rf snekapp
mkdir snekapp
cp snek.py snekapp/__main__.py
python -m pip install -r requirements.txt --target snekapp
rm -rf snekapp/*.dist-info/
python -m zipapp snekapp
