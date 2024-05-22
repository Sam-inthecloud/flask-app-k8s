# DevOps Project: Deploying a Flask Application on AWS EKS

## Overview
This project demonstrates the deployment of a Flask application on Amazon Elastic Kubernetes Service (EKS) using Docker containers. The application is containerized using Docker, deployed on Kubernetes, and hosted on AWS EKS. This README provides an overview of the project, including the technologies used, the deployment process, troubleshooting steps, and instructions for reproducing the setup.

[Blog Page](https://medium.com/@saminthecloud1/devops-deploying-and-troubleshooting-a-flask-application-on-aws-eks-fe962b963cb6)
## Architecture
![Architecture](https://github.com/Sam-inthecloud/flask-app-k8s/blob/main/flask-app.png)
## Technologies Used
- Amazon EKS (Elastic Kubernetes Service)
- Docker
- Flask (Python Web Framework)
- Terraform (Infrastructure as Code)
- AWS CLI (Command Line Interface)

## Deployment Process
1. **Clone the repository**:
   - git clone https://github.com/Sam-inthecloud/flask-app-k8s.git

2. **Building Docker Image**: 
   - Dockerfile in the `flask-app` directory is used to build the Docker image.
   - Use `docker build -t flask-app .` to build the Docker image locally.

3. **Pushing Docker Image to ECR (Elastic Container Registry)**:
   - Tag the Docker image with your ECR repository URI.
   - Use `docker tag flask-app:latest <ECR_URI>:latest` to tag the image.
   - Push the image to ECR using `docker push <ECR_URI>:latest`.

4. **Provisioning Infrastructure with Terraform**:
   - Navigate to the `terraform` directory.
   - Run `terraform init` to initialize the Terraform configuration.
   - Run `terraform plan` to preview the changes.
   - Run `terraform apply` to provision the infrastructure on AWS.

5. **Deploying Flask Application on EKS**:
   - Apply the Kubernetes deployment and service configurations using `kubectl apply -f deployment.yaml -f service.yaml`.

6. **Accessing the Application**:
   - Once the application is deployed, access it using the external IP or DNS provided by the LoadBalancer service in AWS.

## Troubleshooting
- Common issues include connectivity problems, configuration errors, or resource constraints.
- Please read the blog for any Troubleshooting tips

## Contributing
Contributions are welcome! If you have any suggestions, improvements, or feature requests, feel free to open an issue or create a pull request.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

