 //     stage('Run script on ec2') {
    //         steps {
    //             echo 'Running Docker container...'
    //            sh '''
    //             if docker ps -a --format '{{.Names}}' | grep -q "flaskaws"; then
    //                 docker stop flaskaws || true
    //                 docker rm flaskaws || true
    //             fi
    //             docker run -d --name flaskaws -p 5002:5002 sagisen/flaskaws:0.0.7
    //             '''

    //         }
    //     }
    //    stage('Test') {
    //         steps {
    //             echo "Testing application..."
    //             script {
    //                 // Wait for the container to be ready
    //                 sh '''
    //                 for i in {1..10}; do
    //                     if curl -o /dev/null -s -w "%{http_code}" http://127.0.0.1:5002 | grep -q "200"; then
    //                         echo "Application is ready"
    //                         break
    //                     else
    //                         echo "Waiting for application to be ready..."
    //                         sleep 5
    //                     fi
    //                 done
    //                 '''
    //             }
    //         }
    //     }