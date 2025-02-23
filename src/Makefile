dev:
	flask run --host 0.0.0.0 --port 5002 --debug  

production:
	nohup gunicorn -w 4 -b 0.0.0.0:5000 app:app > gunicorn.log 2>&1 &

run_initial:
	pip3 install -r requirements.txt
	python3 run.py

