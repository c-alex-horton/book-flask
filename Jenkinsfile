pipeline {
  agent any
  stages {
    stage('checkout code') {
      steps {
        git(url: 'https://github.com/c-alex-horton/book-flask', branch: 'main')
      }
    }
    stage('build') {
      steps {
        sh 'docker build -t book-flask .'
        sh 'docker run -d -p 5000:5000 book-flask'
      }
    }
    stage('test') {
      steps {
        script {
          // Run JUnit tests
          sh 'docker exec $(docker ps -q) python -m pytest --junitxml=junit-results.xml /tests'
          
          // See if the JUnit XML file was created
          sh 'docker exec $(docker ps -q) ls -l junit-results.xml'

          // Copy the JUnit XML file from the container to the Jenkins workspace
          sh 'docker cp $(docker ps -q):junit-results.xml . || echo "No JUnit XML file found"'

          // See if the JUnit XML file was copied to the Jenkins workspace
          sh 'ls -l junit-results.xml'

          // Print the contents of the JUnit XML file
          sh 'cat junit-results.xml'

          // Parse JUnit test results
          def junitResults = junit allowEmptyResults: true, testResults: 'junit-results.xml'

          // Archive JUnit test results
          archiveJunit 'junit-results.xml'
          
          // Check if any tests failed
          def testFailures = junitResults.failCount + junitResults.errorCount
          
          if (testFailures > 0) {
            currentBuild.result = 'FAILURE'
            error "JUnit tests failed: ${testFailures} test(s) failed"
          }
        }
      }
    }
  }
  post {
    always {
      sh 'docker stop $(docker ps -q)'
      sh 'docker rm $(docker ps -a -q)'
      sh 'docker rmi $(docker images -q)'
    }
  }
}