pipeline {
    agent any
    triggers {
        githubPush()
    }
    stages {
        stage('Create Virtual Environment') {
            steps {
                sh """
                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip3 install -r requirements.txt
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
    }
}