Cloudinary upload tree
====

This is a python script to upload a folder and its subfolders to Cloudinary CDN.

Setup
===

Install requirements:

    pip install -r requirements.txt
   
   
Usage
==

```commandline

usage: upload_tree [-h] --cloud_name CLOUD_NAME --api_key API_KEY --api_secret
                   API_SECRET [--destination-folder DESTINATION_FOLDER]
                   [--exclude-files EXCLUDE_FILES]
                   base_folder

Upload a tree folder to Cloudinary

positional arguments:
  base_folder           Base folder to upload

optional arguments:
  -h, --help            show this help message and exit
  --cloud_name CLOUD_NAME, -c CLOUD_NAME
                        Cloudinary cloud name (default: None)
  --api_key API_KEY, -a API_KEY
                        Cloudinary API key (default: None)
  --api_secret API_SECRET, -s API_SECRET
                        Cloudinary API secret (default: None)
  --destination-folder DESTINATION_FOLDER, -d DESTINATION_FOLDER
                        Destination base folder (default: None)
  --exclude-files EXCLUDE_FILES, -x EXCLUDE_FILES
                        Exclude files (default: [])

```