pipeline {
    environment {
        AWS_ACCOUNT_ID = credentials('aws-account-id')
        AWS_REGION = 'us-east-1' // Adjust to your AWS region
        ECR_REPO_NAME = 'flask'
        IMAGE_TAG = "${env.BUILD_ID}"
    }
    agent any
    
    stages {
        // stage('Checkout Code') {
        //     steps {
        //         // Pull the code from your repository
        //         git 'https://github.com/your-repo/flask-app.git'
        //     }
        // }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPO_NAME}:${IMAGE_TAG}")
                }
            }
        }

        stage('Login to ECR') {
            steps {
                script {
                    sh "aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"
                }
            }
        }

        stage('Push Docker Image to ECR') {
            steps {
                script {
                    docker.image("${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPO_NAME}:${IMAGE_TAG}").push()
                }
            }
        }

        stage('Deploy to ECS') {
            steps {
                script {
                    sh """
                        aws ecs update-service \
                            --cluster flask-cluster \
                            --service flask-first-service \
                            --force-new-deployment \
                            --region ${AWS_REGION}
                    """
                }
            }
        }
    }

    post {
        always {
            // Clean up the local workspace after each build
            sh "docker rmi ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPO_NAME}:${IMAGE_TAG} || true"
        }
        success {
            echo "Deployment to ECS was successful."
        }
        failure {
            echo "Deployment failed. Check logs for details."
        }
    }
}