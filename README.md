# AssetMappr-BE


## Deploy using GitHub Actions
### Steps
**Development**

1. Launch a t2.micro instance. (Create new of use existing key - .pem file)
2. Grant HTTP inbound access permission to 0.0.0.0/0 
3. Connect RDS to EC2 using SGs.
4. Add/Update variables and secrets (Current Repo -> Settings -> Security -> Secrets and Variables -> Actions)

> Variables
> - APP_NAME=AssetMappr-BE
> - DB_NAME=<postgreSQL_db_name> 
> - DB_HOST=<db_host>
> - DB_PORT=<db_port>
> - DEBUG=<application_debug_flag>
> 
> Secrets
> 
> - AWS_EC2_HOST=<instance_ip>
> - AWS_EC2_USER=<instance_user>
> - AWS_PRIVATE_KEY=<private_key>
> - SECRET_KEY=<app_secret_key>
> - DB_USER=<db_user> 
> - DB_PWD=<db_pwd> 

6. Branch out a release branch from main branch with pattern 'release/dev/*'

## Linting:
Install autopep8
```bash
pip install autopep8
pip install pylint
```
To lint a file use:
```bash
autopep8 --in-place --aggressive --aggressive <filename>
```
To check linting issues:
```bash
pylint <filename>
```

## DB Initialization
Fetch and Save Asset Information
```bash
python ./db_init/fetch_and_save_assets.py
```
Create and populate database
```bash
python ./db_init/db_utils.py
```
Note: Mind the relative path.
