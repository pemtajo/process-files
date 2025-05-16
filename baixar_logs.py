import boto3
from datetime import datetime
import os

os.environ["AWS_ACCESS_KEY_ID"] = "AKIA6CWM3FEG3LWDAF53"
os.environ["AWS_SECRET_ACCESS_KEY"] = "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"

s3 = boto3.client('s3')
bucket_name = "cloud-umfg-2025-logs"
cutoff_date = datetime.strptime("2025-05-15", "%Y-%m-%d")

# Lista os arquivos
response = s3.list_objects_v2(Bucket=bucket_name)

if "Contents" in response:
    recent_logs = [
        obj["Key"] for obj in response["Contents"]
        if obj["LastModified"].replace(tzinfo=None) >= cutoff_date
    ]
    
    # Baixa os primeiros arquivos para análise
    for key in recent_logs[:3]:
        filename = key.split("/")[-1]
        print(f"Baixando {key} como {filename}...")
        s3.download_file(bucket_name, key, filename)

    print("Download concluído.")
else:
    print("Nenhum arquivo encontrado no bucket.")
