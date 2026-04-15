import numpy as np
import pandas as pd
import os


def load_sanctioned_strength_data():
    data_path = os.path.join(
        os.path.dirname(__file__),
        '..',
        'data',
        'raw',
        'police_sanction_strength.csv'
    )
    sanctioned_df = pd.read_csv(data_path)

    required_columns = ['District Name', 'ASI', 'CHC', 'CPC']
    missing_columns = set(required_columns) - set(sanctioned_df.columns)
    if missing_columns:
        raise ValueError(
            f"Thiếu cột trong police_sanction_strength.csv: {sorted(missing_columns)}"
        )

    sanctioned_df = sanctioned_df[required_columns].copy()
    sanctioned_df['District Name'] = sanctioned_df['District Name'].astype(str).str.strip()
    sanctioned_df[['ASI', 'CHC', 'CPC']] = sanctioned_df[['ASI', 'CHC', 'CPC']].apply(
        pd.to_numeric, errors='raise'
    )

    return sanctioned_df


def clean_resource_data(df):
    df["Total Crimes per beat"] = df.groupby(["District_Name", "UnitName", "Village_Area_Name", "Beat_Name"])["FIRNo"].transform("count")

    df = df[(df["District_Name"]!= "CID") & (df["District_Name"]!= "ISD Bengaluru") & (df["District_Name"]!= "Coastal Security Police")]

    district_mapping = {
    'Bagalkot': 'SP, BAGALKOTE',
    'Ballari': 'SP, BELLARY',
    'Belagavi City': 'COP, BELGAUM CITY',
    'Belagavi Dist': 'SP, BELGAUM',
    'Bengaluru City': 'COP, BANGALORE CITY',
    'Bengaluru Dist': 'SP, BANGALORE',
    'Bidar': 'SP, BIDAR',
    'Chamarajanagar': 'SP, CHAMARAJANAGARA',
    'Chickballapura': 'SP, CHICKBALLAPURA',
    'Chikkamagaluru': 'SP, CHICKMAGALURU',
    'Chitradurga': 'SP, CHITRADURGA',
    'Dakshina Kannada': 'SP, DK, MANGALORE',
    'Davanagere': 'SP, DAVANGERE',
    'Dharwad': 'SP, DHARWAD',
    'Gadag': 'SP, GADAG',
    'Hassan': 'SP, HASSAN',
    'Haveri': 'SP, HAVERI',
    'Hubballi Dharwad City': 'COP, HUBLI-DHARWAD CITY',
    'K.G.F': 'SP, KGF',
    'Kalaburagi': 'SP, KALABURGI',
    'Kalaburagi City': 'COP, KALBURGI CITY',
    'Karnataka Railways': 'SP, RAILWAYS',
    'Kodagu': 'SP, KODAGU',
    'Kolar': 'SP, KOLAR',
    'Koppal': 'SP, KOPPAL',
    'Mandya': 'SP, MANDYA',
    'Mangaluru City': 'COP, MANGALORE CITY',
    'Mysuru City': 'COP, MYSORE CITY',
    'Mysuru Dist': 'SP, MYSORE',
    'Raichur': 'SP, RAICHUR',
    'Ramanagara': 'SP, RAMANAGARA',
    'Shivamogga': 'SP, SHIVAMOGA',
    'Tumakuru': 'SP, TUMKURU',
    'Udupi': 'SP, UDUPI',
    'Uttara Kannada': 'SP, UK, KARWAR',
    'Vijayanagara': 'SP, VIJAYANAGARA',
    'Vijayapur': 'SP, VIJAYAPURA',
    'Yadgir': 'SP, YADAGIRI'
    }

    df["District Name"] =  df["District_Name"].map(district_mapping)

    sanctioned_df = load_sanctioned_strength_data()

    df = df.merge(sanctioned_df, on='District Name', how='left')
    
    df.drop(columns = ["District_Name", "FIRNo"], inplace = True)

    df.dropna(inplace = True)
    df.drop_duplicates(inplace = True)

    
    category_mapping = {
        'THEFT': 'Property Crimes',
        'BURGLARY - NIGHT': 'Property Crimes',
        'BURGLARY - DAY': 'Property Crimes',
        'ROBBERY': 'Property Crimes',
        'DACOITY': 'Property Crimes',
        'CRIMINAL BREACH OF TRUST': 'Property Crimes',
        'CHEATING': 'Property Crimes',
        'FORGERY': 'Property Crimes',
        'COUNTERFEITING': 'Property Crimes',
        'CRIMINAL MISAPPROPRIATION ': 'Property Crimes',
        'RECEIVING OF STOLEN PROPERTY': 'Property Crimes',
        'MOTOR VEHICLE ACCIDENTS NON-FATAL': 'Accidents and Public Safety',
        'MOTOR VEHICLE ACCIDENTS FATAL': 'Accidents and Public Safety',
        'DEATHS DUE TO RASHNESS/NEGLIGENCE': 'Accidents and Public Safety',
        'NEGLIGENT ACT': 'Accidents and Public Safety',
        'PUBLIC SAFETY': 'Accidents and Public Safety',
        'PUBLIC NUISANCE': 'Accidents and Public Safety',
        'MISSING PERSON': 'Missing Persons',
        ' CYBER CRIME': 'Cyber Crimes',
        'CASES OF HURT': 'Violent Crimes',
        'ATTEMPT TO MURDER': 'Violent Crimes',
        'MURDER': 'Violent Crimes',
        'CULPABLE HOMICIDE NOT AMOUNTING TO MURDER': 'Violent Crimes',
        'ATTEMPT TO CULPABLE HOMICIDE NOT AMOUNTING TO MURDER': 'Violent Crimes',
        'MOLESTATION': 'Violent Crimes',
        'KIDNAPPING AND ABDUCTION': 'Violent Crimes',
        'RIOTS': 'Violent Crimes',
        'CRUELTY BY HUSBAND': 'Violent Crimes',
        'CRIMES RELATED TO WOMEN': 'Violent Crimes',
        'POCSO': 'Violent Crimes',
        'CRIMINAL INTIMIDATION': 'Violent Crimes',
        'WRONGFUL RESTRAINT/CONFINEMENT': 'Violent Crimes',
        'INSULTING MODESTY OF WOMEN (EVE TEASING)': 'Violent Crimes',
        'ASSAULT OR USE OF CRIMINAL FORCE TO DISROBE WOMAN': 'Violent Crimes',
        'EXPOSURE AND ABANDONMENT OF CHILD': 'Violent Crimes',
        'DOWRY DEATHS': 'Violent Crimes',
        'OFFENCES RELATED TO MARRIAGE': 'Violent Crimes',
        'ASSAULT': 'Violent Crimes',
        'CRIMINAL TRESPASS': 'Violent Crimes',
        'MISCHIEF': 'Violent Crimes',
        'ARSON': 'Violent Crimes',
        'CRIMINAL CONSPIRACY': 'Violent Crimes',
        'AFFRAY': 'Violent Crimes',
        'CrPC': 'Legal and Regulatory Offenses',
        'KARNATAKA df ACT 1963': 'Legal and Regulatory Offenses',
        'Karnataka State Local Act': 'Legal and Regulatory Offenses',
        'NARCOTIC DRUGS & PSHYCOTROPIC SUBSTANCES': 'Legal and Regulatory Offenses',
        'COTPA, CIGARETTES AND OTHER TOBACCO PRODUCTS': 'Legal and Regulatory Offenses',
        'COPY RIGHT ACT 1957': 'Legal and Regulatory Offenses',
        'ARMS ACT  1959': 'Legal and Regulatory Offenses',
        ' PREVENTION OF DAMAGE TO PUBLIC PROPERTY ACT 1984': 'Legal and Regulatory Offenses',
        ' REPRESENTATION OF PEOPLE ACT 1951 & 1988': 'Legal and Regulatory Offenses',
        'PASSPORT ACT': 'Legal and Regulatory Offenses',
        'EXPLOSIVES': 'Legal and Regulatory Offenses',
        'OFFENCES PROMOTING ENEMITY': 'Legal and Regulatory Offenses',
        'Concealment of birth by secret disposal of Child': 'Legal and Regulatory Offenses',
        'PORNOGRAPHY': 'Legal and Regulatory Offenses',
        'ADULTERATION': 'Legal and Regulatory Offenses',
        'POISONING-PROFESSIONAL': 'Legal and Regulatory Offenses',
        'SLAVERY': 'Legal and Regulatory Offenses',
        'OFFENCES BY PUBLIC SERVANTS (EXCEPT CORRUPTION) (Public servant is accused)': 'Legal and Regulatory Offenses',
        'BONDED LABOUR SYSTEM': 'Legal and Regulatory Offenses',
        'FOREST': 'Legal and Regulatory Offenses',
        'INDIAN ELECTRICITY ACT ': 'Legal and Regulatory Offenses',
        'INDIAN MOTOR VEHICLE': 'Legal and Regulatory Offenses',
        'UNNATURAL SEX ': 'Legal and Regulatory Offenses',
        'IMPERSONATION ': 'Legal and Regulatory Offenses',
        'PUBLIC JUSTICE': 'Legal and Regulatory Offenses',
        'OF ABETMENT': 'Legal and Regulatory Offenses',
        ' POST & TELEGRAPH,TELEGRAPH WIRES(UNLAWFUL POSSESSION)ACT 1950': 'Legal and Regulatory Offenses',
        'Human Trafficking': 'Legal and Regulatory Offenses',
        'ANTIQUES (CULTURAL PROPERTY)': 'Legal and Regulatory Offenses',
        'OFFICIAL SECURITY RELATED ACTS': 'Legal and Regulatory Offenses',
        'UNLAWFUL ACTIVITIES(Prevention)ACT 1967 ': 'Legal and Regulatory Offenses',
        'SEDITION': 'Legal and Regulatory Offenses',
        'DOCUMENTS & PROPERTY MARKS': 'Legal and Regulatory Offenses',
        'DEFENCE FORCES OFFENCES RELATING TO (also relating to desertion)': 'Legal and Regulatory Offenses',
        'Giving false information respecting an offence com': 'Legal and Regulatory Offenses',
        'UNNATURAL DEATH (Sec 174/174c/176)': 'Legal and Regulatory Offenses',
        'CINEMATOGRAPH ACT 1952': 'Legal and Regulatory Offenses',
        'INFANTICIDE': 'Legal and Regulatory Offenses',
        'PREVENTION OF CORRUPTION ACT 1988': 'Legal and Regulatory Offenses',
        'NATIONAL SECURITY ACT': 'Legal and Regulatory Offenses',
        'ILLEGAL DETENTION': 'Legal and Regulatory Offenses',
        'RAPE': 'Sexual Crimes',
        'IMMORAL TRAFFIC': 'Sexual Crimes',
        'SCHEDULED CASTE AND THE SCHEDULED TRIBES ': 'Hate Crimes and Discrimination',
        'COMMUNAL / RELIGION   ': 'Hate Crimes and Discrimination',
        'OFFENCES AGAINST PUBLIC SERVANTS (Public servant is a victim)': 'Crimes Against Public Servants',
        'SUICIDE': 'Other Crimes',
        'Failure to appear to Court': 'Other Crimes',
        'ELECTION': 'Other Crimes',
        'Disobedience to Order Promulgated by PublicServan': 'Other Crimes',
        'CHILDREN ACT': 'Other Crimes',
        'ANIMAL': 'Other Crimes',
        'FOREIGNER': 'Other Crimes',
        'Attempting to commit offences': 'Other Crimes',
        'FALSE EVIDENCE': 'Other Crimes',
        'CONSUMER': 'Other Crimes',
        'DEFAMATION': 'Other Crimes',
        'ESCAPE FROM LAWFUL CUSTODY AND RESISTANCE': 'Other Crimes',
        'DEATHS-MISCARRIAGE': 'Other Crimes',
        'KARNATAKA POLICE ACT 1963': "Legal and Regulatory Offenses" ,
        'RAILWAYS ACT': "Legal and Regulatory Offenses",
        'OFFENCES AGAINST STATE': "Legal and Regulatory Offenses",
        'CIVIL RIGHTS ': "Hate Crimes and Discrimination",
        'FAILURE TO APPEAR TO COURT': "Other Crimes",
        'BUYING & SELLING MINOR FOR PROSTITUTION': "Sexual Crimes",
    }


    # Assuming your data is in a DataFrame called 'data'
    df['Crime Group'] = df['CrimeGroup_Name'].map(category_mapping)

    df.drop(columns = ["CrimeGroup_Name"], inplace = True)

    crime_severity_weights = {
    'Violent Crimes': 5,
    'Sexual Crimes': 5,
    'Crimes Against Public Servants': 4,
    'Cyber Crimes': 4,
    'Hate Crimes and Discrimination': 4,
    'Accidents and Public Safety': 3,
    'Property Crimes': 3,
    'Missing Persons': 2,
    'Legal and Regulatory Offenses': 2,
    'Other Crimes': 1
    }

    df["Crime Severity"] = df["Crime Group"].map(crime_severity_weights)

    df.drop(columns = ["Crime Group"], inplace = True)
    df.dropna(inplace = True)
    crime_severity_group = df.groupby(["District Name","UnitName","Beat_Name"]).agg(Crime_Severity_per_Beat = ("Crime Severity", "sum"))

    df = df.merge(crime_severity_group["Crime_Severity_per_Beat"], on = ["District Name","UnitName","Beat_Name"], how = "left")

    df.drop(columns = ["Crime Severity"], inplace = True)


    df.drop_duplicates(inplace = True)

    new_order = ['District Name', 'UnitName',  'Village_Area_Name', 'Beat_Name','Total Crimes per beat', 'Crime_Severity_per_Beat', 'ASI', 'CHC', 'CPC']
    df = df[new_order]

    columns_to_rename = {'UnitName': 'Police Unit',
    'Beat_Name': 'Beat Name',
    'Village_Area_Name': "Village Area Name",
    "Accused_to_Arrested": "Accused to Arrested Ratio",
    "Charge_Sheeted_to_Arrested": "Charge Sheeted to Arrested Ratio",
    "Crime_Severity_per_Beat": "Crime Severity per Beat",
    "ASI": "Sanctioned Strength of Assistant Sub-Inspectors per District",
    "CHC": "Sanctioned Strength of Head Constables per District",
    "CPC": "Sanctioned Strength of Police Constables per District"}

    df = df.rename(columns=columns_to_rename)

    columns_to_convert = ['Sanctioned Strength of Assistant Sub-Inspectors per District',
                      'Sanctioned Strength of Head Constables per District',
                      'Sanctioned Strength of Police Constables per District']

    df[columns_to_convert] = df[columns_to_convert].apply(np.round).astype(int)
    
    # Calculate the sum of 'Crime Severity per Beat' for each district
    district_crime_severity_sum = df.groupby("District Name")["Crime Severity per Beat"].sum()

    # Calculate 'Normalised Crime Severity' by dividing 'Crime Severity per Beat' by the sum for each district
    df["Normalised Crime Severity"] = df.apply(lambda row: row["Crime Severity per Beat"] / district_crime_severity_sum[row["District Name"]], axis=1)

    df.drop(columns = ["Crime Severity per Beat"], inplace = True)


    # Save the new dataset to a new CSV file
    output_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', 'Resource_Allocation_Cleaned.csv')
    df.to_csv(output_path, index = False)














