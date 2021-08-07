# MarvikAPI

This project is about a simple REST API with 2 endpoints:
  * /counters
  * /timestamp

## Run the API

### Production

In order to deploy de API you need to build the docker images by running

```bash
make build
```

and then start the needed containers with

```bash
make run
```

The API will be running in **http://localhost:8000** and you can see the available endpoints
in  **http://localhost:8000/docs**

Another alternative is to use make the request with Curl. You can one of the following:


```bash
curl -X 'GET' 'http://localhost:8000/counters' -H 'accept: application/json'
```

```bash
curl -X 'POST' 'http://localhost:8000/timestamp' -H 'accept: application/json' -H 'Content-Type: application/json' -d '{"mode": true}'
```

```bash
curl -X 'POST' 'http://localhost:8000/timestamp' -H 'accept: application/json' -H 'Content-Type: application/json' -d '{"mode": false}'
```



### Development

In order to deploy de API you need to build the docker images by running

```bash
make build_dev
```

and then start the needed containers with

```bash
make run_dev
```

In this way, the code folder is mounted by a volume and the API won0t be running by default. You
will need to go inside the container and launch it
