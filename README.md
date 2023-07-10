# AssetMappr-BE

## Deploy using GitHub Actions
### Steps
**Development**

1. Launch a t2.micro instance. (Create new of use existing key - .pem file)
2. Grant HTTP inbound access permission to 0.0.0.0/0 
3. ssh to instance
```bash
ssh -o StrictHostKeyChecking=no -i <private_key> <user>@<ip>
```
4. Install docker
```bash
curl -fsSL https://get.docker.com -o get-docker.sh && sudo sh get-docker.sh
# Provide permissions to docker command
sudo usermod -aG docker $(whoami)
```
5. Add/Update variables and secrets (Current Repo -> Settings -> Security -> Secrets and Variables -> Actions)

> Variables
> - APP_NAME=AssetMappr-BE
> 
> Secrets
> 
> - AWS_EC2_HOST=<instance_ip>
> - AWS_EC2_USER=<instance_user>
> - AWS_PRIVATE_KEY=<private_key>
> - SECRET_KEY=<app_secret_key>
> - DB_NAME=<postgreSQL_db_name> 
> - DB_USER=<db_user> 
> - DB_PWD=<db_pwd> 
> - DB_HOST=<db_host>
> - DB_PORT=<db_port>

6. Branch out a release branch from main branch with pattern 'release/dev/*'