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
        sh 'docker exec $(docker ps -q) python -m pytest /tests | tee pytest-output.txt'
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