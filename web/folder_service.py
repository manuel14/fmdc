from django.conf import settings
from web.s3_service import S3Service
from web.file_system_service import FyleSystemService

class FolderService():

    def __init__(self):
        self.folder_service = self.get_folder_service()

    @staticmethod
    def get_folder_service():
        try:
            settings.AWS_STORAGE_BUCKET_NAME
            folder_service = S3Service()
        except AttributeError:
            folder_service = FyleSystemService()
        return folder_service
    
    def get_files_from_folder(self, path):
        return self.folder_service.get_files_from_folder(path=path)

    def get_folder_names_from_path(self, path):
        contents = self.folder_service.get_folder_names_from_path(path)
        return contents


    def get_folders_with_their_contents(self, path):
        radio_contents = self.folder_service.get_folders_with_their_contents(path)
        return radio_contents

    
    def get_side_images(self, path):
        images = self.folder_service.get_side_images(path)
        return images

    