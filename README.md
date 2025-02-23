# Aqar Plus

```
docker build . -t aqar
```

## SSL

To Use SSL, obtain the certificate via certbot, and copy the private key and certificate to the `ssl` directory in the root of the project.
then build the docker container.

```
cp /etc/letsencrypt/live/aqar.mona-hasan.com/fullchain.pem ./ssl/fullchain.pem
cp /etc/letsencrypt/live/aqar.mona-hasan.com/privkey.pem ./ssl/privkey.pem
```

## Build & Run

| if a previous container is running, stop it first

```
git pull
docker build . -t aqar
```

```
docker run -d --restart always -p 443:8080 aqar
```
