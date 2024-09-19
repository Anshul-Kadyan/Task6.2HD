pipeline {
    agent any

    environment {
        SONAR_TOKEN = credentials('sonarqube-token') // SonarQube token
        AWS_ACCESS_KEY_ID = credentials('aws-access-key-id') // AWS Access Key
        AWS_SECRET_ACCESS_KEY = credentials('aws-secret-access-key') // AWS Secret Key
    }

    stages {
        stage('Build') {
            steps {
                echo 'Building the project...'
                sh 'python3 -m venv venv' // Create virtual environment
                sh '. venv/bin/activate && python3 -m pip install --upgrade pip' // Upgrade pip
                sh '. venv/bin/activate && pip install -r requirements.txt' // Install dependencies
                sh '. venv/bin/activate && pip install pytest' // Install pytest
            }
        }

        stage('Test') {
            steps {
                echo 'Running tests...'
                sh '. venv/bin/activate && pytest test_main.py' // Run tests
            }
        }

        stage('SonarQube Analysis') {
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

        stage('Deploy') {
            steps {
                echo 'Deploying the application using Docker...'
                sh 'docker build -t flask-app .' // Build Docker image
                sh 'docker stop flask-app || true' // Stop any existing container
                sh 'docker rm flask-app || true' // Remove the existing container
                sh 'docker run -d -p 3000:5000 --name flask-app flask-app' // Run the Docker container
            }
        }

        // AWS CodeDeploy Stage
        stage('AWS CodeDeploy') {
            steps {
                echo 'Deploying to AWS CodeDeploy...'
                script {
                    sh '''
                    aws deploy create-deployment \
                    --application-name FlaskApp \
                    --deployment-group-name <YourDeploymentGroupName> \
                    --s3-location bucket=<YourS3Bucket>,key=flask-app.zip,bundleType=zip \
                    --deployment-config-name CodeDeployDefault.OneAtATime \
                    --region <YourRegion>
                    '''
                }
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
