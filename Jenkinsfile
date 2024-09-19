pipeline {
    agent any

    environment {
        SONAR_TOKEN = credentials('sonarqube-token')
    }

    stages {
        stage('Build') {
            steps {
                echo 'Building the project...'
                sh 'python3 -m venv venv'                   // Create virtual environment
                sh '. venv/bin/activate'                    // Activate virtual environment
                sh '/opt/anaconda3/bin/pip3 install -r requirements.txt' // Use full path to pip3
            }
        }

        stage('Test') {
            steps {
                echo 'Running tests...'
                sh '. venv/bin/activate && pytest test_main.py'
            }
        }

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
            sh 'rm -rf venv'
        }
    }
}

