# One Time Setup
Only Do this once per device you do not need to do this once it is setup. 

### **Step 1:** Install Python
Go to the python website and download the installer and install python. Do the latest version (3.12ish) and go through the options for it. For any options that says Add pip or Add to path, check that box. You can Add Idle too if you want to write or modify code. 

After Installing you can test python by opening Idle and do `print("hello world")`

### **Step 2:** Env vars 
Setup your env vars, type in edit env and click edit env vars for your account. Select Path and then click Edit, Click New and paste in the path of where you have pip installed. I have it in here `C:\Users\zashams\AppData\Local\Programs\Python\Python312\Scripts\pip` (this is what I have pasted), simply just add your username instead of mine, zashams -> your username. Check also whether pip.exe file is there too via file explorer. 

Click OK

Add more env vars, click New instead of Edit this time, and add these variables:
- `PIP_DEFAULT_TIMEOUT` = `1000`
- `PIP_NO_CACHE_DIR` = `false`
- `PIPENV_INSTALL_TIMEOUT` = `9999`
- `NO_PROXY` = `localhost,127.0.0.1`
- `HTTP_PROXY` = ``
- `HTTPS_PROXY` = ``

put `PIP_DEFAULT_TIMEOUT` as variable name and `1000` as value and click OK, Do the same for all ther other variables. 

Download the `nc-colb-cert.pem` cert and put it in a folder and copy the path. 
Add a `REQUESTS_CA_BUNDLE` variable and paste the path as the value. 

Click Ok

### **Step 3:** File Setup
Set up your files, Make a new folder and put `DataMatching.py` in it, within that folder make another folder called `Excel_File`(do not change this folder name), This is where you need to put the BL dataset and PD dataset. Make sure the BL dataset is called `Business_Data.csv` and PD dataset is called `PD_Data.csv`. 

### **Step 4:** Open terminal
Go to the location where `DataMatching.py` is and open up terminal at the location (type cmd and press enter and then type `cd <file path>` Ex. `cd "C:\Users\zashams\Documents\python scripts"` this is where it is on my computer)

After navigating there type in `pip config set global.trusted-host "pypi.org files.pythonhosted.org pypi.python.org"` 


### **Step 5:** Install Libraries
Now your pip should work. In the terminal where `DataMatching.py` is do `pip install pipenv` (if it doesn't work make sure you followed step 2 correctly)

Now that you have pipenv installed do `pipenv install pandas` wait for it to install. 
Install all the other Libraries (`pipenv install <lib name here>`)
- `pandas`
- `openpyxl`
- `fuzzywuzzy`
- `python-levenshtein`

### **Step 6:** Run the code
Now you can run the python script, the previous step should of generated a Pipfile in the same path as `DataMatching.py`, edit it and add this at the end:

    [scripts]
    testall = "pipenv run python DataMatching.py"

in terminal type `pipenv run testall` (testall can be called something else just make sure you change in the Pipfile and in run command)

Now a `output.csv` should be generated and this is the merged dataset with Businesses that have been broken into.

## **To run with New Data**
To do this with new data is should be very easy to do, just replace `Business_Data.csv` and `PD_Data.csv` with the new datasets. Just make sure these two have the same names and same path relative to `DataMatching.py`. `Excel_File\Business_Data.csv` and `Excel_File\PD_Data.csv` respectively. 

**Notes**
-I recommend installing vscode as it makes everything very simple, you can open terminal, look at code, and make/modify any files very easily. 
