import docker

serviceIpAddresses = []

def watch(serviceKey, dockerHost, dockerPort, image):

   dockerClient = docker.from_env()

   service = dockerClient.containers.list(filters={"ancestor": image})

   if len(service) == 1:

        serviceNetwork = service[0].attrs["NetworkSettings"]["Networks"]

        serviceIpAddress = next( iter(serviceNetwork.values()))["IPAddress"]

        serviceIpAddresses.append(serviceKey+"-service "+serviceIpAddress)