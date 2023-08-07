# YouTube_Data_Harvesting_Tej
## INTRODUCTION
Hi this is Tejesh and this my first data science project : Youtube Data Harvesting. While doing this project I have extract the data from Youtube with the help of channel Id,I have get the data in the form of unstructured so I have planned to store into mongodb. After storing the data into mongodb I need to transfer unstructural form to the structural form so,I have planned to store into MYSQL and then analysing data depending on the customer questions by using streamlit apllication.


![image](https://github.com/Tejesh-25/YouTube_Data_Harvesting_Tej/assets/140998711/9550cf99-8b4a-49f8-bb93-01faa85b894c)

# Devloper Guide
## 1.Tools Install
Markup: *Visual Studio Code.
*Python 3.11.0 or higher.
*MongoDB.
*MYSQL.
*Youtube Api Key.

## 2.Requirement Libraries to Install
  pip install google-api-python-client.
  pip install pymongo.
  pip install mysql-connector-python.
  pip install sqlalchemy.
  pip install pandas.
  pip install streamlit.
  
## 3.Import Libraries
## Youtube Api
  from googleapiclient.discovery import build
## MongoDB
  import pymongo
  
## SQL libraries
  import mysql.connector
  import sqlalchemy
  from sqlalchemy import create_engine
  import pymysql
  
## Pandas
  import pandas as pd
## Dashboard libraries
  import streamlit as st
## 4.E T L Process
## a) Extract data
  In first I need to create a new project in Google Developer Console. After creating the console with help of Credentials I get the my new API key, After that I can          extract the youtube channel data by using youtube channel Id.
## b) Process data 
  Once extraction is completed I need to filter the information based on the customer preference.
## c) Load Data 
  After filteration I need load the data to MongoDB.And also to migrate unstructure data to MYSQL from MongoDB.
## 5. E D A Process and Framework
## a) Access MySQL DB
  Create a connection to the MySQL server and access the specified MySQL DataBase by using mysql library and access tables.
## b) Filter the data
  Filter and process the collected data from the tables depending on the given requirements by using SQL queries and transform the processed data into a DataFrame format.
## c) Visualization
  Finally, create a Dashboard by using Streamlit and give dropdown options on the Dashboard to the user and select a question from that menu to analyse the data and show      the output in Dataframe Table and Bar chart.
## User Guide 
## Step-1: Input and Data_Scrab 
  Search for the channel Id, copy and paste in the input box,In below there will be one button  data_scrab if I click that button it will scrab all the data and show to me.
## Step-2 : Store data in Mongodb
  below the data_scrab button there will be another button named as store_data_mongodb if i click that button it will stored the data scessfully.
## Step-3 : Transfer the Data
  If I press the third button named as (Transfer_data_mongodb_to_sql).It will be scessfully tranfer the entire data to mysql from mongo db.
## Step-4 : Frequently Asked Questions
  Select a Question from the dropdown option you can get the results in Dataframe format or bar chat format.
  
  ![image](https://github.com/Tejesh-25/YouTube_Data_Harvesting_Tej/assets/140998711/0b904d4e-9aed-4c17-b946-ce2cede1e845)
  
  ![image](https://github.com/Tejesh-25/YouTube_Data_Harvesting_Tej/assets/140998711/e068ac00-a2d4-4266-b419-d40caa3f6f0a)



  
