pipeline {
    environment {
        // AWS_ACCOUNT_ID = credentials('aws-account-id')
        // AWS_ACCOUNT_ID = ''

        AWS_REGION = 'us-east-1' // Adjust to your AWS region
        ECR_REPO_NAME = 'flask'
        IMAGE_TAG = "${env.BUILD_ID}"

        // AWS_REGION = 'us-west-2'
        // ECR_REPO_NAME = 'my-repo'
        // IMAGE_TAG = 'latest'
        AWS_ACCESS_KEY_ID = credentials('AWS_ACCESS_KEY_ID')     // Jenkins credential ID for access key
        AWS_SECRET_ACCESS_KEY = credentials('AWS_SECRET_ACCESS_KEY') // Jenkins credential ID for secret key
        AWS_ACCOUNT_ID = credentials('aws-account-id') 
        TASK_DEFINITION = 'falsk-family'
        CLUSTER_NAME='flask-cluster'
        SERVICE_NAME='flask-first-service'

    }
    agent any
    
    stages {
       
        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPO_NAME}:${IMAGE_TAG}")
                }
            }
        }

        stage('Login to ECR') {
            
            steps {
                // echo "AWS_ACCESS_KEY_ID: ${AWS_ACCESS_KEY_ID}"
                script {
                    // Login to ECR with AWS CLI
                    sh '''
                    aws configure set aws_access_key_id ${AWS_ACCESS_KEY_ID}
                    aws configure set aws_secret_access_key ${AWS_SECRET_ACCESS_KEY}
                    aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com
                    '''
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

        stage('Update ECS Task Definition') {
            steps {
                script {
                    // Register a new ECS task definition with the updated image
                    sh '''
                    aws ecs register-task-definition \
                    --family ${TASK_DEFINITION} \
                    --container-definitions "$(jq --arg IMAGE_URI "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPO_NAME}:${IMAGE_TAG}" \
                    '.[] | .image = $IMAGE_URI' task-definition.json)" \
                    --region ${AWS_REGION}
                    '''
                }
            }
        }
        stage('Update ECS Service') {
            steps {
                script {
                    // Update the ECS service to use the new task definition
                    sh '''
                    TASK_REVISION=$(aws ecs describe-task-definition \
                        --task-definition ${TASK_DEFINITION} \
                        --query "taskDefinition.revision" \
                        --output text --region ${AWS_REGION})

                    aws ecs update-service \
                        --cluster ${CLUSTER_NAME} \
                        --service ${SERVICE_NAME} \
                        --task-definition ${TASK_DEFINITION}:${TASK_REVISION} \
                        --region ${AWS_REGION}
                    '''
                }
            }
        }
        // stage('Deploy to ECS') {
        //     steps {
        //         script {
        //             sh """
        //                 aws ecs update-service \
        //                     --cluster flask-cluster \
        //                     --service flask-first-service \
        //                     --force-new-deployment \
        //                     --region ${AWS_REGION}
        //             """
        //         }
        //     }
        // }
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