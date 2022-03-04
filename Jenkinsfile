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
                    pip3 install -r setup/requirements.txt
                """
            }
        }
        stage('Static Analysis'){
            steps {
                sh """
                        . .venv/bin/activate
                        pylint --fail-under=8 application/discord_bot/bot.py
                        pylint --fail-under=8 application/discord_bot/controller.py
                        pylint --fail-under=8 application/scripts/lambda.py
                        pylint --fail-under=8 application/database/db_model.py
                        pylint --fail-under=8 application/database/db_wrapper.py
                        pylint --fail-under=8 application/database/mongo.py
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