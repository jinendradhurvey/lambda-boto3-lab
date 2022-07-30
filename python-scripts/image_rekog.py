import boto3
import logging
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)
metadata_table = os.environ["METADATA_TABLE"]


def lambda_handler(event, context):
    client = boto3.client("rekognition")
    dynamodb_resource = boto3.resource("dynamodb")

    for record in event["Records"]:
        bucket_name = record["s3"]["bucket"]["name"]
        image_obj = record["s3"]["object"]["key"]

    amount_of_faces = 0
    male_face = 0
    female_face = 0
    beard = 0
    mustache = 0
    eyeglasses = 0 

    print(amount_of_faces)
    print(bucket_name)
    print(image_obj)

    response = client.detect_faces(Image={'S3Object':{'Bucket':bucket_name,'Name':image_obj}},Attributes=['ALL'])

    faces = response["FaceDetails"]

    amount_of_faces = len(faces)
    print(amount_of_faces)

    for face in faces:
        if face["Gender"]["Value"] == "Male":
            male_face += 1
        elif face["Gender"]["Value"] == "Female":
            female_face += 1
        
        if face["Beard"]["Value"] == True:
            beard += 1
        if face["Mustache"]["Value"] == True:
            mustache += 1
        if face["Eyeglasses"]["Value"] == True:
            eyeglasses += 1

    table = dynamodb_resource.Table(metadata_table)

    metadata = {
        "filename": image_obj,
        "amount_of_faces": amount_of_faces,
        "male_faces": male_face,
        "female_faces": female_face,
        # sunglases
        "Beard" : beard,
        "Mustache" : mustache,
        "Eyeglasses" : eyeglasses
    }

    table.put_item(Item=metadata)