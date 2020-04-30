# Combine CVS files

> *Last updated: 2020/04/27*

> With Pycharm, mark `combine_csv_files` as **Sources Root**

## I. Required installations
If not already done, follow [requirements](../requirements.md) guide

## II. Crawl CSV files
If not already done, follow [crawl csv files](../crawl_csv_files/README.md) guide

## III. Combine data by script

### 1. Verify script
Verify `resources\scripts\pokemon-v1-v2-combination.py` script

### 2. Launch unit tests (optional)
```sh
python -m unittest discover lib_combination\aws_client
python -m unittest discover lib_combination\conf_utils
python -m unittest discover lib_combination\conf_utils
```

### 3. Launch program
```sh
python combine_csv_files.py
```

### 4. Check job
1. Go to AWS console, to **Glue** service
2. Click `Jobs` to check the job running process

## III-bis. Combine data manually
1. Add `resources\scripts\pokemon-v1-v2-combination.py` script to `s3://aws-glue-pokemon-csv/combination/scripts` folder
2. Add folder `csv_file_result_job` in `aws-glue-pokemon-csv` bucket
3. Go to Glue in order to combine data from pokemon v1 format and v2 format 
    - Create a **Job** named `pokemon-v1-v2-combination`
    - Choose existing IAM Role `AWSGlueServiceRoleDefault`
    - Choose `Spark 2.4` and `Python 3`
    - Choose `Spark` and `Python`
    - Choose *An existing script that you provide*
    - Choose `s3://aws-glue-pokemon-csv/combination/scripts/pokemon-v1-v2-combination.py` to store the script
    - Choose `s3://aws-glue-pokemon-csv/combination/tmp` to store temporary files
    - In "Security configuration, script libraries, and job parameters", add following parameters:
        - `--base`: `pokemons`
        - `--result_bucket_path`: `s3://aws-glue-pokemon-csv/combination/csv_file_result_job`
        - `--table_v1`: `pokemons_v1`
        - `--table_v2`: `pokemons_v2`
4. Verify the job and launch it. This may be waiting around 10 minutes

## IV. Access logs & errors
You can access log in `AWS Console > AWS Glue > Crawlers > Logs/Error logs` or directly in **Cloudwatch**

```
...
16:26:56    Detected region eu-west-1
16:26:56    Detected glue endpoint https://glue.eu-west-1.amazonaws.com
16:26:57    YARN_RM_DNS=ip-172-32-87-78.eu-west-1.compute.internal
16:26:57    JOB_NAME = pokemon-v1-v2-combination
16:26:57    PYSPARK_VERSION 3 python3
16:26:57    Specifying eu-west-1 while copying script.
16:27:02    Completed 1.4 KiB/1.4 KiB (41.0 KiB/s) with 1 file(s) remaining
16:27:02    download: s3://aws-glue-pokemon-csv/combination/scripts/pokemon-v1-v2-combination.py to ./script_2020-04-23-16-26-57.py
...
```

## V. Check resulting file
You can access your resulting file in `aws-glue-pokemon-csv` bucket in `csv_file_result_job` folder