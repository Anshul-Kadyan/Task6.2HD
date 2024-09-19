pipeline {
    agent any

    environment {
        SONAR_TOKEN = credentials('sonarqube-token') // Reference to the SonarQube token
    }

    stages {
        // Step 1: Build Stage
        stage('Build') {
            steps {
                echo 'Building the project...'
                sh 'python3 -m venv venv'            // Create virtual environment
                sh '. venv/bin/activate'             // Activate the virtual environment
                sh 'pip install -r requirements.txt' // Install dependencies
            }
        }

        // Step 2: Test Stage
        stage('Test') {
            steps {
                echo 'Running tests...'
                sh '. venv/bin/activate && pytest test_main.py' // Run pytest
            }
        }

        // Step 3: SonarQube Code Quality Analysis
        stage('SonarQube Analysis') {
            steps {
                script {
                    withSonarQubeEnv('SonarQube') {
                        sh '''
                        sonar-scanner \
                            -Dsonar.projectKey=flask-pipeline-project \
                            -Dsonar.sources=. \
                            -Dsonar.host.url=http://localhost:9000 \
                            -Dsonar.login=${SONAR_TOKEN}
                        '''
                    }
                }
            }
        }
    }

    post {
        always {
            echo 'Cleaning up...'
            sh 'rm -rf venv' // Clean up the virtual environment after the build
        }
    }
}
