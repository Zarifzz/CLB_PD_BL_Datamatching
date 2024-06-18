import pandas as pd
# from fuzzywuzzy import fuzz
# from fuzzywuzzy import process
import time
import numpy 

from rapidfuzz import process, fuzz, utils

timestart = time.time()

# Path to BL and PD datasets 
Business_csv_path = "Excel_File\\Business_Data.csv"
PD_csv_path = "Excel_File\\PD_Data.csv"

# Read BL and PD data as Dataframes in pandas 
Business_df = pd.read_csv(Business_csv_path, encoding = 'unicode_escape', engine ='python')
PD_df = pd.read_csv(PD_csv_path, encoding = 'unicode_escape', engine ='python')

# Since we are matching on addresses turn all addresses into lowercase so it is easier to match 
Business_df['Site Location_lower'] = Business_df['Site Location'].str.lower()
PD_df['StreetAddress_lower'] = PD_df['StreetAddress'].str.lower()

# A fuzzy merge function that merges two datasets on a matching row. It will merge if the two addresses are similar enough
# Taken from: https://stackoverflow.com/questions/13636848/is-it-possible-to-do-fuzzy-match-merge-with-python-pandas
def fuzzy_merge(df_1, df_2, key1, key2, threshold=90, limit=2):
    """
    :param df_1: the left table to join
    :param df_2: the right table to join
    :param key1: key column of the left table
    :param key2: key column of the right table
    :param threshold: how close the matches should be to return a match, based on Levenshtein distance
    :param limit: the amount of matches that will get returned, these are sorted high to low
    :return: dataframe with boths keys and matches
    """
    s = df_2[key2].tolist()
    
    m = df_1[key1].apply(lambda x: process.extract(x, s, limit=limit))
    df_1['matches'] = m
    
    m2 = df_1['matches'].apply(lambda x: ', '.join([i[0] for i in x if i[1] >= threshold]))
    df_1['matches'] = m2
    
    return df_1

# returns the first part of an address. Returns "1234" out of "1234 Street Ave."
def extract_first_part(address):
    return address.split()[0]


# Does the fuzzy merge operation. Put in BL data as left table and PD data as right table, Compare on their respective street address cols.  
matching_df = fuzzy_merge(Business_df, PD_df, 'Site Location_lower', 'StreetAddress_lower', 95, 1)

# gets ONLY the matches in the merged DF from fuzzy_merge()
matchesOnly_df = matching_df[matching_df['matches'] != '']

# Add 'DateTimeReported', 'StreetAddress_lower', 'StreetAddress',  'Statute', 'UCR', 'UCR Desc', 'Zip', 'Area', 'Beat' Columns to the merged DF. 
SelectedRows_PDData_df = PD_df[['DateTimeReported', 'StreetAddress_lower', 'StreetAddress',  'Statute', 'UCR', 'UCR Desc']]
merged_df = pd.merge(matchesOnly_df, SelectedRows_PDData_df, left_on='matches', right_on='StreetAddress_lower', how='left')

# Add a Error Column such that if the first part of of the two Addresses dont match it shows Error: True for that row
merged_df['FirstPart1'] = merged_df['Site Location_lower'].apply(extract_first_part)
merged_df['FirstPart2'] = merged_df['matches'].apply(extract_first_part)

merged_df['error'] = merged_df.apply(lambda row: row['FirstPart1'] != row['FirstPart2'] or row['matches'] == '1 world trade center', axis=1)

merged_df.drop(['FirstPart1', 'FirstPart2'], axis=1, inplace=True)

# Turn merged DF into a CSV file to look at!
merged_df.drop('StreetAddress_lower', axis=1, inplace=True)
merged_df.to_csv('Excel_File\\output.csv', index=False)
# prints # of cols and rows 

timeend = time.time()



print("Finished!!!")
print("Timer:", timeend - timestart, "Seconds")
print("Shape: ", merged_df.shape)

'''
Some Notes: 
- Do not run this with any of the csv's open in a excel doc, It will not work as python cannot access it as you are accessing it as well. 
- To drop any other columns in the final resulting CSV add:  merged_df.drop('Insert Column name', axis=1, inplace=True)  right before turning the DF into a CSV. 
'''