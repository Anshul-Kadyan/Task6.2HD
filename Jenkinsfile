pipeline {
    agent any

    environment {
        SONAR_TOKEN = credentials('sonarqube-token') // SonarQube token
        PATH = "/usr/local/bin:${env.PATH}" // Add Docker path to Jenkins environment
        AWS_CREDENTIALS = credentials('aws-codedeploy-credentials') // AWS CodeDeploy Credentials
    }

    stages {
        // Build Stage
        stage('Build') {
            steps {
                echo 'Building the project...'
                sh 'python3 -m venv venv' // Create virtual environment
                sh '. venv/bin/activate && python3 -m pip install --upgrade pip' // Upgrade pip
                sh '. venv/bin/activate && pip install -r requirements.txt' // Install dependencies
                sh '. venv/bin/activate && pip install pytest' // Install pytest
            }
        }

        // Test Stage
        stage('Test') {
            steps {
                echo 'Running tests...'
                sh '. venv/bin/activate && pytest test_main.py' // Run tests
            }
        }

        // Code Quality Analysis Stage
        stage('Code Quality Analysis') {
            steps {
                script {
                    withSonarQubeEnv('SonarQube') {
                        sh '''
                        ~/Downloads/sonar-scanner-6.1.0.4477-macosx-x64/bin/sonar-scanner \
                        -Dsonar.projectKey=flask-pipeline-project \
                        -Dsonar.sources=. \
                        -Dsonar.host.url=http://localhost:9000 \
                        -Dsonar.token=${SONAR_TOKEN} \
                        -Dsonar.exclusions=venv/**
                        '''
                    }
                }
            }
        }

        // Deploy Stage
        stage('Deploy') {
            steps {
                echo 'Deploying the application using Docker...'
                sh 'docker build -t flask-app .' // Build Docker image
                sh 'docker stop flask-app || true' // Stop any existing container
                sh 'docker rm flask-app || true' // Remove the existing container
                sh 'docker run -d -p 3000:5000 --name flask-app flask-app' // Run the Docker container
            }
        }

        // Release Stage (AWS CodeDeploy)
        stage('Release') {
            steps {
                echo 'Deploying to AWS CodeDeploy...'
                script {
                    sh '''
                    aws deploy create-deployment \
                    --application-name FlaskApp \
                    --deployment-group-name FlaskAppDeploymentGroup \
                    --s3-location bucket=flask-app-deployment-bucket,key=flask-app.zip,bundleType=zip \
                    --deployment-config-name CodeDeployDefault.OneAtATime \
                    --region ap-southeast-2 \
                    --access-key-id ${AWS_CREDENTIALS_USR} \
                    --secret-access-key ${AWS_CREDENTIALS_PSW}
                    '''
                }
            }
        }

        // Monitoring & Alerting (Optional for High HD)
        stage('Monitoring & Alerting') {
            steps {
                echo 'Setting up monitoring and alerting...'
                // Add monitoring and alerting tool configuration (e.g., Datadog, New Relic)
            }
        }
    }

    post {
        always {
            echo 'Cleaning up...'
            sh 'rm -rf venv' // Clean up the virtual environment
        }
    }
}
