# Push files to AWS S3

> With Pycharm, mark `push_files` as **Sources Root**

## I. Required installations
If not already done, follow [requirements](../../requirements.md) guide

## II. Edit configurations
Edit following properties in [resources/conf.yml](resources/conf.yml)
   - default-region:
   - bucket-name:
   - profile:

## III. Copy files to upload
Copy files you want to push to S3 in [resources/files](resources/files) folder

## IV. Launch unit tests
```sh
python -m unittest discover lib\aws_client
python -m unittest discover lib\conf_utils
python -m unittest discover lib\file_utils
```

## V. Launch program
```sh
python push_files_to_s3_bucket.py
```