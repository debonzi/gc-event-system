import os
import json

def get_project_id():
    credentials_path = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
    if not credentials_path:
        return 'UNDEFINED'
    with open(credentials_path) as fp:
        credentials = json.load(fp)
    return credentials.get('project_id')
