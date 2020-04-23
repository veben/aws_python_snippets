# CVS files combination

> *Last updated: 2020/04/22*

> With Pycharm, mark `csv_files_combination` as **Sources Root**

## I. Required installations
If not already done, follow [requirements](../../requirements.md) guide

## II. Create authorization (IAM)
1. Create **IAM Role** named `AWSGlueServiceRoleDefault`
2. Add existing policies `AWSGlueServiceRole` and `AmazonS3FullAccess` to this role

## III. Create buckets and add test files (S3)

### Create buckets
1. Create bucket `aws-glue-pokemon-csv`
2. Create bucket `aws-glue-pokemon-tmp` with the folders `query_result_csv` and `file_result_csv`

### Add test files
#### Manually:
1. Create folder `pokemons_v1` and put `pokemons_v1.csv` and `pokemons_v1_2.csv` files inside
2. Create folder `pokemons_v2` and put `pokemons_v2` file inside

#### With aws_s3 > push_files
1. Edit file `../../aws_s3/push_files/resources/conf.yml`, adding `aws-glue-pokemon-csv` as **bucket-name**
2. Launch program with commands:
```sh
cd ../../aws_s3/push_files
python push_files_to_s3_bucket.py
```

## IV. Define crawling (Glue)

### Manually
1. Create **Database** named `pokemons`
2. Create **Table** from **Crawler**  
    - Create crawler `pokemon-csv-crawler`
    - Select `s3://aws-glue-pokemon-csv` as datasource
    - Choose existing IAM Role `AWSGlueServiceRoleDefault`
    - Choose frequency *"Run on demand"*
    - Choose `pokemons` as database
    - Run the crawler
    - Other configuration:
        1. Exclude patterns: **No**
        2. Grouping behavior for S3 data (optional)
            By default, when a crawler defines tables for data stored in S3, it considers both data compatibility and schema similarity. Select this check box to group compatible schemas into a single table definition across all S3 objects under the provided include path. Other criteria will still be considered to determine proper grouping
            => **No**
        3. Prefix add to table (table created by Glue): **No**
        4. When the crawler detects schema changes in the data store, how should AWS Glue handle table updates in the data catalog?
            - Update the table definition in the data catalog: **Yes**
            - Add new columns only: **No**
            - Ignore the change and don't update the table in the data catalog: **No**
        5. How should AWS Glue handle deleted objects in the data store?
            - Delete tables and partitions from the data catalog: **No**
            - Ignore the change and don't update the table in the data catalog: **No**
            - Mark the table as deprecated in the data catalog: **Yes**
3. You can take a look at logs in **CloudWatch** following the associated link

```
...
12:16:54    [ebd0cfd9-a115-4f4e-b015-29339326c14e] BENCHMARK : Running Start Crawl for Crawler pokemon-csv-crawler
12:17:23    [ebd0cfd9-a115-4f4e-b015-29339326c14e] BENCHMARK : Classification complete, writing results to database pokemons
12:17:23    [ebd0cfd9-a115-4f4e-b015-29339326c14e] INFO : Crawler configured with SchemaChangePolicy {"UpdateBehavior":"UPDATE_IN_DATABASE","DeleteBehavior":"DEPRECATE_IN_DATABASE"}.
12:17:46    [ebd0cfd9-a115-4f4e-b015-29339326c14e] INFO : Created table aws_glue_pokemon_csv in database pokemons
12:17:51    [ebd0cfd9-a115-4f4e-b015-29339326c14e] BENCHMARK : Finished writing to Catalog
...
```

4. Inspect the tables created from crawl named `aws_glue_pokemon_csv`
    - Database: pokemons
    - Classification: csv
    - Location: s3://aws-glue-pokemon-csv/
    - objectCount: 2 (number of files processed)
    - delimiter: ,

### With script
TODO

## V. Request table (Athena)
1. Request the `pokemons_v1` table
    - On the **Query Editor** tab, choose the database `pokemons`
    - Choose `s3://aws-glue-pokemon-tmp/query_result_csv/` as **Query result location**
    - Launch following requests:
        - `SELECT COUNT(*) FROM "pokemons"."pokemons_v1";`
        - `SELECT * FROM "pokemons"."pokemons_v1";`

## VI. Transform data (Glue)

### Locally (with script in Pycharm)
> Follow official guide: [link](https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-python-samples-legislators.html)
1. Generate ssh keys (public key: `pokemons_dev_endpoint.pub`; private key: `pokemons_dev_endpoint`) with this command:
        ```sh
        ssh-keygen -t rsa -f C:\Users\<User>/.ssh/pokemons_dev_endpoint -C "<email>"
        ```
