"""
@uthor Shanthanu Varma
A module to query AWS DynamoDB tables
Will need aws-cli installed and signed in OR will require this to run on an AWS
EC2 instance
"""
from datetime import datetime as dt
import pandas as pd
import boto3
import sys
from boto3.dynamodb.conditions import Key

ts = dt.fromtimestamp
TABLENAME = 'name_of_your_table'
KEY_NAME = 'key_to_query'
REGIONS = [] # A string list of the region or regions your project has

# This module receives a list of sessions and checks Dynamo in the two regions
# to extract the corresponding user chats and returns a DF with the chats
def get_data(qid, region):
    print('Checking', region, 'for', session)
    sys.stdout.write("\033[F")
    sys.stdout.write("\033[K")
    DB_TYPE = 'dynamodb'
    dynamodb = boto3.resource(DB_TYPE,
                              region_name=region
                             )
    table = dynamodb.Table(TABLENAME)
    response = table.query(
                KeyConditionExpression=Key(KEY_NAME).eq(qid)
                          )
    try:
        #print(response)
        #answer = input()
        #if answer == 'exit':
        #    exit()
        items = response["Items"]
        #print(items)
        #input()
        for i, item in enumerate(items):
            # Do Some Things
            result = 'some transformation of the retrieved data'
    except:
        return None
    return result


def query(query_ids):
    total = len(query_ids)
    all_data = []
    for i, qid in enumerate(query_ids):
        sys.stdout.write("\033[F")
        sys.stdout.write("\033[K")
        print('Doing '+str(i+1)+'. Remaining '+str(total-i-1))
        data = None
        r = 0 # to search each region in REGIONS
        try:
            while not data and r < len(REGIONS): # Stops if data is found or all regions are queried
                data = get_data(qid, REGIONS[r])
                if data:
                    all_data.append(data)
                #print(data,1)
                #input()
                r += 1
            if not data:
                print('Not in any region')
        except:
            print ('Something went Wrong')
            #input()
    return all_data
