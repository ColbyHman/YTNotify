lint:
	pylint --fail-under=8 application/discord_bot/
	pylint --fail-under=8 application/scripts/lambda.py
	pylint --fail-under=8 application/database/
test:
	pytest --cov=. ./tests/