import os
import json
import boto3
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# AWS Configuration
AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
SQS_QUEUE_URL = os.getenv('SQS_QUEUE_URL')
S3_BUCKET = os.getenv('S3_BUCKET', 'umfg-cloud-logs-filtered')

# Initialize AWS clients
sqs_client = boto3.client('sqs', region_name=AWS_REGION)
s3_client = boto3.client('s3', region_name=AWS_REGION)

SUBFOLDER = 'version-1424-diego'

def process_message(message):
    """
    Process a single message from SQS queue
    """
    try:
        body = json.loads(message['Body'])

        right_body_event_type = 'eventType' in body and body['eventType'] in ['data_leak', 'system_alert']
        right_body_event_severity = 'metadata' in body and 'severity' in body['metadata'] and body['metadata']['severity'] in ['critical', 'high']

        if right_body_event_type and right_body_event_severity:
            filtered_data = {
                'eventType': 'log_filtered',
                'timestamp': datetime.utcnow().isoformat(),
                'original_message': body
            }
            
            timestamp = datetime.utcnow().strftime('%Y/%m/%d/%H/%M')
            s3_key = f"{SUBFOLDER}/{timestamp}/{message['MessageId']}.json"

            s3_client.put_object(
                Bucket=S3_BUCKET,
                Key=s3_key,
                Body=json.dumps(filtered_data, indent=2),
                ContentType='application/json'
            )
            
            print(f"Successfully processed message {message['MessageId']}")
            return True

        return False
            
    except json.JSONDecodeError:
        print(f"Error decoding JSON from message {message['MessageId']}")
        return False
    except Exception as e:
        print(f"Error processing message {message['MessageId']}: {str(e)}")
        return False

def main():
    """
    Main function to poll SQS queue and process messages
    """
    print(f"Starting to poll queue: {SQS_QUEUE_URL}")
    print(f"Filtering for field: {FILTER_FIELD}")
    print(f"Saving to bucket: {S3_BUCKET}")
    
    while True:
        try:
            # Receive messages from SQS
            response = sqs_client.receive_message(
                QueueUrl=SQS_QUEUE_URL,
                MaxNumberOfMessages=1,
                WaitTimeSeconds=10
            )
            
            messages = response.get('Messages', [])
            
            if not messages:
                print("No messages received")
                continue
            

            if process_message(message):
                # Delete message from queue if successfully processed
                sqs_client.delete_message(
                    QueueUrl=SQS_QUEUE_URL,
                    ReceiptHandle=message['ReceiptHandle']
                )
                    
        except Exception as e:
            print(f"Error in main loop: {str(e)}")
            continue

if __name__ == "__main__":
    main()