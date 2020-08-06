import boto3

# send SMS, for singapore numbers right now
def lambda_handler(event, context):
    contact_number = '91152694'  
    case_result = 'Accepted'

    contact_number = event['contact_number']
    case_result = event['case_result']


    print('contact_number is: ',contact_number)
    print('case_result is: ',case_result)

    sns = boto3.client('sns')

    number = '+65' + contact_number
    
    if (case_result == 'Accepted'):
        print('Accepted')
        message = "Congratulations, your appeal case has been Accepted"

    elif (case_result == 'Rejected'):
        print('Rejected')
        message = "We regret to inform you your appeal case has been REJECTED"

    sns.publish(PhoneNumber = number, Message = message, MessageAttributes={
            'AWS.SNS.SMS.SMSType': {
                'DataType': 'String',
                'StringValue': 'Transactional'
            }
        })


    return {
        'case_result': case_result,
        'contact_number': contact_number
    }
     