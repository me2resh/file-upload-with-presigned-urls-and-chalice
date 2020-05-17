from chalice import Chalice
import boto3
import logging
from botocore.exceptions import ClientError

app = Chalice(app_name='file-upload')
bucket_name = "chalice-file-upload-example"
expiration = 1800


@app.route('/get-upload-url', methods=['POST'])
def get_upload_url():

    request = app.current_request
    payload = request.json_body
    object_name = payload['filename']

    s3_client = boto3.client('s3')
    try:
        response = s3_client.generate_presigned_post(bucket_name,
                                                     object_name,
                                                     ExpiresIn=expiration)
    except ClientError as e:
        app.log.error(e)
        return None

    return response


@app.route('/get-download-url', methods=['POST'])
def get_download_url():

    request = app.current_request
    payload = request.json_body
    object_name = payload['filename']

    s3_client = boto3.client('s3')
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except ClientError as e:
        app.log.error(e)
        return None

    return response
