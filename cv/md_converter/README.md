# Markdown Resume converter

This tool allows you to build/maintain your resume in a Markdown file, and then generate HTML or PDF file from it.  
Sample CV/resume is kept in CV.md file.  
Styles are ensured by styles.css file which are applied to output HTML and affect resulting PDF.  
If needed to add metadata/tags (which theoretically can be scanned by ATS and can be used to add extra data which is not mentioned in the CV text) to the output PDF file, metadata.txt should be provided. Currently only 3 fields are supported: `Title`, `Author`, `Keywords`.  
You can use custom output directory, CSS file name, metadata file name, just run the script without arguments to get help.

# How to get started

1. Edit CV.md file.
2. Adjust styles.css if needed.
3. Adjust metadata.txt if needed.
4. Setup the environment (below).
5. Run md_converter.py to generate output HTML and PDF (which by default are saved to `output` directory).

# Pre-requisites

Download or install latest [wkhtmltopdf](https://wkhtmltopdf.org/downloads.html) and copy .exe inside the directory (or create a symlink).

# Setting environment and generating output with VS Code

1. Download and install latest [python](https://www.python.org/downloads/), it also should provide latest `pip` version.
2. Open current directory (cv/md_converter) in VS Code.
3. Install Python [VS Code extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python).
4. Create Python environment
- `Ctrl + Shift + P` -> `Python: Create environment...`
- Choose `Venv`.
- Choose path to your installed Python version.
- Choose and **mark** `cv\requirements.txt`
- Open VS Code console `Ctrl + ~`, it will be inside created virtual environment.
- If, for some reason, `pip list` doesn't show any other packages except `pip` itself (which meanst that VS Code didn't restore requirements.txt), install packages manually: `pip install -r requirements.txt`
- Now you can press `F5` or `Ctrl + F5` to generate the output files.

# Setting environment and generating output in the commandline

1. Download and install latest [python](https://www.python.org/downloads/), it also should provide latest `pip` version.
2. Open command line inside the directory.
3. Create Python environment `python -m venv .venv`
4. Activate the environment `.venv\Scripts\activate`
5. Install required pip packages `pip install -r requirements.txt`
6. Generate output files

```
python.exe .\md_converter.py .\CV.md
```