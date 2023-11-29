# Your Flask App CI/CD

## Summary

This repository provides a step-by-step guide for deploying a Flask API using Jenkins, Docker, Kubernetes (Amazon EKS), and AWS Secrets Manager. The CI/CD pipeline automates the build, test, and deployment processes.

## Table of Contents

1. [Setting Up](#setting-up)
    - [1.1 Create GitHub Repository](#11-create-github-repository)
    - [1.2 Write Flask API Code](#12-write-flask-api-code)
    - [1.3 Set Up AWS Secrets Manager](#13-set-up-aws-secrets-manager)
    - [1.4 Set Up Jenkins](#14-set-up-jenkins)

2. [Configuring Jenkins](#configuring-jenkins)
    - [2.1 Configure Jenkins Credentials](#21-configure-jenkins-credentials)
    - [2.2 Write Jenkinsfile](#22-write-jenkinsfile)

3. [Setting Up Amazon EKS](#setting-up-amazon-eks)
    - [3.1 Create Amazon EKS Cluster](#31-create-amazon-eks-cluster)
    - [3.2 Configure `kubectl`](#32-configure-kubectl)

4. [Configuring Kubernetes](#configuring-kubernetes)
    - [4.1 Create Kubernetes Manifests](#41-create-kubernetes-manifests)

5. [Update Flask Code](#update-flask-code)
    - [5.1 Update Flask Code for Secrets Manager](#51-update-flask-code-for-secrets-manager)

6. [Push Code to GitHub](#push-code-to-github)
    - [6.1 Push Code to GitHub](#61-push-code-to-github)

7. [Running Jenkins Pipeline](#running-jenkins-pipeline)
    - [7.1 Run Jenkins Pipeline](#71-run-jenkins-pipeline)

8. [Verification](#verification)
    - [8.1 Verify Deployment](#81-verify-deployment)

9. [Scaling and Monitoring](#scaling-and-monitoring)
    - [9.1 Scale and Monitor](#91-scale-and-monitor)

## Setting Up

### 1.1 Create GitHub Repository

- Create a new private GitHub repository for your Flask API.

### 1.2 Write Flask API Code

- Use the provided Flask code (`app.py`) or write your Flask API code.

### 1.3 Set Up AWS Secrets Manager

- Go to AWS Secrets Manager in the AWS Management Console.
- Create a new secret for your Flask API's sensitive information (e.g., database credentials).
- Note the ARN of the created secret.

### 1.4 Set Up Jenkins

- Install Jenkins on a server or use a Jenkins instance in the cloud.
- Install necessary Jenkins plugins for Docker, Kubernetes, and AWS.

## Configuring Jenkins

### 2.1 Configure Jenkins Credentials

- Add credentials for GitHub (for checking out code) and DockerHub (for pushing Docker images).
- Add AWS credentials with permissions to access Secrets Manager.

### 2.2 Write Jenkinsfile

- Write a Jenkinsfile customized for your environment.
- Set variables like `DOCKER_IMAGE`, `K8S_CLUSTER_NAME`, `K8S_REGION`, `K8S_NAMESPACE`, `GIT_CREDENTIALS_ID`, and `DOCKERHUB_CREDENTIALS_ID`.

## Setting Up Amazon EKS

### 3.1 Create Amazon EKS Cluster

- Set up an Amazon EKS cluster in your AWS account.
- Note the cluster name and region.

### 3.2 Configure `kubectl`

- Install `kubectl` on your Jenkins instance.
- Configure `kubectl` with the credentials of the Amazon EKS cluster.

## Configuring Kubernetes

### 4.1 Create Kubernetes Manifests

- Write Kubernetes manifests for Deployment, Service, and Ingress. You can use the ones you provided earlier.

## Update Flask Code

### 5.1 Update Flask Code for Secrets Manager

- Modify the Flask code (`app.py`) to retrieve sensitive information (e.g., database credentials) from AWS Secrets Manager.

## Push Code to GitHub

### 6.1 Push Code to GitHub

- Push your Flask API code and the updated Jenkinsfile to the GitHub repository.

## Running Jenkins Pipeline

### 7.1 Run Jenkins Pipeline

- Trigger the Jenkins pipeline manually or set up webhooks to trigger it automatically on code changes.
- Monitor the Jenkins pipeline stages for successful deployment.

## Verification

### 8.1 Verify Deployment

- Check the logs and status in Jenkins to ensure that each stage of the pipeline is successful.
- Verify that the Flask API is running on your Amazon EKS cluster.

## Scaling and Monitoring

### 9.1 Scale and Monitor

- If needed, scale the deployment on Amazon EKS based on demand.
- Set up monitoring and logging for your Flask API using AWS services or other tools.

