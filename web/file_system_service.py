import os
import re
from django.conf import settings
from web.constants import IMAGE_EXTENSION_PATTERN
from web.helpers import get_width_and_height_from_image, safe_unicode_str


class FyleSystemService():

    def __init__(self):
        self.path_prefix = settings.MEDIA_ROOT

    def create_folder(self, path):
        """
        Args:
            path: str: path like object

        """
        try:
            os.makedirs(path)
        except PermissionError:
            raise


    def get_files_from_folder_path(self, path, pattern=None):
        """
        Travels through a directory and returns all the files in it

        Args:
            path: str: path in the system from where to look for the files
            pattern: str: regex to match files

        Returns:
            list: list of files that were found in the path and matched the regex pattern
        """
        files = []
        # Path where to look for files
        lookup_path = self.path_prefix + path
        for filepath in os.listdir(lookup_path.encode()):
            image_extension_pattern_compiled = re.compile(pattern)
            try:
                filename = re.match(image_extension_pattern_compiled, filepath.decode("utf-8")).group(1)
                file_in_path = {
                    'url': ''.join([settings.MEDIA_URL[0:-1], path, filepath.decode("utf-8")]),
                    'name': filename
                }
                if pattern == IMAGE_EXTENSION_PATTERN:
                    try:
                        height, width = get_width_and_height_from_image(path=lookup_path + filepath.decode("utf-8"))
                    except Exception:
                    # could not read image
                        continue
                    file_in_path['width'] = width
                    file_in_path['height'] = height
                files.append(file_in_path)
            except AttributeError:
                # file does not match the extension wanted so we ignore it
                continue
        return files


    def get_folder_names_from_path(self, path):
        """
        Args:
            path(str): path to folder without preceding slash

        Returns:
            list of folders inside path
        """
        full_path = self.path_prefix + path
        return [folder for folder in os.listdir(full_path) if os.listdir(full_path)]


    def get_folders_with_their_contents(self, path):
        contents = {}
        full_path = self.path_prefix + path
        for folder in os.listdir(full_path):
            # We need to add this hack to avoid UnicodeEncodeError with surrogates
            encoded_folder = safe_unicode_str(folder)
            folder_path = os.path.join(full_path, encoded_folder)
            for file in os.listdir(folder_path):
                encoded_file = safe_unicode_str(file)
                if os.path.isfile(os.path.join(folder_path, file)):
                    relative_path = os.path.join(settings.MEDIA_URL, "radio", encoded_folder)
                    file_url = f"{relative_path}/{encoded_file}"
                    try:
                        contents[encoded_folder].append({
                            "name": encoded_file,
                            "url": file_url 
                        })
                    except KeyError:
                        contents[encoded_folder] = [ {"name": encoded_file, "url": file_url} ]
        for folder_name, folder_content in contents.items():
            contents[folder_name] = sorted(folder_content, key=lambda item: item["name"])
        contents = {k:v for k,v in sorted(contents.items(), key=lambda item: item[0])}
        return contents


    def get_side_images(self, path):
        return [os.path.join(settings.MEDIA_URL + path, safe_unicode_str(fn)) for fn in os.listdir(settings.MEDIA_ROOT+path)]