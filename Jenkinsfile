pipeline {
    agent any

    environment {
        SONAR_TOKEN = credentials('sonarqube-token') // SonarQube token
        PATH = "/usr/local/bin:${env.PATH}" // Add Docker path to Jenkins environment
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
                sh 'docker stop flask-app || echo "No running container"' // Stop any existing container
                sh 'docker rm flask-app || echo "No existing container"' // Remove the existing container
                sh 'docker run -d -p 3000:5000 --name flask-app flask-app' // Run the Docker container
            }
        }

        stage('Release') {
            steps {
                echo 'Pushing Docker image to DockerHub...'
                sh '''
                docker tag flask-app anshul1413/flask-app:latest
                docker push anshul1413/flask-app:latest
                '''
            }
        }
    }

    post {
        always {
            echo 'Cleaning up...'
            sh 'rm -rf venv' // Clean up the virtual environment
            sh 'docker system prune -f' // Clean up Docker images and containers
        }
    }
}
