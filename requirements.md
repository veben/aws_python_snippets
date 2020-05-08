# Requirements

>*Last updated: 2020/04/23*

## I. Create free tier account

[https://portal.aws.amazon.com/gp/aws/developer/registration/index.html?nc2=h_ct&src=header_signup](https://portal.aws.amazon.com/gp/aws/developer/registration/index.html?nc2=h_ct&src=header_signup)

## II. Enable Multi-factor authentication (MFA)

1. Connect to [AWS console](https://aws.amazon.com/fr/console/)
2. Follow the official guide : [https://console.aws.amazon.com/iam/home?#/security_credentials](https://console.aws.amazon.com/iam/home?#/security_credentials)

## III. Create Developer user with programmatic access

> https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html#id_users_create_console

1. Connect to [AWS console](https://aws.amazon.com/fr/console/) with root account
2. Go to **IAM** service
3. Create **Group** named `Developers`
4. Add existing **Policy** `PowerUserAccess` to the group
5. Create **User** named `dev`
6. Check **Programmatic access**
7. Check **AWS Management Console access** (optional)
8. Add it to the administrator group 
9. Copy **Access keys** (access key ID and secret access key)
10. Put them in `C:\Users\<User>\.aws/credentials` file, like that:

	```
	[p-dev]
	aws_access_key_id = dev_ACCESS_KEY
	aws_secret_access_key = dev_ACCESS_KEY
	region = eu-west-1
	```

## IV. Install **Python**

## V. Install **AWS CLI**
[https://docs.aws.amazon.com/cli/latest/userguide/install-windows.html](https://docs.aws.amazon.com/cli/latest/userguide/install-windows.html)

> With python

1. Install awscli with command:
	```sh
	pip3 install awscli
	```

2. Upgrade to last version:
	```sh
	pip3 install --user --upgrade awscli
	```

3. Known your **awscli** version:
	```sh
	aws --version
	```

## VI. Configure AWS CLI

1. If not done, create/edit `C:\Users\<User>\.aws\credentials` file, and add default credentials configuration
	```
	[default]
	aws_access_key_id = YOUR_ACCESS_KEY
	aws_secret_access_key = YOUR_SECRET_KEY
	```

2. If not done, create/edit `C:\Users\<User>\.aws\config` file, and add default region
	```
	[default]
	region=us-west-1
	```

## VII. Install **aws-mfa**

1. Install aws-mfa with command:
	```sh
	pip3 install aws-mfa
	```

2. Upgrade to last version:
	```sh
	pip3 install --user --upgrade aws-mfa
	```

3. Known your aws-mfa version:
	```sh
	pip3 show aws-mfa
	```

## VIII. Install **boto3** (the AWS SDK for python):

1. Install aws-mfa with command:
	```sh
	pip3 install boto3
	```

2. Upgrade to last version:
	```sh
	pip3 install --user --upgrade boto3
	```

3. Known your boto3 version:
	```sh
	pip3 show boto3
	```

**boto3 credentials priority**: [link](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html)


## IX. Install **moto** (the AWS mocking tool):

1. Install aws-mfa with command:
	```sh
	pip install boto3 moto
	```

2. Upgrade to last version:
	```sh
	pip3 install --user --upgrade moto
	```

3. Known your moto version:
	```sh
	pip3 show moto
	```

## X. Create Administrator user with programatic access (optional, if you need to deat with IAM or other things)

1. Connect to [AWS console](https://aws.amazon.com/fr/console/)
2. Go to **IAM** service
3. Create **Group** named `Administrators`
4. Add existing **Policy** `AdministratorAccess` to the group
5. Create **User** named `admin`
6. Check **Programmatic access**
7. Check **AWS Management Console access** (optional)
8. Add it to the administrator group 
9. Copy **Access keys** (access key ID and secret access key)
10. Put them in `C:\Users\<User>\.aws/credentials` file, like that:

	```
	[p-admin]
	aws_access_key_id = admin_ACCESS_KEY
	aws_secret_access_key = admin_ACCESS_KEY
	region = eu-west-1
	```