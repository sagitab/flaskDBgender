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
        stage('Setup Environment') {
            steps {
                withCredentials([
                    usernamePassword(credentialsId: 'aws_keys',
                                     usernameVariable: 'AWS_USERNAME',
                                     passwordVariable: 'AWS_SECRET_KEY')
                ]) {
                    script {
                        // Expose credentials to the rest of the pipeline
                        env.AWS_ACCESS_KEY = AWS_USERNAME
                        env.AWS_SECRET_KEY = AWS_SECRET_KEY
                        env.MYSQL_HOST='mysql'
                        env.MYSQL_USER='root'
                        env.MYSQL_PASSWORD= credentials('sql_pass')
                        env.MYSQL_DB='mydb'
                        env.PORT=5002
                        env.SSH_KEY_PATH= credentials('key_path')
                    }
                }
            }
        }
        stage('Deploy') {
            steps {
                echo "Running the deployment script..."
                sh 'python deploy.py'
            }
        }
        stage('Push image to dockerhub') {
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
