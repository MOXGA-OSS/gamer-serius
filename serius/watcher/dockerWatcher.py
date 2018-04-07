import docker

serviceIpAddresses = []

def watch(serviceKey, dockerHost, dockerPort, image):

   dockerClient = docker.DockerClient(base_url="tcp://"+dockerHost+":"+str(dockerPort))

   service = dockerClient.containers.list(filters={"ancestor": image})

   if len(service) == 1:

        serviceNetwork = service[0].attrs["NetworkSettings"]["Networks"]

        serviceIpAddress = next( iter(serviceNetwork.values()))["IPAddress"]

        serviceIpAddresses.append(serviceKey+"-service "+serviceIpAddress)