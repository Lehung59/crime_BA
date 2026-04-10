# Crime Analysis and Resource Allocation Dataset Description

## Overview
This document provides a comprehensive description of the datasets used in the Business Analytics project focused on crime patterns and resource allocation in Karnataka, India. The project aims to analyze historical crime data to identify patterns, profile recidivism risks, and optimize police resource distribution.

## Data Source & Context
The data is sourced from the state of Karnataka, India. It encapsulates diverse sociological factors unique to the Indian context, including the caste system and specific legal classifications of crimes.

---

## Dataset Components

### 1. Crime Pattern Analysis (`Crime_Pattern_Analysis_Cleaned.csv`)
This dataset contains granular information about individual First Information Reports (FIRs) and is used to analyze spatial and temporal crime trends.

*   **Key Columns:**
    *   `District_Name`: The administrative district where the crime occurred.
    *   `UnitName`: The specific police station or unit handling the case.
    *   `Crime_Group_Name`: Broad classification of the crime (e.g., THEFT, MURDER, BURGLARY).
    *   `Latitude`, `Longitude`: Geographic coordinates for mapping and spatial analysis.
    *   `Victim_Count`, `Accused_Count`: Number of individuals involved.
    *   `Offence_From_Date`, `Offence_To_Date`: Temporal duration of the incident.

### 2. Crime Type Distribution (`Crime_Type_cleaned_data.csv`)
Aggregated data focusing on the frequency of crime categories across different timeframes and districts.

*   **Key Columns:**
    *   `District_Name`: Location of the offences.
    *   `Crime Category`: Specific type of crime (e.g., POCSO, Dacoity).
    *   `Offence_From_Year/Month/Day`: Decomposed time components for trend analysis.

### 3. Criminal Profiling (`Criminal_Profiling_cleaned.csv`)
Contains demographic and professional profiles of individuals involved in criminal activities.

*   **Key Columns:**
    *   `Occupation`: The professional background of the individual (e.g., Labourer, Farmer, Driver).
    *   `Caste`: The sociological classification of the individual (critical for understanding societal patterns in India).
    *   `Age`, `Sex`: Basic demographic markers.
    *   `Crime_Group1`, `Crime_Head2`: Specific crime classifications.

### 4. Recidivism Analysis (`Recidivism_cleaned_data.csv`)
Focused on predicting the likelihood of re-offending. This dataset is a primary input for H2O AutoML predictive modeling.

*   **Key Columns:**
    *   `Recidivism`: Binary flag (0 or 1) indicating if the individual re-offended.
    *   `Age`, `Caste`, `Profession`: Predictive features for modeling.
    *   `PresentCity`: Geographic context for the individual.

### 5. Resource Allocation (`Resource_Allocation_Cleaned.csv`)
Data regarding police force strength and workload, used to optimize personnel distribution.

*   **Key Columns:**
    *   `Beat Name`: The smallest administrative area for police patrol.
    *   `Total Crimes per beat`: Workload indicator.
    *   `Sanctioned Strength`: Numbers for Assistant Sub-Inspectors (ASI), Head Constables (HC), and Police Constables (PC).
    *   `Normalised Crime Severity`: A calculated metric to prioritize resource deployment.

---

## Technical & Sociological Context

### Legal Terms & Crime Categories
*   **POCSO (Protection of Children from Sexual Offences):** Crimes related to child sexual abuse, carrying severe legal penalties.
*   **Dacoity:** Armed robbery committed by a group of five or more people.
*   **SLL (Special and Local Laws):** Offences registered under state-specific or specialized legislation rather than the Indian Penal Code (IPC).

### The Caste System (Varna)
The dataset includes detailed documentation of the `Caste` field, which is central to Indian sociological analysis:
*   **Brahmin:** Traditionally priests and teachers.
*   **Kshatriya:** Traditionally warriors and rulers.
*   **Vaishya:** Traditionally traders and agriculturists.
*   **Shudra:** Traditionally laborers and service providers.
*   **Scheduled Castes (Dalits):** Historically marginalized groups (e.g., ADI DRAVIDA, MADIGA, CHALAVADI). These are often referred to as "untouchables" in historical contexts and are subject to protective legislation (Prevention of Atrocities Act).

### Occupational Significance
Occupations like **Labourer**, **Farmer**, and **Driver** represent significant portions of the offender profile in certain regions, often linked to socio-economic stressors. The distinction between "Businessman" and "Labourer" helps in analyzing the economic background of crime types (e.g., White-collar vs. Blue-collar crimes).

---

## Project Usage
*   **Visual Analysis:** Mapping crime hotspots using Latitude/Longitude.
*   **Predictive Analytics:** Using Recidivism data to build risk assessment models.
*   **Strategic Planning:** Using Resource Allocation data to recommend redistribution of police personnel based on "Normalised Crime Severity" and current "Sanctioned Strength."
