""" upload files to DigitalOcean Spaces """

from boto3 import session
from werkzeug.utils import secure_filename

from config import Config


# Initiate session
session = session.Session()
s3_client = session.client(
    "s3",
    region_name="fra1",
    endpoint_url=Config.DIGITAL_OCEAN_SPACES_BUCKET_ENDPOINT,
    aws_access_key_id=Config.DIGITAL_OCEAN_SPACES_ACCESS_ID,
    aws_secret_access_key=Config.DIGITAL_OCEAN_SPACES_SECRET_KEY,
)


def upload_file_to_spaces(file) -> str:

    file_path = Config.DIGITAL_OCEAN_SPACES_IMAGE_FOLDER + "/" + secure_filename(file.filename)

    try:
        s3_client.upload_fileobj(file, "aqar-plus-images", file_path, ExtraArgs={"ACL": "public-read"})

    except Exception as e:
        # This is a catch all exception, edit this part to fit your needs.
        print("Something Happened: ", e)
        return e
    print("File uploaded successfully: ", file_path)
    # after upload file to s3 bucket, return filename of the uploaded file
    return file_path


def delete_file_from_spaces(file_path):
    try:
        s3_client.delete_object(
            Bucket="aqar-plus-images",
            Key=file_path,
        )
    except Exception as e:
        print("Something Happened: ", e)
        return e

    return True


def get_spaces_file_origin_url(file_path):
    return Config.DIGITAL_OCEAN_SPACES_BUCKET_ENDPOINT + "/" + Config.DIGITAL_OCEAN_SPACES_BUCKET_NAME + "/" + file_path


def get_spaces_file_cdn_url(file_path):
    return (
        Config.DIGITAL_OCEAN_SPACES_BUCKET_CDN_ENDPOINT
        + "/"
        + Config.DIGITAL_OCEAN_SPACES_BUCKET_NAME
        + "/"
        + file_path
    )


def extract_file_path_from_url(url):
    if Config.DIGITAL_OCEAN_SPACES_BUCKET_ENDPOINT in url:
        return url.replace(Config.DIGITAL_OCEAN_SPACES_BUCKET_ENDPOINT + "/", "")
    elif Config.DIGITAL_OCEAN_SPACES_BUCKET_CDN_ENDPOINT in url:
        return url.replace(Config.DIGITAL_OCEAN_SPACES_BUCKET_CDN_ENDPOINT + "/", "")

    raise ValueError("Invalid Spaces URL")
