''' PodWorker | modules | upload.py '''

import os
import time
import threading
from io import BytesIO

from PIL import Image
from boto3 import session
from botocore.config import Config


# --------------------------- S3 Bucket Connection --------------------------- #
bucket_session = session.Session()

boto_config = Config(
    signature_version='s3v4',
    retries={
        'max_attempts': 3,
        'mode': 'standard'
    }
)

if os.environ.get('BUCKET_ENDPOINT_URL', None) is not None:
    boto_client = bucket_session.client(
        's3',
        endpoint_url=os.environ.get('BUCKET_ENDPOINT_URL', None),
        aws_access_key_id=os.environ.get('BUCKET_ACCESS_KEY_ID', None),
        aws_secret_access_key=os.environ.get('BUCKET_SECRET_ACCESS_KEY', None),
        config=boto_config
    )
else:
    boto_client = None  # pylint: disable=invalid-name


# ---------------------------------------------------------------------------- #
#                                 Upload Image                                 #
# ---------------------------------------------------------------------------- #
def upload_image(job_id, image_location, result_index=0, results_list=None):
    '''
    Upload image to bucket storage.
    '''
    if boto_client is None:
        # Save the output to a file
        output = BytesIO()
        img = Image.open(image_location)
        img.save(output, format=img.format)

        os.makedirs("uploaded", exist_ok=True)
        with open(f"uploaded/{result_index}.png", "wb") as file_output:
            file_output.write(output.getvalue())

        return f"uploaded/{result_index}.png"

    output = BytesIO()
    img = Image.open(image_location)
    img.save(output, format=img.format)

    bucket = time.strftime('%m-%y')

    # Upload to S3
    boto_client.put_object(
        Bucket=f'{bucket}',
        Key=f'{job_id}/{result_index}.png',
        Body=output.getvalue(),
        ContentType="image/png"
    )

    output.close()

    presigned_url = boto_client.generate_presigned_url(
        'get_object',
        Params={
            'Bucket': f'{bucket}',
            'Key': f'{job_id}/{result_index}.png'
        }, ExpiresIn=604800)

    if results_list is not None:
        results_list[result_index] = presigned_url

    return presigned_url


# ---------------------------------------------------------------------------- #
#                                Files To Upload                               #
# ---------------------------------------------------------------------------- #
def files(job_id, file_list):
    '''
    Uploads a list of files in parallel.
    Once all files are uploaded, the function returns the presigned URLs list.
    '''
    upload_progress = []  # List of threads
    file_urls = [None] * len(file_list)  # Resulting list of URLs for each file

    for index, file in enumerate(file_list):
        new_upload = threading.Thread(
            target=upload_image,
            args=(job_id, file, index, file_urls)
        )

        new_upload.start()
        upload_progress.append(new_upload)

    # Wait for all uploads to finish
    for upload in upload_progress:
        upload.join()

    return file_urls
