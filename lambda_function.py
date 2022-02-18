import json
import boto3

CONTENT_TYPE = "Content-Type"
CONTENT_TYPE_VAL = "application/json"
INVOCATION_TYPE = "RequestResponse"
VAL_FUNC = "arn:aws:lambda:eu-central-1:255547448515:function:validateJSON"
CON_FUNC = "arn:aws:lambda:eu-central-1:255547448515:function:convertJSONtoCSV"
STATUS_OK = 200
STATUS_ERROR = 400

def lambda_handler(event, context):
    client = boto3.client("lambda")
    header = event["headers"]

    # Check Content-Type
    if header[CONTENT_TYPE] != CONTENT_TYPE_VAL:
        status_txt = "Wrong Content-Type! Use " + CONTENT_TYPE_VAL
        print(status_txt)
        return {"statusCode": STATUS_ERROR, "body": status_txt}

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

    print(responseJson)

    if statusCode != STATUS_OK:
        return {"statusCode": statusCode, "body": statusTxt}

    # Convert JSON to CSV
    inputParams = {"JSON": event["body"]}

    resConvJSON = client.invoke(
        FunctionName=CON_FUNC,
        InvocationType=INVOCATION_TYPE,
        Payload=json.dumps(inputParams),
    )

    responseJson = json.load(resConvJSON["Payload"])
    print(responseJson)
    for key, value in responseJson.items():
        if key == "statusCode":
            statusCode = value
        elif key == "headers":
            headers = value
        elif key == "body":
            data = value
        elif key == "isBase64Encoded":
            encoded = value

    if statusCode != STATUS_OK:
        return {"statusCode": statusCode, "body": data}

    return {
        "headers": headers,
        "statusCode": statusCode,
        "body": data,
        "isBase64Encoded": encoded,
    }