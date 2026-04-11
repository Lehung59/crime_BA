import pandas as pd
import os


def ingest_resource_data():
    raw_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw', 'FIR_Details_Data.csv')
    df = pd.read_csv(raw_path)

    df.drop(columns= df.columns[~df.columns.isin(['District_Name', 'UnitName', 'FIRNo', 'CrimeGroup_Name',
        'Beat_Name', 'Village_Area_Name',
       ])],inplace = True)

    df.drop_duplicates(inplace =  True)

    return df