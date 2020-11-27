### Transcriptions Flask API ###
export FLASK_APP=app.py
python3 -m flask run


docker build -t flask-librosa:latest .
docker run -p 5000:5000 flask-librosa:latest


### Deployment to AWS ECS ###

