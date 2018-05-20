import collections
import json
import logging
import os
import os.path
from pathlib import Path
from shutil import copyfile
from serius.thread.timer.repeatedTimer import repeatedTimer
import serius.watcher.dockerWatcher as dockerWatcher
import serius.watcher.rancherWatcher as rancherWatcher
import sys

# Home Path
homePath = str(Path.home())

# Host Files
hostsFile = "/etc/hosts"
hostsWrite = homePath+"/serius/hosts.write"
hostsBackup = homePath+"/serius/hosts.backup"

# Service IP Addresses
serviceIpAddresses = []

# Service Old IP Addresses
serviceOldIpAddresses = []

# Loggings
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s.%(funcName)s +%(lineno)s: %(levelname)-3s [%(process)d] %(message)s")
log = logging.getLogger('Serius')

# IP Resolver
def resolveDockerIPToDomain(configFileJson):

    if os.path.exists(hostsBackup):
        
        copyfile(hostsBackup, hostsWrite)

    else:

        if not os.path.exists(hostsFile):

          with open(hostsFile,"w")  as file:

              file.close()

        copyfile(hostsFile, hostsWrite)

    global serviceIpAddresses

    serviceIpAddresses = []

    for serviceKey in configFileJson["services"].keys():

        log.info("Service: "+serviceKey)

        dockerHost = configFileJson["services"][serviceKey]["dockerHost"]
        dockerPort = configFileJson["services"][serviceKey]["dockerPort"]
        image = configFileJson["services"][serviceKey]["image"]

        log.info("Watching "+serviceKey+" Docker ...")

        if configFileJson["watchType"] == "docker":

            dockerWatcher.watch(serviceKey, dockerHost, dockerPort, image)

        elif configFileJson["watchType"] == "rancher":

            rancherWatcher.watch(serviceKey, dockerHost, dockerPort, image)

        log.info("Received "+serviceKey+" Docker IP")

    copyfile(hostsWrite, hostsBackup)

    global serviceOldIpAddresses

    log.info("Checking if service IP addresses have been changed ...")

    compare = lambda x, y: collections.Counter(x) == collections.Counter(y)

    if not compare(serviceIpAddresses, serviceOldIpAddresses):

        log.info("Updated the host DNS")

        for serviceIpAddress in serviceIpAddresses:

            with open(hostsWrite, "a") as file:

                file.write(serviceIpAddress+"\n")

                file.close()

        copyfile(hostsWrite, hostsFile)

        serviceOldIpAddresses = []

        serviceOldIpAddresses = serviceIpAddresses[:]

    else:

        log.info("Nothing changed")


# Main

def main():

    log.info("Starting Serius ...")

    log.info("Creating a Serius directory ...")

    if not os.path.exists(homePath+"/serius"):

        os.makedirs(homePath+"/serius")

    log.info("Already created a Serius directory")

    seriusArgs = sys.argv

    log.info("Checking parameters ...")

    if len(seriusArgs) == 3:

        configArg = seriusArgs[1]

        if configArg == "-c":

            configFileArg = seriusArgs[2]

            if configFileArg is not None:

                log.info("All parameters are correct.")

                log.info("Loading the JSON config file ...")

                configFileJson = json.load(open(configFileArg))

                log.info("Loading finished")

                log.info("Resolving service Docker IPs ...")

                if configFileJson["watchType"] == "docker":

                    log.info("Using Docker watcher ...")

                elif configFileJson["watchType"] == "rancher":

                    log.info("Using Rancher watcher ...")

                repeatedTimer(configFileJson["watchInterval"], resolveDockerIPToDomain, configFileJson)

        else:
            
            log.error("You should use -c to config Serius.")

    else:
            
        log.error("Invalid parameters")
    

