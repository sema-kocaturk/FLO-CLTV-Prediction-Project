# FLO CLTV Prediction Project
 FLO CLTV Prediction Project
Customer Lifetime Value (CLTV) Analysis using Python
This repository contains code and analysis for calculating Customer Lifetime Value (CLTV) using the Beta-Geometric/Negative Binomial Distribution (BG/NBD) and Gamma-Gamma models. CLTV is an important metric in marketing and customer relationship management that estimates the potential value a customer will bring to a business over their entire relationship with the company.

Getting Started
To run the analysis in this repository, you'll need the following prerequisites:
Required libraries: pandas, lifetimes

Dataset
The analysis is performed on a dataset containing customer order information. The following preprocessing steps were applied to the dataset:

Outliers were identified and replaced with upper and lower limits using outlier_thresholds and replace_with_thresholds functions.
Date columns were converted to the datetime format.
Calculated new features like total_num_order and total_value_order.
Created cltv_df DataFrame for CLTV analysis.
CLTV Analysis
The CLTV analysis includes the following steps:

Data Preparation

Calculated recency, frequency, and T_weekly for each customer.
Calculated average monetary value per transaction.
BG/NBD Model

Fit the Beta-Geometric/Negative Binomial Distribution model to frequency, recency, and T_weekly data.
Predicted expected purchases over the next 3 and 6 months.
Gamma-Gamma Model

Fit the Gamma-Gamma model to frequency and monetary_cltv_avg data.
Calculated expected average transaction value.
CLTV Calculation

Calculated CLTV using the BG/NBD and Gamma-Gamma models.
Sorted customers by CLTV to identify top customers.

Segmentation

Segmented customers into 4 segments (A, B, C, D) based on their CLTV values.
Analyzed segment characteristics based on recency, frequency, and average monetary value.
Results
The analysis provides insights into customer behavior and value, allowing businesses to focus their efforts on high-value segments. The segmentation provides a clear view of different customer groups and their potential impact on the business's bottom line.

Usage
You can use the provided code and notebooks to perform your own CLTV analysis on different datasets. Modify the dataset file path, adjust parameters, and expand the analysis to suit your specific needs.

Contribution
Contributions to this repository are welcome! If you find any issues or ways to improve the analysis, feel free to submit a pull request.
