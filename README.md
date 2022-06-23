sitemanager:

```
git clone https://github.com/ravichandra99/turbo-dollop.git
cd turbo-dollop
docker build -t pytorch_odapi .
docker run -dp 5050:5000 pytorch_odapi
docker container restart pytorch_odapi
```

device:

```
git clone -b dev [repo](https://github.com/ravichandra99/turbo-dollop.git)
cd turbo-dollop
docker-compose up -d
```
