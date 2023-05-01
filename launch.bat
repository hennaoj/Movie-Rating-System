set FLASK_APP=review_system
set FLASK_ENV=development

if exist .\instance del /q .\instance
if exist .\client\apikeys del /q .\client\apikeys\*


flask init-db
flask create-sample-data
flask create-sample-api-key

flask run
