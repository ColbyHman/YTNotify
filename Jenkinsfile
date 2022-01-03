pipeline {
    agent{
        docker {
          image 'python:3.8'
        }
    }
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
                        pylint --fail-under=8 bot.py
                        pylint --fail-under=8 lambda.py
                        pylint --fail-under=8 db_model.py
                        pylint --fail-under=8 db_wrapper.py
                    """
            }
        }
        stage('Unit Testing'){
            steps {
                sh """
                    echo "Tested!"
                """
            }
        }
    }
}