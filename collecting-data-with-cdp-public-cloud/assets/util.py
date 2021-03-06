#****************************************************************************
# (C) Cloudera, Inc. 2020-2021
#  All rights reserved.
#
#  Applicable Open Source License: GNU Affero General Public License v3.0
#
#  NOTE: Cloudera open source products are modular software products
#  made up of hundreds of individual components, each of which was
#  individually copyrighted.  Each Cloudera open source product is a
#  collective work under U.S. Copyright Law. Your license to use the
#  collective work is as provided in your written agreement with
#  Cloudera.  Used apart from the collective work, this file is
#  licensed for your use pursuant to the open source license
#  identified above.
#
#  This code is provided to you pursuant a written agreement with
#  (i) Cloudera, Inc. or (ii) a third-party authorized to distribute
#  this code. If you do not have a written agreement with Cloudera nor
#  with an authorized and properly licensed third party, you do not
#  have any rights to access nor to use this code.
#
#  Absent a written agreement with Cloudera, Inc. (“Cloudera”) to the
#  contrary, A) CLOUDERA PROVIDES THIS CODE TO YOU WITHOUT WARRANTIES OF ANY
#  KIND; (B) CLOUDERA DISCLAIMS ANY AND ALL EXPRESS AND IMPLIED
#  WARRANTIES WITH RESPECT TO THIS CODE, INCLUDING BUT NOT LIMITED TO
#  IMPLIED WARRANTIES OF TITLE, NON-INFRINGEMENT, MERCHANTABILITY AND
#  FITNESS FOR A PARTICULAR PURPOSE; (C) CLOUDERA IS NOT LIABLE TO YOU,
#  AND WILL NOT DEFEND, INDEMNIFY, NOR HOLD YOU HARMLESS FOR ANY CLAIMS
#  ARISING FROM OR RELATED TO THE CODE; AND (D)WITH RESPECT TO YOUR EXERCISE
#  OF ANY RIGHTS GRANTED TO YOU FOR THE CODE, CLOUDERA IS NOT LIABLE FOR ANY
#  DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, PUNITIVE OR
#  CONSEQUENTIAL DAMAGES INCLUDING, BUT NOT LIMITED TO, DAMAGES
#  RELATED TO LOST REVENUE, LOST PROFITS, LOSS OF INCOME, LOSS OF
#  BUSINESS ADVANTAGE OR UNAVAILABILITY, OR LOSS OR CORRUPTION OF
#  DATA.
#
#  Source File Name: util.py
#  Description: Helper functions used in data_generator.py
#  Author(s): Nicolas Pelaez
#***************************************************************************/
from random import randint,uniform,gauss
import numpy as np
import time
from datetime import timedelta

#Factory 2 is going to be in Alaska (Much colder)
#Factory 4 is going to be in Texas (Much hotter)

def getambientdata(factory_id,date):
    ambient_data = []
    if(factory_id==2):
        temp = randint(-35,15) #Celsius
        humidity = randint(0,60) #Percent
        Celsius = randint(1010,1040) #millibar
    elif(factory_id==4):
        temp = randint(0,30) #Celsius
        humidity = randint(0,100) #Percent
        Celsius = randint(1010,1040) #millibar
    else:
        temp = randint(-10,25) #Celsius
        humidity = randint(0,100) #Percent
        Celsius = randint(1010,1040) #millibar
    ambient_data.append([factory_id,date,temp,humidity,Celsius])
    export_data = np.array(ambient_data).ravel()
    return export_data

def getmachinedata(factory_id,machine_id,date_string,date_actual):
    factory_data = []
    timestamp_start = time.mktime(date_actual.timetuple())
    nextday = date_actual + timedelta(days=1)
    timestamp_end = time.mktime(nextday.timetuple())
    if(factory_id==2):
        reporting_slices = 18
    elif(factory_id==4):
        reporting_slices = 22
    else:
        reporting_slices = 20
    for reports in range(1,reporting_slices):
        part_no = chr(96 + machine_id) + '42CLDR'
        timestamp = uniform(timestamp_start,timestamp_end)
        serial_no = part_no + '01' + str(factory_id) + '666' + str(int(timestamp))
        factory_data.append([factory_id,machine_id,part_no,serial_no,timestamp])

    return factory_data

def getemployeedata(factory_id,employee_id,date,sourcetype):
    employee_data = []
    if(factory_id==2):
        time_worked = round(gauss(7,2),2)
        if(randint(0,1000) % 48 == 0):
            vacation = 1
        else:
            vacation = 0
        if(randint(0,1000) % 30 == 0):
            sick = 1
        else:
            sick = 0
    elif(factory_id==4):
        time_worked = round(gauss(8,1),2) #Change to gauss
        if(randint(0,1000) % 20 == 0):
            vacation = 1
        else:
            vacation = 0
        if(randint(0,1000) % 60 == 0):
            sick = 1
        else:
            sick = 0
    else:
        time_worked = round(gauss(8,2),2)
        if(randint(0,1000) % 30 == 0):
            vacation = 1
        else:
            vacation = 0
        if(randint(0,1000) % 48 == 0):
            sick = 1
        else:
            sick = 0
    if(sourcetype == "Logs"):
        employee_data.append([factory_id,employee_id,time_worked,date])
    if(sourcetype == "Vacation"):
        employee_data.append([factory_id,employee_id,vacation,date])
    if(sourcetype == "Sick"):
        employee_data.append([factory_id,employee_id,sick,date])
    exportdata = np.array(employee_data).ravel()
    return exportdata

def getemployeemetadata(factory_id,employee_id,faker):
    employee_metadata = []
    employee = faker.profile()
    salary = round(uniform(60000,120000),2)

    employee_metadata.append([factory_id,employee_id,employee['sex'],
                            employee['mail'],employee['job'],
                            employee['birthdate'],salary])
    exportdata = np.array(employee_metadata).ravel()
    return exportdata
