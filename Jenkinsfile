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
            set + e
            // Run JUnit tests
            sh 'docker exec $(docker ps -q) python -m pytest --junitxml=junit-results.xml /tests'
            set - e
          } catch (e) {
              currentBuild.result = 'FAILURE'
              error "JUnit tests failed: ${e.toString()}"
        }
      }
    }
  }
}
  post {
    always {
      sh 'echo "Copying JUnit XML file from container to Jenkins workspace"'
      // Copy the JUnit XML file from the container to the Jenkins workspace
      sh 'docker cp $(docker ps -q):junit-results.xml . || echo "No JUnit XML file found"'

      // Archive JUnit test results
      sh 'echo "Archiving JUnit XML file"'
      junit 'junit-results.xml'
      sh 'echo "Archiving Done"'
      sh 'docker stop $(docker ps -q)'
      sh 'docker rm $(docker ps -a -q)'
      sh 'docker rmi $(docker images -q)'
    }
  }
}
