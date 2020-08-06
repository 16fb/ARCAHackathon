### GET Request database data, send to website 
## user sends get request, returns str of json 

# pip3 install -t $PWD pymysql

# 2. (If Using Lambda) Write your code, then zip it all up 
# a) Mac/Linux --> zip -r9 ${PWD}/function.zip 
# b) Windows --> Via Windows Explorer

# Lambda Permissions:
# AWSLambdaVPCAccessExecutionRole

import json
import pymysql
#import psycopg2


#Configuration Values
endpoint = 'db-test.cjthjauaprsn.us-east-1.rds.amazonaws.com'
username = 'sixteenfb'
password = 'nobody16FB;___;'
database_name = 'ARCA'

#Connection
connection = pymysql.connect(endpoint, user=username,
passwd=password, db=database_name,
cursorclass=pymysql.cursors.DictCursor) # seriously? this is all it takes, you gotta be kidding me.

def lambda_handler(event, context):

    # variables
    client_name = 'null' 
    reason = 'null'
    creation_date = 0
    state = 'Rejected'

    #dictonary to store values before send as JSON

    #val = (client_name,reason,creation_date,state)

    try:
        # variables must be enclosed in single quotes apparently.
        query = "SELECT * FROM Forms;"
        cursor = connection.cursor()
        cursor.execute(query)

        # read rows (returns a tuple)
        #row = cursor.fetchone()

        # returns a list of tuples
        lst = cursor.fetchall()
        print("list of tuples data from DB")
        print(lst)

        #print("Testin JSON Object")
        #print(lst[1]['reason'])

    
        # the JSON module has defult way to generate JSON strings
        # only works for 2 value tuples:
        data = json.dumps(lst)
        print("data from DB in JSON format is")
        print(data)

        jsonReply = data

        # Check when json is parsed, still works
        #testjson = json.loads(jsonReply)
        #print("testing json loads")
        #print(testjson[1]["client_name"])
        
        # accept changes
        connection.commit()   

    finally:
        cursor.close()
        #connection.close()


    #jsonReply = json.dumps(data)

    #print("Testing JSON ")
    #print(type(jsonReply))
    #print(jsonReply['1']["reason"])

    return{
        'statusCode':200,
        'body':jsonReply
    }
    
    
    

    

    
lambda_handler(1,1)