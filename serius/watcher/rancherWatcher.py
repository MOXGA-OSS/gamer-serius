import docker
from serius import serius

def watch(serviceKey, dockerHost, dockerPort, image):

   dockerClient = docker.DockerClient(base_url="tcp://"+dockerHost+":"+str(dockerPort))

   service = dockerClient.containers.list(filters={"ancestor": image})

   if len(service) == 1:

        serviceLabels = service[0].attrs["Config"]["Labels"]

        serviceIpAddress = serviceLabels["io.rancher.container.ip"]

        serviceIpAddress = serviceIpAddress.replace("/16","")

        serius.serviceIpAddresses.append(serviceIpAddress+" "+serviceKey+"-service")