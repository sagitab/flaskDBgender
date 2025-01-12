pipeline {
    agent any
    environment {
        build_number = "${env.BUILD_NUMBER}" // Build number from Jenkins
        image_name = "sagisen/flaskaws:0.0.${env.BUILD_NUMBER}" // Docker image name
    }
    triggers {
        pollSCM('* * * * *') // Poll SCM every minute
    }
    stages {
        stage('Clean') {
            steps {
                echo 'Cleaning workspace...'
                sh 'rm -rf flaskDBgender'
            }
        }
        stage('Clone Code') {
            steps {
                echo 'Cloning repository...'
                sh 'git clone https://github.com/sagitab/flaskDBgender.git'
            }
        }
        stage('Build') {
            steps {
                echo 'Building Docker image...'
                withCredentials([usernamePassword(credentialsId: 'docker_creds', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                    sh '''
                      docker login -u ${DOCKER_USERNAME} -p ${DOCKER_PASSWORD}
                      docker build -t ${image_name} flaskDBgender
                    '''
                }
            }
        }
        stage('Run script on ec2') {
            steps {
                echo 'Running Docker container...'
               sh '''
                if docker ps -a --format '{{.Names}}' | grep -q "flaskaws"; then
                    docker stop flaskaws || true
                    docker rm flaskaws || true
                fi
                docker run -d --name flaskaws -p 5002:5002 sagisen/flaskaws:0.0.7
                '''

            }
        }
       stage('Test') {
            steps {
                echo "Testing application..."
                script {
                    // Wait for the container to be ready
                    sh '''
                    for i in {1..10}; do
                        if curl -o /dev/null -s -w "%{http_code}" http://127.0.0.1:5002 | grep -q "200"; then
                            echo "Application is ready"
                            break
                        else
                            echo "Waiting for application to be ready..."
                            sleep 5
                        fi
                    done
                    '''
                }
            }
        }
        stage('Deploy') {
            steps {
                echo 'Pushing Docker image to registry...'
                withCredentials([usernamePassword(credentialsId: 'docker_creds', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                    sh '''
                      docker login -u ${DOCKER_USERNAME} -p ${DOCKER_PASSWORD}
                      docker push ${image_name}
                    '''
                }
            }
        }
    }
    post {
        always {
            echo 'Pipeline execution completed.'
            sh '''
              docker stop flaskaws || true
              docker rm flaskaws || true
            '''
        }
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}
