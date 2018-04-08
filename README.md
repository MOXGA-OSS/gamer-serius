### Gamer Serius: Microservice Docker DNS for Local Linux 

At [GAMER](https://gamer.in.th), we use Serius to address Docker IP recognitions in local Linux for each service. Serius will map a Docker IP for each service to one service domain name for the Linux. 

## Requirements 

- Python version 3.6+
- Allowance of Docker Remote API for each microservice Docker host
- Root access to your local Linux

## Configurations 

watchInterval - time in seconds to watch service Dockers

watchType - type to watch (docker or rancher)

### Service Section

dockerHost - a service Docker host IP

dockerPort - a service Docker host port

image - a service Docker image

## Installing Serius 

To install Serius to your projects, you have to run pip install:

```shell
$ pip install serius
```

## How to use Serius?

```shell
$ serius -c serius.conf.json
```

-c is for a Serius config file.

## License

Serius is MIT Licensed.
