#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Job for putting files from local to HDFS and then creating internal hive tables with files name and
Inserting data into internal hive table"""

# import the python subprocess module
import subprocess
import pandas as pd
import os
from pyhive import hive

_dirPath  = "/home/brajendra/dev/StockMarket/MyShares/"
_newDirPath = "/home/brajendra/dev/StockMarket/ProcessedFiles/"
def start_app():
    for root, dirs, files in os.walk(_dirPath):
        for file in files:
            if file.endswith(".csv"):
                FileProcessing(file)
    (ret, out, err)= run_cmd(['hadoop', 'fs', '-put',_newDirPath, '/brajendra/StockMarket'])
    
    for root, dirs, files in os.walk(_newDirPath):
        for file in files:
            if file.endswith(".csv"):
                CreateAndInsertData(file)
                
def FileProcessing(_filename):
    
    _data = pd.read_csv(_dirPath + _filename)
    _data = _data.drop_duplicates()
    _data = _data.dropna()
    _data = _data.apply(lambda x: x.str.lstrip() if x.dtype == "object" else x)
    _data.columns = _data.columns.str.upper()
    _data.columns = _data.columns.str.rstrip()
    _data.columns = _data.columns.str.replace(' ','_')
    _data.columns = _data.columns.str.replace('.','')
    newFileName = _filename
    _data.to_csv(_newDirPath + newFileName)


def run_cmd(args_list):
    print("Start copy files from Local to HDFS")
    print('Running system command: {0}'.format(' '.join(args_list)))
    proc = subprocess.Popen(args_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    s_output, s_err = proc.communicate()
    s_return = proc.returncode
    return s_return, s_output, s_err


def CreateAndInsertData(_fileName):
    print("Star Inserting Data into Hive Tables")
    #print("File Name : " + _fileName)
    conn = hive.Connection(host="127.0.0.1", port='10000', username="brajendra",database='db_StockMarket')
    cursor = conn.cursor()
    cursor.execute("set hive.cli.print.header=true")
    _tableName = "tbl_" + _fileName.split(".")[0];
    #print(_tableName)
    create_query = 'Create table if NOT exists ' +_tableName + '(S_Date string,SERIES string,OPEN string,HIGH string,LOW string,PREV_CLOSE string ,LTP string,CLOSE string,VWAP string,52W_H float,52W_L float,VOLUME float,VALUE string,No_Of_Trades float )'
    optional_query = ' row format delimited fields terminated by "," tblproperties("skip.header.line.count"="1")'
    final_query = create_query + optional_query
    cursor.execute(final_query)
    print("Table Created!!") 
    
    
    #Loading data from hdfs to hive table 
    _hdfsPath = "'hdfs://127.0.0.1:9000/brajendra/StockMarket/ProcessedFiles/"+ _fileName +"'"
    #print(_hdfsPath)
    insert_query = "load data INPATH " + _hdfsPath + " into table "+_tableName
    cursor.execute(insert_query)
    print("Data Load!!")
    
    cursor.close()

start_app()

print("Done") 