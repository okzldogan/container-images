#!/usr/bin/env python

import os
import json
import subprocess
import datetime

from google.cloud import secretmanager
from google.cloud import storage

# Set project_id by getting the environment variables using os.environ.get

project_id = os.environ.get("PROJECT_ID")
bucket_name = os.environ.get("BUCKET_NAME")

# Get the current date and time

current_date_and_time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
date_only = datetime.datetime.now().strftime("%Y-%m-%d")

def create_db_backup(project_id, bucket_name):

    # Iniatiate the GCP secret manager client
    secret_manager_client = secretmanager.SecretManagerServiceClient()

    # List the backup user secret in the project

    get_backup_user_secret = secret_manager_client.list_secrets(
        {
            "parent": f"projects/{project_id}",
            "filter": "name:backup"
        }
    )

    backup_user_secret_name = get_backup_user_secret.secrets[0].name

    # Set the secret name
    latest_secret_version = f"{backup_user_secret_name}/versions/latest"

    # Get the secret
    secret_response = secret_manager_client.access_secret_version(request={"name": latest_secret_version})

    # Parse the JSON output of secret_response
    backup_sa_credentials_json  = json.loads(secret_response.payload.data.decode("UTF-8"))
    mysql_backup_username       = backup_sa_credentials_json['username']
    mysql_backup_user_password  = backup_sa_credentials_json['password']
    connection_host             = backup_sa_credentials_json['host']
    mysql_db_name               = backup_sa_credentials_json['database']

    print(f"Initiating database backup cronjob for {mysql_db_name} db...")

    try:

        # Compose the mysqldump command
        db_backup_command = f"mysqldump -u {mysql_backup_username} -p{mysql_backup_user_password} -h {connection_host} --no-tablespaces --triggers --routines --single-transaction -f {mysql_db_name} > /tmp/{mysql_db_name}-{current_date_and_time}.sql"

        # Execute the mysqldump command
        run_command = subprocess.run(db_backup_command, capture_output=True, check=True, shell=True)


    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        exit()

    # If the file /tmp/{mysql_db_name}-{current_date_and_time}.sql exists, print the success message

    if os.path.exists(f"/tmp/{mysql_db_name}-{current_date_and_time}.sql"):
        print(f"Backup file /tmp/{mysql_db_name}-{current_date_and_time}.sql created successfully.")

        print("Authenticating to Google Cloud Storage...")
        # Authenticate to google cloud storage and upload the backup file
        storage_client = storage.Client()

        # Set the source file and destination folder and blob name
        source_file = f"/tmp/{mysql_db_name}-{current_date_and_time}.sql"
        destination_folder = f"db-backups/{date_only}/"
        destination_blob_name =  destination_folder + f"{mysql_db_name}-{current_date_and_time}.sql"

        # Upload the file to the bucket

        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)

        print(f"Uploading file {source_file} to {bucket_name}...")

        response = blob.upload_from_filename(source_file)

        # If upload fails, exit the script
        if response == 0:
            print(f"Uploading to {bucket_name} failed. Exiting script...")
            exit()

        # If upload succeeds, continue with the script
        else:
            print(f"Uploading file {destination_blob_name} succeeded.")
            pass
        
    else:
        print(f"Backup file /tmp/{mysql_db_name}-{current_date_and_time}.sql does not exist. Exiting script...")
        exit()


create_db_backup(project_id, bucket_name)