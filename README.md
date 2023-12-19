# MLOps-Pipeline-Deployment-and-serving-AWS

This repository hosts an end-to-end MLOps solution designed for efficient model retraining, real-time metric notifications, and effortless deployment of ML models to serverless Amazon Sagemaker endpoints. Additionally, it includes a web application for visualizing model training metrics and conducting model inference.

## Project Overview

This project focuses on a subset of the larger Machine Learning Operations (MLOps) Pipeline, streamlining the model training and deployment process. It aims to enhance model quality, accelerate development, identify model and dataset drift, ensure governance, and continuously monitor ML models.

### Key Features

* **Model Retraining**: Push based/Automatic retraining of ML models with latest training dataset.
* **Real-time Metrics**: Notifications via email for latest staged trained model's metric.
* **Sagemaker Deployment**: Seamless deployment of models to serverless Sagemaker endpoints.
* **Model Visualization**: Web-based interface for visualizing historical model training metrics.
* **Model Inference**: Conducting model predictions through an intuitive web application.

### Implementation Scope

Compared to a production MLOps pipeline, this project implements stages like Model Training, Deployment, Serving, and Monitoring on AWS. It leverages a custom script to train an Image Classification model for waste segregation.

### Use Case

The model classifies images as Organic or Recyclable, aiding organizations handling waste segregation. It speeds up manual sorting processes, reducing errors and optimizing workforce utilization.

### Target Audience

Primarily for ML Engineers and Data Scientists, reducing model deployment and retraining time, allowing teams to focus on enhancing datasets and experimenting with ML techniques. A future scope includes deploying the frontend for public use.

## Performance Targets

1. **Deployment Downtime:** Achieving zero downtime when updating models on SageMaker endpoints.
2. **Model Inference Time:** Ensuring low latency (maximum 400 microseconds for a 5MB model).
3. **Monitoring and Maintenance:** Storing model metrics in DynamoDB for analysis and decision-making.
4. **Scalability:** Using serverless components to handle potential load surges without performance issues.

## Implementation on AWS

### Services Used and Significance

- **Compute:** AWS Lambda for serverless tasks, EC2 for hosting the frontend.
- **Storage:** Amazon S3 for model artifacts, training datasets, model-metric json files, and user-uploaded images.
- **Database:** DynamoDB for storing model metrics and job statuses.
- **Networking:** API Gateway for Lambda function communication, EventBridge for triggering actions based on job statuses.
- **Notification:** AWS SNS for email notifications on model training and deployment.


### Deployment Model Overview

The project is hosted on AWS, leveraging various managed services for scalability, security, and cost-effectiveness. It utilizes a combination of serverless compute (FaaS) and infrastructure (IaaS) to optimize costs and flexibility.

### AWS Architecture 

![AWS-Architecture](/image-assets/aws-architecture-diagram.png)

The architecture diagram illustrates the communication between frontend, Lambda functions, S3, DynamoDB, and SageMaker. Data storage, Lambda executions, API Gateway, and EventBridge facilitate the project's functionalities.

### Security Measures

The system ensures encryption at rest using SSE-S3 and KMS for S3 and DynamoDB, respectively. In-transit data is encrypted using SSL/TLS for fuliling API requests, and also security is maintained using HTTPS, IAM-roles and policies, and CloudWatch for monitoring.

## Service Selection Rationale

In crafting this MLOps pipeline, several AWS services were considered for various tasks. The final choices were made based on several factors, including scalability, cost-effectiveness, ease of integration, and the specific needs of the project.

### Compute Services

**AWS Lambda:** Chosen for its serverless nature, enabling stateless execution of tasks like model training, endpoint deployment, and triggering notifications. Its event-driven architecture aligns well with the project's requirements, ensuring optimal resource utilization and cost efficiency.

*Alternative Considerations:* While AWS Fargate and ECS could offer more environment control and flexibility for certain tasks, Lambda's lightweight nature, ease of deployment, and pay-as-you-go pricing model make it the preferred choice for this project's lightweight computations.

**Elastic Compute Cloud (EC2):** Utilized for hosting the frontend application due to its versatility and control over the hosting environment. Although AWS Elastic Beanstalk and Amplify offer scalable and managed options, EC2 was chosen for its simplicity, adequate performance, and cost-effectiveness for the current workload.

### Storage Services

**Amazon S3:** Selected for its virtually unlimited scalability, cost efficiency, and seamless integration with SageMaker. S3's durability and accessibility suit the storage needs for model artifacts, training datasets, and user-uploaded images.

*Alternative Considerations:* While other storage solutions like EC2 with Elastic Block Storage (EBS) or Elastic File System (EFS) exist, their configuration complexity and limited scalability compared to S3 made them less suitable for this project's requirements.

### Database Services

