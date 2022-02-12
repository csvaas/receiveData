import json
import boto3

CONTENT_TYPE = "Content-Type"
CONTENT_TYPE_VAL = "application/json"


def lambda_handler(event, context):
    #client = boto3.client("lambda")
    header = event["headers"]

    # Check Content-Type
    if header[CONTENT_TYPE] != CONTENT_TYPE_VAL:
        return {"statusCode": 400, "text": json.loads(header)}

    return {"statusCode": 200, "text": json.loads(header)}
