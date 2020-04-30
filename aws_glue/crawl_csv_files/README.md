# Define CSV crawling

> *Last updated: 2020/04/23*

> With Pycharm, mark `crawl_csv_files` as **Sources Root**

## I. Required installations
If not already done, follow [requirements](../../requirements.md) guide

## II. Push CSV files to S3 bucket
If not already done, follow [push csv files](../../aws_s3/push_csv_files/README.md) guide

## III. Create authorization (IAM)
1. Create **IAM Role** named `AWSGlueServiceRoleDefault`
2. Add existing policies `AWSGlueServiceRole` and `AmazonS3FullAccess` to this role

## IV. Crawl by script

### 1. Edit configurations
Edit following properties in [resources/conf.yml](resources/conf.yml)
   - database:
   - crawler-name:
   - folder-path:

### 2. Add policy to user group
1. Go to AWS Console, IAM service
2. Create a new **Policy** named `AWSGluePassRolePolicy` containing this code:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "iam:PassRole",
      "Resource": "arn:aws:iam::<ACCOUNT ARN>:role/AWSGlueServiceRoleDefault"
    }
  ]
}
```
> You can get the **Account ARN** going to `AWS Console > My Account > Account id`

3. Go to previously created `Developers` group and add the new policy to it

### 3. Launch unit tests (optional)
```sh
python -m unittest discover lib_crawling\aws_client
python -m unittest discover lib_crawling\conf_utils
```

### 4. Launch program
```sh
python crawl_csv_files.py
```

### 5. Check crawler
1. Go to AWS console, to **Glue** service
2. Click `Crawlers` to check the crawling process

## IV-bis. Crawl manually
1. In AWS console, go to **Glue** service
2. Create **Database** named `pokemons`
3. Create **Table** from **Crawler**  
    - Create crawler `pokemon-csv-crawler`
    - Select `s3://aws-glue-pokemon-csv` as datasource
    - Choose existing IAM Role `AWSGlueServiceRoleDefault`
    - Choose frequency *"Run on demand"*
    - Choose `pokemons` as database
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
    - Run the crawler

## V. Access logs
You can access log in `AWS Console > AWS Glue > Crawlers > Logs` or directly in **Cloudwatch**

```
...
12:16:54    [ebd0cfd9-a115-4f4e-b015-29339326c14e] BENCHMARK : Running Start Crawl for Crawler pokemon-csv-crawler
12:17:23    [ebd0cfd9-a115-4f4e-b015-29339326c14e] BENCHMARK : Classification complete, writing results to database pokemons
12:17:23    [ebd0cfd9-a115-4f4e-b015-29339326c14e] INFO : Crawler configured with SchemaChangePolicy {"UpdateBehavior":"UPDATE_IN_DATABASE","DeleteBehavior":"DEPRECATE_IN_DATABASE"}.
12:17:46    [ebd0cfd9-a115-4f4e-b015-29339326c14e] INFO : Created table pokemon_v1 in database pokemons
12:17:48    [ebd0cfd9-a115-4f4e-b015-29339326c14e] INFO : Created table pokemons_v2 in database pokemons
12:17:51    [ebd0cfd9-a115-4f4e-b015-29339326c14e] BENCHMARK : Finished writing to Catalog
...
```

## VI. Access created tables
1. Go to AWS console, to **Glue** service
2. Click `Tables` to inspect the 2 created tables
    - Database: pokemons
    - Classification: csv
    - Location: s3://aws-glue-pokemon-csv/
    - objectCount: 2 (number of files processed)
    - delimiter: ,

## VII. Request created data
You can request the data created by crawling with **Athena** service

1. If not already done, create bucket `aws-glue-pokemon-csv` with the folder `query_result_csv`
2. Go to AWS console, Athena service, and request the `pokemons_v1` table
    - On the **Query Editor** tab, choose the database `pokemons`
    - Choose `s3://aws-glue-pokemon-csv/query_result_csv/` as **Query result location**
    - Launch following requests:
        - `SELECT COUNT(*) FROM "pokemons"."pokemons_v1";`
        - `SELECT * FROM "pokemons"."pokemons_v1";`