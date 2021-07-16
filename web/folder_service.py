from django.conf import settings
from web.s3_helpers import S3Client
from web import file_system_helpers

class FolderService():
    
    @classmethod
    def get_files_from_folder(cls, path):
        if settings.AWS_STORAGE_BUCKET_NAME:
            folder=f"media{path}"
            contents = S3Client.get_s3_objects_from_folder(path=folder)
        else:
            contents = file_system_helpers.get_files_from_folder_path(path=path)
        return contents


    @classmethod
    def get_folder_names_from_path(cls, folder):
        if settings.AWS_STORAGE_BUCKET_NAME:
            folder=f"media{folder}"
            contents = S3Client.get_s3_folders(path=folder)
        else:
            folder = f"{settings.MEDIA_ROOT}{folder}"
            contents = file_system_helpers.get_folder_names_from_path(path=folder)
        return contents


    @classmethod
    def get_radio_contents(cls, path):
        if settings.AWS_STORAGE_BUCKET_NAME:
            path = f"media{path}"
            radio_contents = S3Client.get_folders_with_their_contents(path=path)
        else:
            path = f"{settings.MEDIA_ROOT}/path"
            radio_contents = file_system_helpers.get_radio_contents(path)
        return radio_contents

    @staticmethod
    def _format_side_images(images):
        formatted_images = [image['url'] for image in images]
        return formatted_images

    @classmethod
    def get_side_images(cls, path):
        if settings.AWS_STORAGE_BUCKET_NAME:
            path = f"/{path}"
            images = cls.get_files_from_folder(path)
            images = cls._format_side_images(images)
        else:
            images = file_system_helpers.get_side_images(path=path)
        return images

    