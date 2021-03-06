import argparse
import os
from multiprocessing import pool

import cloudinary
from cloudinary.uploader import upload

EXCLUDE_FILES = [
    '.DS_Store'
]

DEFAULT_TAGS = ['gis']


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

    parser.add_argument('--unique-filename', dest='unique_filename', action='store_true',
                        help="""
                        When set to true, add random characters at the end of
                        the filename that guarantee its uniqueness.
                        This parameter is relevant only if use_filename is also set to true.
                        """)
    parser.add_argument('--no-unique-filename', dest='unique_filename', action='store_false',
                        help="""
                        When set to false, does not add random characters at the end of
                        the filename that guarantee its uniqueness.
                        This parameter is relevant only if use_filename is also set to true.
                        """)
    parser.set_defaults(unique_filename=False)

    parser.add_argument('--use-filename', dest='use_filename', action='store_true',
                        help="""
                        When true, the uploaded file's original filename becomes the Public ID. 
                        Random characters are appended to the filename value to ensure Public ID uniqueness 
                        if unique_filename is true.
                        """)
    parser.add_argument('--no-use-filename', dest='use_filename', action='store_false',
                        help="""
                        When false, the Public ID will be comprised of random characters.
                        """)
    parser.set_defaults(use_filename=True)

    parser.add_argument("--exclude-files", '-x', dest='exclude_files', action="append", default=[],
                        help="Exclude files")
    parser.add_argument("--tag", '-t', dest='tags', action="append", default=[],
                        help="Set tags on uploaded files")
    parser.add_argument("--resource-type", '-r', dest='resource_type', action="store",
                        choices=['image', 'raw', 'video', 'auto'],
                        default='auto',
                        help="Set resource type. raw means no transformation on upload")
    parser.add_argument("--concurrent_workers", "-w",
                        type=int,
                        default=10,
                        help="Specify number of concurrent network threads.")

    arguments = parser.parse_args()

    if not arguments.exclude_files:
        arguments.exclude_files = EXCLUDE_FILES

    if not arguments.tags:
        arguments.tags = DEFAULT_TAGS

    return arguments


def upload_file(source_filename, destination_filename, base_folder, tags=[], resource_type='auto'):
    """
    Upload a file to base folder.

    :param source_filename:
    :param destination_filename:
    :param base_folder:
    :param tags:
    :param resource_type:
    :return:
    """
    print('upload_file', base_folder, source_filename, destination_filename)
    result = upload(source_filename, folder=os.path.join(base_folder, os.path.dirname(destination_filename)),
                    use_filename=True, unique_filename=False, tags=tags, resource_type=resource_type)

    return result


def upload_file_concurrent(source_filename,
                           destination_filename,
                           base_folder,
                           options):
    """
    Upload a file to base folder.

    :param source_filename:
    :param destination_filename:
    :param base_folder:
    :param options:
    :return:
    """
    print('upload_file', base_folder, source_filename, destination_filename, options)
    result = upload(source_filename,
                    folder=os.path.join(base_folder, os.path.dirname(destination_filename)),
                    **options)
    print(result)
    return result


def cloudinary_init(cloud_name="sample", api_key="874837483274837", api_secret="a676b67565c6767a6767d6767f676fe1"):
    cloudinary.config(
        cloud_name=cloud_name,
        api_key=api_key,
        api_secret=api_secret
    )


def create_destination_folder(folder):
    """
    Create a remote folder
    This is a noop, since target folders are created on the fly.

    :param folder:
    :return:
    """
    print('create_destination_folder', folder)
    pass


def upload_tree(base_folder, exclude_files=EXCLUDE_FILES, destination_base_folder='.', tags=[], resource_type='auto'):
    """
    Upload a folder with structure

    :param base_folder:
    :param exclude_files:
    :param destination_base_folder:
    :param tags:
    :param resource_type:
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
        results = []
        for filename in files:
            print(subdir, filename)
            if filename in exclude_files:
                print("Ignoring file", filename)
                continue
            result = upload_file(os.path.join(subdir, filename), filename, destination_folder, tags, resource_type)
            results.append(result)

        print(results, len(results))
        # Create every subfolder
        for d in dirs:
            if d in exclude_files:
                print("Ignoring folder", d)
                continue
            create_destination_folder(os.path.join(destination_folder, d))

        print("*" * 10)


def run_tasks_concurrently(func, tasks, concurrent_workers):
    thread_pool = pool.ThreadPool(concurrent_workers)
    thread_pool.starmap(func, tasks)


def upload_tree_concurrent(base_folder,
                           exclude_files=EXCLUDE_FILES,
                           destination_base_folder='.',
                           concurrent_workers=10,
                           **options):
    """
    Upload a folder with structure

    :param base_folder:
    :param exclude_files:
    :param destination_base_folder:
    :param concurrent_workers:
    :param options:
    :return:
    """

    uploads = []
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
            params = (os.path.join(subdir, filename), filename, destination_folder, options)
            uploads.append(params)

        # Create every target subfolder
        for d in dirs:
            if d in exclude_files:
                print("Ignoring folder", d)
                continue
            create_destination_folder(os.path.join(destination_folder, d))

    run_tasks_concurrently(upload_file_concurrent, uploads, concurrent_workers)


if __name__ == "__main__":
    args = parse_args("pycloud-upload", "Upload a tree folder to Cloudinary")
    print(args)

    cloudinary_init(args.cloud_name, args.api_key, args.api_secret)
    upload_tree_concurrent(args.base_folder, exclude_files=args.exclude_files,
                           destination_base_folder=args.destination_folder, tags=args.tags,
                           resource_type=args.resource_type,
                           use_filename=args.use_filename,
                           unique_filename=args.unique_filename)
