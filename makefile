setup:
	python3 -m venv venv && . ./venv/bin/activate && pip install -r requirements.txt && python3 -m spacy download pt_core_news_sm

train-model:
	python3 -m rasa train

run:
	docker-compose up -d && rasa run -m models --enable-api --cors "*" --debug && rasa run actions --actions actions.actions --debug && rasa run shell