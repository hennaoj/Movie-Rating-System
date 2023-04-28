set FLASK_APP=review_system
set FLASK_ENV=development

if exist .\instance rmdir /q .\instance

set FLASK_APP=review_system
set FLASK_ENV=development
flask init-db
flask create-sample-data
flask create-sample-api-key
