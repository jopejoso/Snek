[ -d "builds/" ] && rm -rf builds/
mkdir -p builds/snekapp
cp snek.py builds/snekapp/__main__.py
python -m pip install -r requirements.txt --target builds/snekapp
rm -rf builds/snekapp/*.dist-info/
python -m zipapp -o builds/snek.pyz builds/snekapp
echo "color 7 & python snek.pyz & exit" > builds/snek.bat
