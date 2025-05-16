# SQS Message Processor

This application processes messages from an Amazon SQS queue, filters them for specific security events, and saves the filtered data to an S3 bucket in a structured format.

## Features

- Polls messages from an SQS queue
- Filters messages for specific security events ('system_alert' and 'data_leak')
- Saves filtered messages to S3 with timestamp-based organization
- Handles JSON parsing and error cases
- Configurable through environment variables
- Docker support for easy deployment

## Prerequisites

- Python 3.9 or higher
- Docker and Docker Compose (for containerized deployment)
- AWS account with appropriate permissions for SQS and S3
- AWS credentials configured

## Configuration

Copy the `.env-example` file to `.env` and configure the following variables:

```bash
# AWS Configuration
AWS_ACCESS_KEY_ID=your_access_key_id
AWS_SECRET_ACCESS_KEY=your_secret_access_key
AWS_REGION=us-east-1

# SQS Configuration
SQS_QUEUE_URL=https://sqs.us-east-1.amazonaws.com/your-account-id/your-queue-name

# S3 Configuration
S3_BUCKET=umfg-cloud-logs-filtered
```

## Running the Application

### Using Docker

1. Build and start the container:
```bash
docker-compose up -d
```

2. View logs:
```bash
docker-compose logs -f
```

### Running Locally

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python sqs_processor.py
```

## Message Processing

The application processes messages in the following example way:

```json
{
    "eventType": "user_login",
    "userId": "123",
    "timestamp": "2024-03-20T10:00:00Z",
    "additionalData": {
        "browser": "Chrome",
        "ip": "192.168.1.1"
    }
}
```

1. Receives messages from the configured SQS queue
2. Filters messages for specific event types:
   - system_alert
   - data_leak
3. For matching messages, creates a filtered version with:
   - eventType: 'log_filtered'
   - timestamp: current UTC time
   - original_message: complete original message

## Output Structure

Filtered messages are saved in the S3 bucket with the following structure:

```
bucket/
  └── security-profpedro/
      └── YYYY/
          └── MM/
              └── DD/
                  └── HH/
                      └── MM/
                          └── message-id.json
```

Each saved file contains:
- The filtered event type
- Processing timestamp
- Original message content

## Error Handling

The application includes error handling for:
- JSON parsing errors
- AWS service errors
- Network issues

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
