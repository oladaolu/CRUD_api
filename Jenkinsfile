pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'myflaskapp:1.0.0'
        K8S_CLUSTER_NAME = 'your-eks-cluster-name'
        K8S_REGION = 'your-aws-region'
        K8S_NAMESPACE = 'your-namespace'
        GIT_CREDENTIALS_ID = 'gitCredentials'
        DOCKERHUB_CREDENTIALS_ID = 'DockerHubCredentials'
    }

    stages {
        stage('Checkout') {
            steps {
                script {
                    checkout([$class: 'GitSCM', branches: [[name: '*/main']], userRemoteConfigs: [[url: "your github url", credentialsId: GIT_CREDENTIALS_ID]]])
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                withCredentials([string(credentialsId: DOCKERHUB_CREDENTIALS_ID, variable: 'DockerHubCredentials')]) {
                    script {
                        docker.withRegistry('https://index.docker.io/v1/', 'DockerHubCredentials') {
                            docker.build(DOCKER_IMAGE)
                            docker.push(DOCKER_IMAGE)
                        }
                    }
                }
            }
        }

        stage('Deploy to EKS') {
            steps {
                script {
                    sh "aws eks --region ${K8S_REGION} update-kubeconfig --name ${K8S_CLUSTER_NAME}"
                    sh "kubectl config use-context ${K8S_CLUSTER_NAME}"
                    sh "kubectl apply -f kubernetes/ --namespace=${K8S_NAMESPACE}"
                }
            }
        }
    }

    post {
        success {
            echo 'Deployment successful!'
        }

        failure {
            echo 'Deployment failed. Check logs for details.'
        }
    }
}
