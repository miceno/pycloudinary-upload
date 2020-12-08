Cloudinary upload tree
====

This is a python script to upload a folder and its subfolders to Cloudinary CDN.

Transformation quota
===

Every image or video upload counts on your Transformation quota, since Cloudinary
analyses the image and prepares it for the CDN.

Use `raw` resource_type so image uploads will not count on your Transformation quota. 
See https://cloudinary.com/blog/understanding_cloudinary_s_transformation_quotas 

Setup
===

Install requirements:

    pip install -r requirements.txt
   
   
Usage
==

```commandline

usage: pycloud-upload [-h] 
    --cloud_name CLOUD_NAME 
    --api_key API_KEY 
    --api_secret API_SECRET
    [--destination-folder DESTINATION_FOLDER] 
    [--unique-filename] [--no-unique-filename] 
    [--use-filename] [--no-use-filename] 
    [--exclude-files EXCLUDE_FILES] 
    [--tag TAGS] 
    [--resource-type {image,raw,video,auto}]
    [--concurrent_workers CONCURRENT_WORKERS]
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
  --unique-filename     When set to true, add random characters at the end of the filename that guarantee its uniqueness. This
                        parameter is relevant only if use_filename is also set to true. (default: False)
  --no-unique-filename  When set to false, does not add random characters at the end of the filename that guarantee its uniqueness.
                        This parameter is relevant only if use_filename is also set to true. (default: False)
  --use-filename        When true, the uploaded file's original filename becomes the Public ID. Random characters are appended to the
                        filename value to ensure Public ID uniqueness if unique_filename is true. (default: True)
  --no-use-filename     When false, the Public ID will be comprised of random characters. (default: True)
  --exclude-files EXCLUDE_FILES, -x EXCLUDE_FILES
                        Exclude files (default: [])
  --tag TAGS, -t TAGS   Set tags on uploaded files (default: [])
  --resource-type {image,raw,video,auto}, -r {image,raw,video,auto}
                        Set resource type. raw means no transformation on upload (default: auto)
  --concurrent_workers CONCURRENT_WORKERS, -w CONCURRENT_WORKERS
                        Specify number of concurrent network threads. (default: 10)


```


Example:
```commandline

python pycloud-upload.py
        -r raw                
        -c ahpn 
        -a API_KEY 
        -s SECRET
        --destination-folder CLOUDINARY_DESTINATION_FOLDER 
        SOURCE_FOLDER

python pycloud-upload.py
    -c ahpn -a API_KEY -s SECRET_KEY
    -r raw 
    --destination-folder tiles/poblenou-1871/20/530565 
    ~/Downloads/1871/1871/20/530565

```

# Cloudinary CLI

Have a look at it https://cloudinary.com/documentation/cloudinary_cli

## Upload directory

It does not allow to set `raw` resource_type so every upload will count for your
Transformation quota.

```commandline

cld -C ahpn upload_dir -f "tiles/poblenou-1871" ~/Downloads/1871/1871/20/530564

```
