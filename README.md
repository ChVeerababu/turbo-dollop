sitemanager:


git clone repo\n
cd repo
docker build -t pytorch_odapi .
docker run -dp 5050:5000 pytorch_odapi
docker container restart pytorch_odapi

device:
git clone -b dev repo
cd repo
docker-compose up -d
