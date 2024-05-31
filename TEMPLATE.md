# Template
This is the template for PD data and BL data

### PD data template:
PD data should be in this format.

| ...    | DateTimeReported | ...  | StreetAddress    | Statute | UCR    | UCR Desc | Zip    | Area | Beat |
| -------- | ------- | -------- | ------- | -------- | ------- | -------- | ------- | --------| --------|
| XXXXX  | XXXXX    |XXXXX  | XXXXX    |XXXXX  | XXXXX    |XXXXX  | XXXXX    |XXXXX  | XXXXX    |
| XXXXX  | XXXXX    |XXXXX  | XXXXX    |XXXXX  | XXXXX    |XXXXX  | XXXXX    |XXXXX  | XXXXX    |
| XXXXX  | XXXXX    |XXXXX  | XXXXX    |XXXXX  | XXXXX    |XXXXX  | XXXXX    |XXXXX  | XXXXX    |

Make sure these Columns are present in PD Data: 
- `DateTimeReported`
- `StreetAddress`
- `Statute`
- `UCR`
- `UCR Desc`
- `Zip`
- `Area`
- `Beat`


### BL data template:
BL data should be in this format.

| LicenseNumber  | ... | Site Location  |  ... |
| -------- | ------- | -------- | ------- | 
| XXXXX  | XXXXX    |XXXXX  | XXXXX    |
| XXXXX  | XXXXX    |XXXXX  | XXXXX    |
| XXXXX  | XXXXX    |XXXXX  | XXXXX    |

Make sure these Columns are present in PD Data: 
- `LicenseNumber`
- `Site Location`

### File Hierachy Model:

```
<Your File Name>
│   DataMatching.py   
│
└───Excel_File
    │   Business_Data.csv
    │   PD_Data.csv

```
