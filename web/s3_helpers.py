
import re

import boto3
from django.conf import settings
from web.helpers import extract_prefix_from_str
from web.constants import IMAGE_EXTENSION_PATTERN

LAST_ITEM_INDEX = -1

class S3Client():
    def __init__(self):
        pass

    @classmethod
    def get_client(cls):
        if not hasattr(cls, 'client'):
            s3_client = boto3.client('s3')
            setattr(cls, 'client', s3_client)
        return getattr(cls, 'client')

    @staticmethod
    def _get_s3_files_from_lookup(result):
        s3_files = []
        result_prefix = f"{settings.MEDIA_ROOT}"
        try:
            for s3_object in result['Contents']:
                if s3_object['Size'] != 0:
                    result_filepath = f"{result_prefix}{extract_prefix_from_str(s3_object['Key'], prefix='media')}"
                    result_folder = S3Client._format_result(
                        filepath=result_filepath,
                        size=s3_object['Size']
                    )
                    s3_files.append(result_folder)
            return s3_files
        except KeyError:
            return []


    def get_s3_folders(bucket=settings.AWS_STORAGE_BUCKET_NAME, path=None):
        folders = []
        client = S3Client.get_client()
        if path[-1] != '/':
            prefix = f"{path}/"
        else:
            prefix = path
        result = client.list_objects(Bucket=bucket, Prefix=prefix, Delimiter='/')
        for folder in result.get('CommonPrefixes', None):
            item = folder.get('Prefix')[:-1]
            folder_formatted = item.split("/")[LAST_ITEM_INDEX]
            folders.append(folder_formatted)
        return folders

    @classmethod
    def get_s3_objects_from_folder(cls, bucket=settings.AWS_STORAGE_BUCKET_NAME, path=None):
        client = S3Client.get_client()
        if path[-1] != '/':
            prefix = f"{path}/"
        else:
            prefix = path
        result = client.list_objects(Bucket=bucket, Prefix=prefix, Delimiter='/')
        print(result)
        return cls._get_s3_files_from_lookup(result)

    @classmethod
    def get_folders_with_their_contents(cls, path):
        folders = cls.get_s3_folders(path=path)
        contents = {}
        for folder in folders:
            complete_path = f"{path}/{folder}"
            objects = cls.get_s3_objects_from_folder(path=complete_path)
            contents[folder] = objects
        return contents
    
    @staticmethod
    def _format_result(filepath, size):
        result = {
            'url': filepath,
            'name': filepath.split('/')[-1]
        }
        if re.match(re.compile(IMAGE_EXTENSION_PATTERN), filepath):
            result['height'] = size
            result['width'] = size

        return result

