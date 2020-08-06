import json
import pymysql

#Configuration Values
endpoint = 'db-test.cjthjauaprsn.us-east-1.rds.amazonaws.com'
username = 'sixteenfb'
password = 'nobody16FB;___;'
database_name = 'ARCA'

#Connection
connection = pymysql.connect(endpoint, user=username,
passwd=password, db=database_name)

print('Loading function')

def lambda_handler(event, context):
    # event is a JSON
    #print("EVENT JSON IS")
    #print(event)
    
    #body = event['body']

    #print("BODY IS")
    #print(body)

    #body = json.loads(body)

    #Parse for POST request 
    #client_name = body['client_name']
    #reason = body['reason']
    #creation_date = body['creation_date']
    #state = body['state']
    
    # Parse out query string params (GET REQUEST)
    client_name = event['queryStringParameters']['client_name']
    reason = event['queryStringParameters']['reason']
    creation_date = event['queryStringParameters']['creation_date']
    state = event['queryStringParameters']['state']
    contact_number = event['queryStringParameters']['contact_number']


    # print out all parameters
    print('client_name=' + client_name)
    print('reason=' + reason)
    print('creation_date=' + creation_date)
    print('state=' + state)
    print('contact_number=' + contact_number)


    #todo make this nicer
    #variables
    client_name = client_name 
    reason = reason
    creation_date = creation_date
    state = state
    contact_number = contact_number

    val = [client_name,reason,creation_date,state,contact_number]
    
    # run thorugh values in rules engine
    val = rulesEngine(val)

    try:
        # variables must be enclosed in single quotes apparently.
        query = "INSERT INTO Forms (client_name, reason, creation_date, state, contact_number) VALUES (%s,%s,%s,%s,%s)" #.format(client_name,reason,creation_date) 

        cursor = connection.cursor()
        cursor.execute(query,val)

        # accept changes
        connection.commit()   

    finally:
        cursor.close()
        #connection.close()



    #2. Construct the body of the response object
    transactionResponse = {}
    transactionResponse['client_name'] = client_name
    transactionResponse['reason'] = reason
    transactionResponse['creation_date'] = creation_date
    transactionResponse['state'] = state
    transactionResponse['contact_number'] = contact_number
    transactionResponse['message'] = 'Database Updated'

    #3. Construct http response object
    responseObject = {}
    responseObject['statusCode'] = 200
    responseObject['headers'] = {}
    responseObject['headers']['Content-Type'] = 'application/json'
    responseObject['body'] = json.dumps(transactionResponse)

    print("function completed")

    #4. Return the response object
    return responseObject
    
# Rules Engine, check if reason is empty, if so reject 
def rulesEngine(val):
    if val[1] == "":
        val[3] = "Rejected"
    return val
    