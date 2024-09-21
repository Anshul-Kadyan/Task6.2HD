pipeline {
    agent any

    environment {
        SONAR_TOKEN = credentials('sonarqube-token') // SonarQube token
        PATH = "/usr/local/bin:/opt/homebrew/bin:${env.PATH}" // Docker and AWS CLI paths
        DATADOG_API_KEY = credentials('datadog-api-key') // Datadog API key
    }

    stages {
        stage('Build') {
            steps {
                echo 'Building the project...'
                sh 'python3 -m venv venv && . venv/bin/activate && python3 -m pip install --upgrade pip && pip install -r requirements.txt'
            }
        }

        stage('Test') {
            steps {
                echo 'Running tests...'
                sh '. venv/bin/activate && pytest test_main.py'
            }
        }

        stage('Code Quality Analysis') {
            steps {
                withSonarQubeEnv('SonarQube') {
                    sh '/Users/kadyan/Downloads/sonar-scanner-6.1.0.4477-macosx-x64/bin/sonar-scanner -Dsonar.projectKey=flask-pipeline-project -Dsonar.sources=. -Dsonar.host.url=http://localhost:9000 -Dsonar.token=${SONAR_TOKEN} -Dsonar.exclusions=venv/**'
                }
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying the application using Docker...'
                sh 'docker build -t flask-app . && docker stop flask-app || true && docker rm flask-app || true && docker run -d -p 3000:5000 --name flask-app flask-app'
            }
        }

        stage('Release') {
            steps {
                echo 'Deploying to AWS CodeDeploy...'
                withCredentials([[$class: 'UsernamePasswordMultiBinding', credentialsId: 'aws-codedeploy-credentials', usernameVariable: 'AWS_ACCESS_KEY_ID', passwordVariable: 'AWS_SECRET_ACCESS_KEY']]) {
                    sh '''
                    aws deploy create-deployment \
                    --application-name FlaskAppDeploy \
                    --deployment-group-name FlaskAppDeploymentGroup \
                    --s3-location bucket=flask-app-deployment-bucket,key=flask-app.zip,bundleType=zip \
                    --deployment-config-name CodeDeployDefault.OneAtATime \
                    --region ap-southeast-2
                    '''
                }
            }
        }

        stage('Monitoring and Alerting') {
            steps {
                echo 'Monitoring application using Datadog...'

                // Trigger Datadog events and alerts
                sh '''
                curl -X POST \
                -H "Content-type: application/json" \
                -H "DD-API-KEY: ${DATADOG_API_KEY}" \
                -d '{
                      "title": "Jenkins Monitoring Alert",
                      "text": "Monitoring FlaskApp for performance issues.",
                      "priority": "normal",
                      "alert_type": "info"
                    }' \
                https://api.datadoghq.com/api/v1/events
                '''

                // Start Datadog agent on the server (if not already running)
                sh 'sudo systemctl start datadog-agent'
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
