# Combine CVS files

> *Last updated: 2020/05/08*

> /!\ This part need to create AWS Glue endpoint. Using a endpoint like that can lead to important costs
> /!\ See: https://blog.jayway.com/2018/07/03/aws-glue-dev-endpoint-deleter/

> With Pycharm, mark `combine_csv_files_with_endpoint` as **Sources Root**

## I. Required installations
If not already done, follow [requirements](../../requirements.md) guide

## II. Crawl CSV files
If not already done, follow [crawl csv files](../crawl_csv_files/README.md) guide

## III. Create authorization (IAM)
1. Create **IAM Role** named `AWSGlueServiceRoleDefault`
2. Add existing policies `AWSGlueServiceRole` and `AmazonS3FullAccess` to this role

## IV. Combine data by script

### Locally (optional)
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
cd  /home/glue/scripts/aws_glue/combine_csv_files
python combine_csv_files.py
```
