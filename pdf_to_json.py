#!/usr/bin/env python
# -*-coding:utf-8 -*-
#
#-----------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------
# File       : pdf_to_json.py
# Author     : BMV System Integration Pvt Ltd.
# Version    : 1.0.0
# Date       : 02nd January 2023
# Contact    : info@systemintegration.in
# Purpose    : This is the python script to extraxt the texts from pdf file and write it into json file.
# import     : tabula - to extract the texts from pdf file.
#              json   - to convert the data into json data.
#              csv    - to read the csv file.
#              os     - to perform os related commands.
#-----------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------

try:
    import tabula
except Exception as E:
    print("Exception : 'tabula' is not installed", )
import csv
import json
import os

PDF_FILE = "C:\\Users\\bmvsi-117\\Documents\\POC\\india_population.pdf" # path to PDF file
JSON_FILE = "C:\\Users\\bmvsi-117\\Documents\\POC\\india_population_json.json" # path to JSON file

def csv_to_json(csv_file, json_file):
    """
    Convert CSV file to JSON file

    param : csv_file - path to csv file
            json_file - path to JSON file
    """
    data_dict = {}
    with open(csv_file, encoding="utf-8") as cfile:
        cfilereader = csv.DictReader(cfile)

        # get csv content in dictionary
        for row in cfilereader:
            state = row['States /UTs']
            data_dict[state] = row
    # print(data_dict)

    os.remove(csv_file) # remove csv file

    with open(json_file, 'w', encoding='utf-8') as jfile:
        jfile.write(json.dumps(data_dict))
    if os.path.exists(json_file):
        return True
    else:
        False

def pdf_to_json(pdffile, jsonfile):
    """
    Converts PDF file to JSON file

    Params : pdffile - path to PDF file
             jsonfile - path to JSON file
    """

    try:
        if not os.path.exists(pdffile):
            raise Exception("PDF not found!!")

        df = tabula.read_pdf(pdffile, pages='1',stream=True, multiple_tables=False, silent=True, area=[ 108.776,58.286,624.071,541.653])
        df[0] = df[0].dropna(axis=1) # removed column with NAN
        df[0] = df[0].drop(0) # removed extra row

        temp_csv = "C:\\Users\\bmvsi-117\\Documents\\POC\\india_population_csv.csv" # path to temporary CSV file

        df[0].to_csv(temp_csv, encoding="utf-8", index=False)
        done = csv_to_json(temp_csv, jsonfile)
        if done:
            return jsonfile
        else:
            return None
    except Exception as e:
        print("Exception :", e)

if __name__ == "__main__":
    res = pdf_to_json(PDF_FILE, JSON_FILE)
    if res is None:
        print("Exception in getting JSON file!")