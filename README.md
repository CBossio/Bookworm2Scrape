<p align="center">
    <img src="img/Bookworm.png" alt="logo" />
</p>
<h1 align="center">Bookworm2Scrape Setup Guide 📖🐛</h1>

Follow these steps to set up the project on your local machine.

## Prerequisites

- **Python 3.12.6** (or install it if you don’t have it: [https://www.python.org/downloads/](https://www.python.org/downloads/))
- **Git** installed (Download from [https://git-scm.com/](https://git-scm.com/))

## Installation

1. **Create a project folder**  
   Create a folder anywhere on your system to hold the project files.

2. **Open a terminal and navigate to your folder**  
   ```bash
   cd your/path/to/the/folder

3. **Clone the repo**
   ```bash
   git clone https://github.com/CBossio/Bookworm2Scrape.git

4. **Create an enviroment**
   ```bash
   python -m venv venv

5. **Enter the project folder**
   ```bash
   cd Bookworm2Scrape

6. **Activate the enviroment**
   ```bash
   venv\Scripts\activate

7. **Check isolated Python**
   ```bash
   where python

8. **Install dependencies**
   ```bash
   pip install -r requirements.txt

## Execute extraction
### Airflow

### Jupyter
<img src="img/code_preview_etl.png" alt="logo" />
<p> The process its pretty straight foward, you should run all the cells in order<p>

### Quickfixes & Notes
<p> In case of having multiple log errors in the "failed_urls_library" or "failed_urls_book"
You should modify in the setting.py the Proxies, the log shows which is the one struggling</p>

<p> Sometimes the code throws a random error of charmap codec, but it doesent affect the code</p>

## Execute reporting
### Airflow

### Jupyter
<img src="img/code_preview_reporting.png" alt="logo" />
<p> The same as the extraction process, you should run all the cells in order<p>




