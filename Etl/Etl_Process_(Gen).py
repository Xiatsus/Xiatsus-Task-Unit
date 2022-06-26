# Final Project.
# Discpline: Database Topics.
# Code: Matb10.

# Start the Master and workers.
# $SPARK_HOME/sbin/start-all.sh

# Stop the Master and workers.
# $SPARK_HOME/sbin/stop-all.sh

# Start SPARK SHELL with Python.
# $SPARK_HOME/bin/pyspark

# Submit .py to SPARK SHELL with Python Shell.
# $SPARK_HOME/bin/spark-submit

# Libraries to run operating system commands through Python.

import subprocess
import os
import sys

import findspark

findspark.init()

import pyspark
import pandas as pd

# First Step from ETL. Data Extract Process.

# Folder Creation (If necessary).

if os.path.isdir("/home/usr/abc"):
    pass  # Nothing to do.

else:
    subprocess.run(["mkdir", "/home/usr/abc"])

# Download .zip Google Community Mobility Reports. Save in '/home/usr/abc'.

from urllib import request

file_url = "https://www.gstatic.com/covid19/mobility/Region_Mobility_Report_CSVs.zip"
file = "/home/usr/abc/Region_Mobility_Report_CSVs.zip"

request.urlretrieve(file_url, file)

# Folder Creation (If necessary).

if os.path.isdir("/home/usr/def"):
    pass  # Nothing to do.

else:
    subprocess.run(["mkdir", "/home/usr/def"])

# Download Cases.csv from the Fiocruz/eSUS-VE database. Save in '/home/usr/def'.

file_url = "https://raw.githubusercontent.com/Xiatsus/Xiatsus-Task-Unit/main/Database/Fiocruz%20Database/Cases.csv"
file = "/home/usr/def/Cases.csv"

request.urlretrieve(file_url, file)

# Download Deaths.csv from the Fiocruz/SIVEP-Gripe database. Save in '/home/usr/def'.

file_url = "https://raw.githubusercontent.com/Xiatsus/Xiatsus-Task-Unit/main/Database/Fiocruz%20Database/Deaths.csv"
file = "/home/usr/def/Deaths.csv"

request.urlretrieve(file_url, file)

# Extract sub. file from '/home/usr/def'.

from zipfile import ZipFile

z = ZipFile("/home/usr/abc/Region_Mobility_Report_CSVs.zip", "r")
z.extract("2020_BR_Region_Mobility_Report.csv", "/home/usr/def")
z.close()

# Second Step from ETL. Remove useless information, and formatting the data.

from pyspark import SparkConf
from pyspark.context import SparkContext
from pyspark.sql import SparkSession, SQLContext

# Create SparkSession

spark = SparkSession.builder.master("local").appName("Etl.py").getOrCreate()

#or

# spark = SparkSession.builder.getOrCreate()

# Folder Creation (If necessary).

if os.path.isdir("/home/usr/ghi"):
    pass  # Nothing to do.

else:
    subprocess.run(["mkdir", "/home/usr/ghi"])

# Processing: Google Community Mobility Reports.

path = "/home/usr/def/2020_BR_Region_Mobility_Report.csv"

df = spark.read.csv(path, inferSchema=True, header=True)
df = df.drop("sub_region_1", "sub_region_2", "iso_3166_2_code",
             "census_fips_code", "place_id")
df = df.selectExpr(
    "country_region_code as Code",
    "country_region as Country",
    "date as Date",
    "retail_and_recreation_percent_change_from_baseline as Retail_and_Recreation",
    "grocery_and_pharmacy_percent_change_from_baseline as Grocery_and_Pharmacy",
    "parks_percent_change_from_baseline as Parks",
    "transit_stations_percent_change_from_baseline as Transit_Stations",
    "workplaces_percent_change_from_baseline as Workplaces",
    "residential_percent_change_from_baseline as Residential",
)

# Exporting .csv.

df = df.write.option(
    "header", True).mode('overwrite').csv("/home/usr/ghi/Mobility_Report.csv")

print("Google Community Mobility Reports has been processed, and saved in the directory /home/usr/ghi.")

# Processing: Cases Reports.

path1 = "/home/usr/def/Cases.csv"

df1 = pd.read_csv(path1, header=None, nrows=362, index_col=0)
df1 = df1.transpose()
df1.columns = ["Date", "Cases"]

# Max = Line 362.

# Exporting .csv.

df1 = df1.to_csv("/home/usr/ghi/Cases.csv", header=True, index=False, index_label = False)

print("Cases Reports has been processed, and saved in the directory /home/usr/ghi.")

# Processing: Deaths Reports.

path2 = "/home/usr/def/Deaths.csv"

df2 = pd.read_csv(path2, header=None, nrows=289, index_col=0, on_bad_lines='skip')
df2 = df2.transpose()
df2.columns = ["A", "B","C", "D", "E", "F", "G", "H"]
df2 = df2.drop(columns=["C", "D", "E", "F", "G", "H"])
df2.columns = ["Date", "Occurrences"]

# Max = Line 289.

# Exporting .csv.

df2 = df2.to_csv("/home/usr/ghi/Deaths.csv", header=True, index=False, index_label = False)

print("Deaths Reports has been processed, and saved in the directory /home/usr/ghi.")

# Final export occurs at the end of processing each of the .Csv / Data Sources.

# Show result. It can be used for testing purposes in any part of the operation with Dataframes:

# df.show()