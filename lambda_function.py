import json
import boto3

CONTENT_TYPE = "Content-Type"
CONTENT_TYPE_VAL = "application/json"
INVOCATION_TYPE = "RequestResponse"
VAL_FUNC = "arn:aws:lambda:eu-central-1:255547448515:function:validateJSON"
CON_FUNC = "arn:aws:lambda:eu-central-1:255547448515:function:convertJSONtoCSV"


def lambda_handler(event, context):
    client = boto3.client("lambda")
    header = event["headers"]

    # Check Content-Type
    if header[CONTENT_TYPE] != CONTENT_TYPE_VAL:
        status_txt = "Wrong Content-Type! Use " + CONTENT_TYPE_VAL
        return {"statusCode": 400, "text": status_txt}

    # Validate JSON
    inputParams = {"JSON": event["body"]}

    resValJSON = client.invoke(
        FunctionName=VAL_FUNC,
        InvocationType=INVOCATION_TYPE,
        Payload=json.dumps(inputParams),
    )

    responseJson = json.load(resValJSON["Payload"])
    for key, value in responseJson.items():
        if key == "statusCode":
            statusCode = value
        elif key == "statusTxt":
            statusTxt = value

    return {"statusCode": statusCode, "text": statusTxt}
