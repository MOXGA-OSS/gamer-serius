#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import json
import dockerWatcher
import os.path
from shutil import copyfile
import os

# IP Resolver

def resolveDockerIPToDomain(configFileJson):

    if os.path.isfile("hosts.backup"):

        copyfile("hosts.backup","hosts.write")

    else:

        copyfile("/etc/hosts","hosts.write")

        for serviceKey in configFileJson['services'].keys():

            dockerHost = configFileJson['services'][serviceKey]['dockerHost']
            dockerPort = configFileJson['services'][serviceKey]['dockerPort']
            image = configFileJson['services'][serviceKey]['image']

            dockerWatcher.watch(serviceKey, dockerHost, dockerPort, image)

        copyfile("hosts.write", "hosts.backup")

        for serviceIpAddress in dockerWatcher.serviceIpAddresses:

            with open('hosts.write', 'a') as file:

                file.write(serviceIpAddress+'\n')

        os.system("cat hosts.write > /etc/hosts")

# Main

seriusArgs = sys.argv

if len(seriusArgs) == 3:

    configArg = seriusArgs[1]

    if configArg == "-c":

        configFileArg = seriusArgs[2]

        if configFileArg is not None:

            configFileJson = json.load(open(configFileArg))

    else:
        
        print ("You should use -c to config Serius.")

else:
        
    print ("Invalid parameters")
    

