docker build -t sagemaker-images-cf  .

docker tag sagemaker-images-cf:latest <ACCOUNT_ID>.dkr.ecr.<REGION_NAME>.amazonaws.com/sagemaker-images-cf:latest

aws ecr get-login-password --region <REGION_NAME> | docker login --username AWS --password-stdin <ACCOUNT_ID>.dkr.ecr.<REGION_NAME>.amazonaws.com/sagemaker-images-cf

docker push <ACCOUNT_ID>.dkr.ecr.<REGION_NAME>.amazonaws.com/sagemaker-images-cf:latest
