import json
import pymysql
import boto3

#Configuration Values
endpoint = 'db-test.cjthjauaprsn.us-east-1.rds.amazonaws.com'
username = 'sixteenfb'
password = 'nobody16FB;___;'
database_name = 'ARCA'
 
# Define the client to interact with AWS Lambda !!!
client = boto3.client('lambda')

#Connection
connection = pymysql.connect(endpoint, user=username,
passwd=password, db=database_name)

print('Loading function')

def lambda_handler(event, context):

    # initialise + set values for testing
    case_id = 0
    state = 0
    contact_number = 0

    # Parse out query string params (GET REQUEST)
    try:
        case_id = event['queryStringParameters']['id']
        state = event['queryStringParameters']['result']
    except:
        responseObject = {}
        responseObject['statusCode'] = 205
        responseObject['body'] = "Inputs not recognised"
        return responseObject


    # print out all parameters
    print('case_id = ' , case_id)
    print('type of case_id is = ', type(case_id))
    print('state = ' , state)
    print('type of state is = ', type(state))


    try:
        # variables must be enclosed in single quotes apparently.
        #query = "INSERT INTO Forms (client_name, reason, creation_date, state) VALUES (%s,%s,%s,%s)" #.format(client_name,reason,creation_date) 
        query = "UPDATE Forms SET state = %s WHERE id = %s;"
        val = [state,case_id]

        cursor = connection.cursor()
        cursor.execute(query,val)

        ### obtain phone number of specific case_id
        query = "SELECT contact_number FROM Forms"
        val = []

        cursor.execute(query,val)

        lst = cursor.fetchone() # returns tuple of size 1
        print("phone number of case id", lst[0])
        contact_number = str(lst[0])

        # accept changes
        connection.commit()   

    finally:
        cursor.close()
        #connection.close()


    ### Call lambda function sendToSNS to notify client
    inputParams = {
        "contact_number" : contact_number,
        'case_result' : state
    }

    response = client.invoke(
        FunctionName = 'arn:aws:lambda:us-east-1:607199713421:function:sendSNS',
        InvocationType = 'RequestResponse',
        Payload = json.dumps(inputParams)
    )
 
    responseFromChild = json.load(response['Payload'])

    print("response from child function is:", responseFromChild)



    #2. Construct the body of the response object
    transactionResponse = {}
    transactionResponse['case_id'] = case_id
    transactionResponse['message'] = 'Database Case State Updated, SMS sent to client'
    transactionResponse['contact_number'] = responseFromChild['contact_number']
    transactionResponse['case_result'] = responseFromChild['case_result']


    #3. Construct http response object
    responseObject = {}
    responseObject['statusCode'] = 200
    responseObject['headers'] = {}
    responseObject['headers']['Content-Type'] = 'application/json'
    responseObject['body'] = json.dumps(transactionResponse)

    print("function completed")

    #4. Return the response object
    return responseObject
    


#lambda_handler(1,1)