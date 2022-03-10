pipeline {
    agent{
        any
    }
    triggers {
        githubPush()
    }
    stages {
        stage('Build and Start Docker Service'){
            steps {
                sh """
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