**AWS DynamoDB:** Chosen for its serverless, NoSQL architecture, offering low latency, flexible schema, and scalability. DynamoDB's ability to store extensive model metrics in a durable and cost-effective manner aligns well with the project's monitoring and retrieval needs.

*Alternative Considerations:* While Amazon RDS or Aurora Serverless provide more structured schemas, DynamoDB's flexibility and serverless nature, along with its cost-efficient billing based on data request usage, made it the optimal choice.

### Networking and Notification Services

**AWS API Gateway:** Utilized for managing communication between frontend and Lambda functions, providing a secure single-entry point for API requests. Its features like automatic payload conversion and monitoring capabilities streamline API management.

**Amazon EventBridge and AWS SNS:** Chosen for event-driven notifications, seamlessly triggering actions based on job statuses. SNS's flexibility in notification types and EventBridge's rich event management capabilities suited the project's needs.

*Alternative Considerations:* Though alternatives like AWS Fargate or ECS could handle specific tasks, the simplicity and efficient event-driven nature of Lambda and the integrations with API Gateway and other services made them the preferred choices.

These selections were made considering the project's specific requirements, ensuring an optimal balance between performance, scalability, cost, and ease of implementation.


## Delivery Model Overview

A combination of FaaS (Lambda) and IaaS (EC2) is used to balance costs and flexibility. Lambda handles the ML pipeline tasks, while EC2 hosts the frontend for developers' access.

### Future Scope

- **Automated Model Retraining:** AWS Step Functions for scheduled retraining.
- **Rollback Functionality:** Implementing the ability to revert to previous models.
- **User Interface Enhancements:** Using Cognito for user authentication and integrating edge devices for model inference.

## Project Cost Estimation

| Service           | Usage                                             | Cost  |
| ----------------- | ------------------------------------------------- | ----- |
| Amazon S3 (Standard Tier) | 1 GB storage, 50 PUT requests, 10 GET requests... | $0.03 |
| Amazon EC2        | 1 t2.micro instance, 8 hours uptime, 30 GB EBS... | $12.96|
| Amazon SageMaker  | 1 ml.m5.large instance, 10 training jobs, 30 mi... | $14.50|
| Amazon ECR        | 1 9 GB image stored                               | $0.90 |
| Amazon DynamoDB   | 1 provisioned RCU and WCU, 230 KB item size, Provisioned 'standard' table class | $0.59 |
| Amazon CloudWatch | 10 lambda functions, 20 requests per function, 1GB Log Data ingetsed | $1 |
| Data Transfer OUT | 1 Gb of outbound traffic | $0.09 |
| Safety buffer amount | | $10 |
| Minimum **Monthly** Cost Estimate |                               | **$40.07** |

* *While this estimation provides a calculated overview, some values within it might represent higher usage than anticipated, possibly affecting the accuracy of the total cost.*
These costs are estimated using the AWS Pricing calculator [“AWS Pricing Calculator,” Calculator.aws. [Online] Available: https://calculator.aws/#/]

## Project Execution Screenshot

![Model Evaluation Dashboard](/image-assets/model-evaluation-dashboard.png)

_Figure : Dashboard for visualising the model metrics stored in DynamoDB_

![Subscribe SNS Topic](/image-assets/subscribe-sns-topic.png)

_Figure : Subscribe email ID to SNS Topic_

![Subscription Email Notification](/image-assets/subscription-email-notification.png)

_Figure : Subscription email notification_

![Error when no model endpoitn is deployed to Amazon SageMaker](/image-assets/error-when-no-model-endpoint-deployed.png)

_Figure : Error prompt when performing prediction when no model endpoint deployed for inference_

![Initiate Model Training](/image-assets/initiate-model-training.png)

_Figure : Starting training job of the model on the training dataset_

![In-Progress Model Training status](/image-assets/model-training-in-progress.png)

_Figure : Status indicating model training in progress_

![Email Notification after training is successfull](/image-assets/email-notification-after-training-suceeded.png)

_Figure : Email notification showing model comparison between latest trained model and the current deployed model_

![Accept/Reject model after model training](/image-assets/options-after-model-training.png)

_Figure : Accept and Reject model with latest staged model metric on frontend_

![Email Notification after model deployment is successfull](/image-assets/email-notification-successful-model-deployment.png)

_Figure : email received about model endpoint status "inService" after successful deployment_


![Inference result - organic class](/image-assets/inference-result-organic.png)

_Figure : Inference result for an Organic image_


![Inference result - recyclable class](/image-assets/inference-result-recyclable.png)

_Figure : Image inference result for a recyclable image_


![Visualisation after model accepted and deployed to Amazon Sagemaker endpoint](/image-assets/visualisation-after-model-accepted-and-deployed.png)

_Figure : Visualisation dashboard after model is accepted_




<hr>

---