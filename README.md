## Pre-run
Like all Python project, this tool requires installing it's dependancies.
To do this, simply run
```
pip install -r requirements.txt
```
Further, in order for the tool to run correctly, Tesseract must be installed.

## Installing Tesseract on Windwos
1. Install tesseract using windows installer available at: https://github.com/UB-Mannheim/tesseract/wiki

2. Note the tesseract path from the installation.Default installation path at the time the time of this edit was: C:\Users\USER\AppData\Local\Tesseract-OCR. It may change so please check the installation path.

3. pip install pytesseract

4. Set the tesseract path in the script before calling image_to_string:

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\USER\AppData\Local\Tesseract-OCR\tesseract.exe'

## Runing the project
Once the dependancies have been installed, running this program is as simple as 
```
python analyze.py <filename>
```