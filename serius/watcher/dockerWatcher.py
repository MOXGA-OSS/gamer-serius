import docker
from serius import serius

def watch(serviceKey, dockerHost, dockerPort, image):

   dockerClient = docker.DockerClient(base_url="tcp://"+dockerHost+":"+str(dockerPort))

   service = dockerClient.containers.list(filters={"ancestor": image})

   if len(service) == 1:

        serviceNetwork = service[0].attrs["NetworkSettings"]["Networks"]

        serviceIpAddress = next( iter(serviceNetwork.values()))["IPAddress"]

        serius.serviceIpAddresses.append(serviceIpAddress+" "+serviceKey+"-service")