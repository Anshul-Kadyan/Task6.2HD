pipeline {
    agent any

    environment {
        SONAR_TOKEN = credentials('sonarqube-token') // Reference to the SonarQube token
    }

    stages {
        stage('Build') {
            steps {
                echo 'Building the project...'
                sh 'python3 -m venv venv' // Create virtual environment
                sh '. venv/bin/activate && python3 -m pip install --upgrade pip' // Upgrade pip
                sh '. venv/bin/activate && pip install -r requirements.txt' // Install dependencies
                sh '. venv/bin/activate && pip install pytest' // Install pytest in the virtual environment
            }
        }

        stage('Test') {
            steps {
                echo 'Running tests...'
                sh '. venv/bin/activate && pytest test_main.py' // Run tests with pytest
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
    }

    post {
        always {
            echo 'Cleaning up...'
            sh 'rm -rf venv' // Clean up virtual environment
        }
    }
}