2. Create Development endpoint for S3 data ([official guide](https://docs.aws.amazon.com/glue/latest/dg/dev-endpoint-tutorial-prerequisites.html))
    - named `pokemons_dev_endpoint`
    - Choose existing IAM Role `AWSGlueServiceRoleDefault`
    - Upload public ssh key
    - Skip all other step and click Finish (*the provisioning phase took minutes*)
3. Configure **Pycharm (professional only)** to access to the development endpoint ([official guide](https://docs.aws.amazon.com/glue/latest/dg/dev-endpoint-tutorial-pycharm.html))
    - Download `PyGlue` lib from here: [link](https://s3.amazonaws.com/aws-glue-jes-prod-us-east-1-assets/etl-1.0/python/PyGlue.zip)
    - Put it on following folder: `C:\Env\tools\python\python3.7.7\Lib`
    - Connection:
        - Type: SFTP
        - Host: *<public adress of pokemons_dev_endpoint>*
        - User name: glue
        - Authentication: Key pair
        - Private key: `C:\Users\<User>\.ssh\pokemons_dev_endpoint`
        - Passphrase: *the passphrase asked during key pair generation*
    - Mappings:
        - Local Path: `C:\Env\dev\perso\aws_python_snippets`
        - Deployment Path: `/home/glue/scripts/`
    - Excluded Paths: `C:\Env\dev\perso\aws_python_snippets\venv`
    - Upload script to endpoint: Right click on `aws_python_snippets` and `Deployment > Upload to pokemons_dev_endpoint`
    - Check `Tools > Deployment > Automatic Upload (always)`
    - Define **remote** Python interpreter
        - SSH Interpreter
        - ...
        - Interpreter: `/usr/bin/gluepython3`
4. Edit configurations
Edit following properties in [resources/conf.yml](resources/conf.yml)
   - result-folder-path: *bucket/folder where you want the file resulting from the combination*
   - columns: *columns you want to keep*

5. Launch program with following commands:
```sh
ssh -i C:\Users\<User>\.ssh\pokemons_dev_endpoint glue@<public adress of pokemons_dev_endpoint>
cd  /home/glue/scripts/aws_glue/csv_files_combination
python csv_files_combination.py
```

### With AWS Glue job
1. Add `resources\scripts\pokemon-v1-v2-combination.py` script to `s3://aws-glue-pokemon-tmp/combination/scripts` folder
2. Add folder `csv_file_result_job` in `aws-glue-pokemon-tmp` bucket
3. Go to Glue in order to combine data from pokemon v1 format and v2 format 
    - Create a **Job** named `pokemon-v1-v2-combination`
    - Choose existing IAM Role `AWSGlueServiceRoleDefault`
    - Choose `Spark 2.4` and `Python 3`
    - Choose `Spark` and `Python`
    - Choose *An existing script that you provide*
    - Choose `s3://aws-glue-pokemon-tmp/combination/scripts/pokemon-v1-v2-combination.py` to store the script
    - Choose `s3://aws-glue-pokemon-tmp/combination/tmp` to store tempory files
4. Verify the job and launch the job. This may be waiting around 10 minutes
    

## VI. Transform to parket format and request (Glue & Athena)
1. Create bucket **aws-glue-pokemon-parket**
2. Add folder `query_result_parket` in `aws-glue-pokemon-tmp` bucket
3. Go to Glue in order to transform the data from `CSV` to `Parquet` format  
    - Create a **Job** named `pokemon-csv-to-parket-job`
    - Choose existing IAM Role `AWSGlueServiceRoleDefault`
    - Choose `Spark` and `Python`
    - Choose *A proposed script generated by AWS Glue*
    - Choose `s3://aws-glue-pokemon-tmp/parket/scripts` to store the script
    - Choose `s3://aws-glue-pokemon-tmp/parket/tmp` to store tempory files
    - Select table `aws_glue_pokemon_csv` as datasource
    - Choose *Create table in your data target* with properties:
        * Datastore: S3
        * Format: Parket
        * Target path: `s3://aws-glue-pokemon-parket` }
4. Verify the script and launch the job. This may be waiting around 10 minutes
5. Create another table from crawler  
    - Create crawler `pokemon-parket-crawler`
    - Select `s3://aws-glue-pokemon-parket` as datasource
    - Choose existing IAM Role `AWSGlueServiceRoleDefault`
    - Choose frequency *"Run on demand"*
    - Choose `pokemons` as database
    - Run the crawler
6. Inspect the table created from crawl named `aws_glue_pokemon_parket`
7. Create the bucket `aws-glue-pokemon-tmp` with the folder `query_result_parket`
8. Do the same with `aws_glue_pokemon_parket` table
    - On the **Query Editor** tab, choose the database `pokemons`
    - Choose `s3://aws-glue-pokemon-parket-query-result/query_result/` as **Query result location**
    - Launch following request: `SELECT * FROM "pokemons"."aws_glue_pokemon_parket" limit 10;`