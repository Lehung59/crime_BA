import os
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)
from ingestion.ingest_crime_pattern import *
from preprocessing.clean_crime_pattern import *
from ingestion.ingest_criminal_profiling import *
from preprocessing.clean_criminal_profiling import *
from ingestion.ingest_recidivism import *
from preprocessing.clean_recidivism import *
from modeling.train_recidivism import *
from preprocessing.transform_recidivism import *
from ingestion.ingest_resource_allocation import *
from preprocessing.clean_resource_allocation import *


def crime_pattern_analysis():
    raw_data = ingest_crime_pattern_analysis()
    cleaned_data = clean_data_crime_pattern_analysis(raw_data)
    cleaned_data = update_crime_lat_long(cleaned_data)


def Criminal_profiling():
    raw_data = ingest_criminal_profiling()
    clean_Criminal_Profiling(raw_data)


def predictive_modeling():
    raw_data = ingest_recidivism_data()
    cleaned_data = clean_recividism_model(raw_data)
    X_train, X_test, y_train, y_test = transform_cleaned_recidivism_data(cleaned_data)
    train_recidivism_model(X_train, X_test, y_train, y_test)


def resource_allocation():
    raw_data = ingest_resource_data()
    cleaned_data = clean_resource_data(raw_data)


crime_pattern_analysis()
Criminal_profiling()
predictive_modeling()
resource_allocation()
