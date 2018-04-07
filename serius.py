#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import logging
import os
import os.path
from shutil import copyfile
import sys
from rpTimer import rpTimer
import watcher.dockerWatcher as dockerWatcher

# Host Files
hostsFile = "/etc/hosts"
hostsWrite = "hosts.write"
hostsBackup = "hosts.backup"

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

    for serviceKey in configFileJson["services"].keys():

        log.info("Service: "+serviceKey)

        dockerHost = configFileJson["services"][serviceKey]["dockerHost"]
        dockerPort = configFileJson["services"][serviceKey]["dockerPort"]
        image = configFileJson["services"][serviceKey]["image"]

        log.info("Watching "+serviceKey+" Docker ...")

        dockerWatcher.watch(serviceKey, dockerHost, dockerPort, image)

        log.info("Received "+serviceKey+" Docker IP")

    copyfile(hostsWrite, hostsBackup)

    log.info("Map "+serviceKey+" Docker IP to Domain")

    for serviceIpAddress in dockerWatcher.serviceIpAddresses:

        with open(hostsWrite, "a") as file:

            file.write(serviceIpAddress+"\n")

            file.close()

    copyfile(hostsWrite, hostsFile)

    dockerWatcher.serviceIpAddresses = []

# Main

log.info("Starting Serius ...")

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

            timer = repeatedTimer(configFileJson["watchInterval"], resolveDockerIPToDomain, configFileJson)

    else:
        
        log.error("You should use -c to config Serius.")

else:
        
    log.error("Invalid parameters")
    

