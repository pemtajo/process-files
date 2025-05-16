import json
from datetime import datetime

def process_message(body):
    """
    Simula o processamento de uma única mensagem de log
    """
    try:
        event_type = body.get('eventType')  
        severity = body.get('severity')  

        # Processa logs com eventType em ['data_leak', 'system_alert'] e severity em ['critical', 'high']
        if event_type in ['data_leak', 'system_alert']:
            if severity in ['critical', 'high']:  
                filtered_data = {
                    'eventType': 'log_filtered',
                    'timestamp': datetime.utcnow().isoformat(),
                    'original_message': body
                }
                print(f"Successfully processed: {json.dumps(filtered_data, indent=2)}")
                return True
            else:
                print(f"Log com severity inválido: {json.dumps(body, indent=2)}")
        else:
            print(f"Log com eventType inválido: {json.dumps(body, indent=2)}")

        return False
    except json.JSONDecodeError:
        print(f"Error decoding JSON from message")
        return False
    except Exception as e:
        print(f"Error processing message: {str(e)}")
        return False

# Testes

# Log com severity e eventType corretos
log_1 = {
    "eventType": "data_leak",
    "severity": "critical",
    "timestamp": "2025-05-16T18:21:24.331537",
    "additionalData": {
        "browser": "Edge",
        "ip": "127.0.0.104",
        "sessionId": "824daa06-6a01-42c6-8739-c45237b5af57",
        "userAgent": "Mozilla/5.0 (Linux)"
    }
}

# Log com severity e eventType incorretos
log_2 = {
    "eventType": "error_occurred",
    "severity": "critical",
    "timestamp": "2025-05-16T18:21:24.331537",
    "additionalData": {
        "browser": "Edge",
        "ip": "127.0.0.104",
        "sessionId": "824daa06-6a01-42c6-8739-c45237b5af57",
        "userAgent": "Mozilla/5.0 (Linux)"
    }
}

# Log sem severity
log_3 = {
    "eventType": "data_leak",
    "timestamp": "2025-05-16T18:21:24.331537",
    "additionalData": {
        "browser": "Edge",
        "ip": "127.0.0.104",
        "sessionId": "824daa06-6a01-42c6-8739-c45237b5af57",
        "userAgent": "Mozilla/5.0 (Linux)"
    }
}

# Log com eventType incorreto e sem severity
log_4 = {
    "eventType": "error_occurred",
    "timestamp": "2025-05-16T18:21:24.331537",
    "additionalData": {
        "browser": "Edge",
        "ip": "127.0.0.104",
        "sessionId": "824daa06-6a01-42c6-8739-c45237b5af57",
        "userAgent": "Mozilla/5.0 (Linux)"
    }
}

# Testando os logs
print("Testando Log 1 (com severity e eventType corretos):")
process_message(log_1)

print("\nTestando Log 2 (com severity e eventType incorretos):")
process_message(log_2)

print("\nTestando Log 3 (sem severity):")
process_message(log_3)

print("\nTestando Log 4 (com eventType incorreto e sem severity):")
process_message(log_4)
