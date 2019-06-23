import argparse
import os

import cloudinary
from cloudinary import uploader

EXCLUDE_FILES = [
    '.DS_Store'
]


def parse_args(app_name, description=None):
    """
    Parse arguments

    :return:
    """
    parser = argparse.ArgumentParser(app_name, description=description,
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--cloud_name", '-c', action="store", help="Cloudinary cloud name", required=True)
    parser.add_argument("--api_key", '-a', action="store", help="Cloudinary API key", required=True)
    parser.add_argument("--api_secret", '-s', action="store", help="Cloudinary API secret", required=True)
    parser.add_argument("base_folder", action="store", help="Base folder to upload")
    parser.add_argument("--destination-folder", '-d', dest='destination_folder', action="store", default=None,
                        help="Destination base folder")
    parser.add_argument("--exclude-files", '-x', dest='exclude_files', action="append", default=[],
                        help="Exclude files")

    args = parser.parse_args()
    return args


def upload_file(source_filename, destination_filename, base_folder):
    """
    Upload a file to base folder.

    :param filename:
    :param source_filename:
    :param destination_filename:
    :param base_folder:
    :return:
    """
    print('upload_file', base_folder, source_filename, destination_filename)
    # result = uploader.upload(source_filename, folder=os.path.join(base_folder, os.path.dirname(destination_filename)),
    #                            use_filename=True, unique_filename=False, tags='gis')
    #
    # print(result)
    pass


def cloudinary_init(cloud_name="sample", api_key="874837483274837", api_secret="a676b67565c6767a6767d6767f676fe1"):
    cloudinary.config(
        cloud_name=cloud_name,
        api_key=api_key,
        api_secret=api_secret
    )


def create_destination_folder(folder):
    """
    Create a remote folder

    :param folder:
    :param base_folder:
    :return:
    """
    print('create_destination_folder', folder)
    pass


def upload_tree(base_folder, exclude_files=EXCLUDE_FILES, destination_base_folder='.'):
    """
    Upload a folder with structure

    :param base_folder:
    :return:
    """

    for subdir, dirs, files in os.walk(base_folder):

        print("Processing", subdir)
        if os.path.basename(subdir) in exclude_files:
            print("Ignoring subdir", subdir)
            continue
        # Upload files
        relative_path = os.path.relpath(subdir, base_folder)

        destination_folder = destination_base_folder
        if relative_path != '.':
            destination_folder = os.path.join(destination_base_folder, relative_path)
        for filename in files:
            print(subdir, filename)
            if filename in exclude_files:
                print("Ignoring file", filename)
                continue
            upload_file(os.path.join(subdir, filename), filename, destination_folder)

        # Upload subfolders
        for d in dirs:
            if d in exclude_files:
                print("Ignoring folder", d)
                continue
            create_destination_folder(os.path.join(destination_folder, d))

        print("*" * 10)


if __name__ == "__main__":

    args = parse_args("upload_tree", "Upload a tree folder to Cloudinary")
    print(args)
    if not args.exclude_files:
        args.exclude_files = EXCLUDE_FILES

    cloudinary_init(args.cloud_name, args.api_key, args.api_secret)
    upload_tree(args.base_folder, args.exclude_files, args.destination_folder)
