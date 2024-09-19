pipeline {
    agent any
    environment {
        // SonarQube environment variables
        SONARQUBE_URL = 'http://localhost:9000'
        SONAR_TOKEN = credentials('sonar-token')
    }
    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/Anshul-Kadyan/Task6.2HD.git'
            }
        }
        stage('Build') {
            steps {
                echo 'Building the project...'
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }
        stage('Test') {
            steps {
                echo 'Running tests...'
                sh '''
                    . venv/bin/activate
                    pytest test_main.py
                '''
            }
        }
        stage('SonarQube Analysis') {
            environment {
                scannerHome = tool 'SonarQube Scanner'
            }
            steps {
                withSonarQubeEnv('SonarQube') {
                    sh """
                        ${scannerHome}/bin/sonar-scanner \
                        -Dsonar.projectKey=flask-pipeline-project \
                        -Dsonar.sources=. \
                        -Dsonar.host.url=$SONARQUBE_URL \
                        -Dsonar.login=$SONAR_TOKEN \
                        -Dsonar.sourceEncoding=UTF-8  # Explicitly setting source encoding
                    """
                }
            }
        }
    }
}
