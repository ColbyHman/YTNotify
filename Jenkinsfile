pipeline {
    agent any
    triggers {
        githubPush()
    }
    stages {
        stage('Build and Start Docker Service'){
            steps {
                sh """
                    sudo curl -L https://github.com/docker/compose/releases/download/1.8.0/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose
                    /usr/local/bin/docker-compose build
                    /usr/local/bin/docker-compose up -d mongodb
                """
            }
        }
        stage('Create Virtual Environment') {
            steps {
                sh """
                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip3 install -r setup/requirements.txt
                """
            }
        }
        stage('Static Analysis'){
            steps {
                sh """
                        . .venv/bin/activate
                        make lint
                    """
            }
        }
        stage('Unit Testing'){
            steps {
                sh """
                    . .venv/bin/activate
                    make test
                """
            }
        }
    }
}