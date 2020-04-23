# Push files to AWS S3

> With Pycharm, mark `push_csv_files` as **Sources Root**

## I. Required installations
If not already done, follow [requirements](../../requirements.md) guide

## II. Create bucket
1. Go to AWS console, to **S3** service
2. Create bucket `aws-glue-pokemon-csv`

## III. Push by script

### 1. Edit configurations
Edit following properties in [resources/conf.yml](resources/conf.yml)
   - default-region:
   - bucket-name:
   - profile:

### 2. Copy files to upload
Copy files you want to push to S3 in [resources/files](resources/files) folder

### 3. Launch unit tests (optional)
```sh
python -m unittest discover lib_pushing\aws_client
python -m unittest discover lib_pushing\conf_utils
python -m unittest discover lib_pushing\file_utils
```

### 4. Launch program
```sh
python push_csv_files.py
```

### 5. Check bucket
1. Go to AWS console, to **S3** service, in `aws-glue-pokemon-csv`
2. Check folders dans files

## III-bis. Push manually
1. Go to AWS console, to **S3** service, in `aws-glue-pokemon-csv`
2. Create folder `2020-04-23_13:59:42/pokemons_v1` and put `pokemons_v1.csv` and `pokemons_v1_2.csv` files inside
3. Create folder `2020-04-23_13:59:42/pokemons_v2` and put `pokemons_v2.csv` file inside