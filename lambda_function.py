import json
import boto3


def lambda_handler(event, context):
    client = boto3.client("lambda")

    return {"statusCode": 200}
