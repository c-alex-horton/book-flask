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
          try {
            // Run JUnit tests
            sh 'docker exec $(docker ps -q) python -m pytest --junitxml=junit-results.xml /tests'
          } catch (Exception e) {
            currentBuild.result = 'FAILURE'
            error "JUnit tests failed: ${e}"
          }

          // Copy the JUnit XML file from the container to the Jenkins workspace
          sh 'docker cp $(docker ps -q):junit-results.xml . || echo "No JUnit XML file found"'

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