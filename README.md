# README
## Project Overview
This project aims to identify Long Beach businesses that have been broken into by analyzing the correlations and connections between police department (PD) data and BizCare’s business license data. By cross-referencing incident reports of break-ins with business licensing records, we can pinpoint which businesses have been affected, enabling BizCare’s team to direct their efforts to those in need. This methodology involves cleaning and merging datasets, and extracting relevant features by applying Python scripts and other data science techniques to detect significant correlations. The results will provide an Excel spreadsheet of all the business licenses that have been affected, with merged columns from both the PD data and Business License data. Overall, this project leverages data analysis to enhance the targeted support and intervention efforts by BizCare and its team.

## Steps and Corresponding Code
### **Step 1:** Import Necessary Libraries
To handle data and perform fuzzy matching, we import the required libraries.


    import pandas as pd
    from fuzzywuzzy import fuzz
    from fuzzywuzzy import process
    import numpy



### **Step 2:** Load Data
We load the Business License (BL) and Police Department (PD) datasets into pandas DataFrames.
    
    Business_csv_path = "Excel_File\\Business_Data.csv"
    PD_csv_path = "Excel_File\\PD_Data.csv"

    Business_df = pd.read_csv(Business_csv_path, encoding='unicode_escape', engine='python')
    PD_df = pd.read_csv(PD_csv_path, encoding='unicode_escape', engine='python')



### **Step 3:** Preprocess Data
We convert all addresses to lowercase to make them easier to compare.
    
    Business_df['Site Location_lower'] = Business_df['Site Location'].str.lower()
    PD_df['StreetAddress_lower'] = PD_df['StreetAddress'].str.lower()



### **Step 4:** Define Fuzzy Merge Function
We define a function that merges two datasets based on similar addresses using fuzzy matching.
    
    def fuzzy_merge(df_1, df_2, key1, key2, threshold=90, limit=2):
        s = df_2[key2].tolist()  # Get a list of addresses from the right table
        
        
        m = df_1[key1].apply(lambda x: process.extract(x, s, limit=limit))
        df_1['matches'] = m  # Store the matches in a new column
        
        
        m2 = df_1['matches'].apply(lambda x: ', '.join([i[0] for i in x if i[1] >= threshold]))
        df_1['matches'] = m2
        
        return df_1



### **Step 5:** Perform Fuzzy Merge
We use the fuzzy merge function to compare the addresses from both datasets.
    
    matching_df = fuzzy_merge(Business_df, PD_df, 'Site Location_lower', 'StreetAddress_lower', 95, 1)




### **Step 6:** Filter Matches
We keep only the rows where a match was found.
   
    matchesOnly_df = matching_df[matching_df['matches'] != '']



### **Step 7:** Select Specific Columns
We select specific columns from the PD dataset to add to the merged dataset.

    SelectedRows_PDData_df = PD_df[['DateTimeReported', 'StreetAddress_lower', 'StreetAddress', 'Statute', 'UCR', 'UCR Desc', 'Zip', 'Area', 'Beat']]



### **Step 8:** Merge DataFrames
We merge the matched rows with the selected columns from the PD dataset.

    merged_df = pd.merge(matchesOnly_df, SelectedRows_PDData_df, left_on='matches', right_on='StreetAddress_lower', how='left')


### **Step 9:** Check for Errors
We check if the first parts of the addresses match and mark errors if they don't.

    def extract_first_part(address):
        return address.split()[0]

    merged_df['FirstPart1'] = merged_df['Site Location_lower'].apply(extract_first_part)
    merged_df['FirstPart2'] = merged_df['matches'].apply(extract_first_part)
    merged_df['error'] = merged_df.apply(lambda row: row['FirstPart1'] != row['FirstPart2'] or row['matches'] == '1 world trade center', axis=1)

    merged_df.drop(['FirstPart1', 'FirstPart2'], axis=1, inplace=True)



### **Step 10:** Clean Up
We remove the duplicate address column from the final dataset

    merged_df.drop('StreetAddress_lower', axis=1, inplace=True)



### **Step 11:** Output the Result
We save the final merged dataset to a CSV file and print the number of rows and columns in the final dataset.

    merged_df.to_csv('Excel_File\\output.csv', index=False)
    print("Shape: ", merged_df.shape)



#### Notes: 
- Do not run this with any of the CSV files open in an Excel document. Python cannot access the files if they are open in Excel.
- To drop any other columns in the final resulting CSV, add `merged_df.drop('Insert Column name', axis=1, inplace=True)` right before saving the DataFrame to a CSV.

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
- `HTTP_PROXY` = `http://aspnet:aspnet@proxy4.ci.long-beach.ca.us:8080/`
- `HTTPS_PROXY` = `http://aspnet:aspnet@proxy4.ci.long-beach.ca.us:8080/`

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






