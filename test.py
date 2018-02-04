#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ambari import AmbariApi
from ranger import RangerApi

def testAmbari():
    ambariApi = AmbariApi("http", "127.0.0.1", "8080", "basic")
    ambariApi.setCredentialsBasic("admin", "hortonworks")

    result = ambariApi.getAdminViewVersion()
    print(ambariApi)

    result = ambariApi.getClusterName()
    print(ambariApi)

    result = ambariApi.getClusterStatus()
    print(ambariApi)

    result = ambariApi.getClusterStaleConfig()
    print(ambariApi)

    result = ambariApi.getResourceManagerHosts()
    print(ambariApi)

    result = ambariApi.getQueuesFromAmbari()
    print(ambariApi)

    result = ambariApi.postServiceCheck("HDFS")
    print(ambariApi)

def testRanger():
    rangerApi = RangerApi("http", "127.0.0.1", "6080", "basic")
    rangerApi.setCredentialsBasic("raj_ops", "raj_ops")
    result = rangerApi.getServices()
    print(rangerApi)

    result = rangerApi.getPolicies()
    print(rangerApi)

    result = rangerApi.getPolicy(16)
    print(rangerApi)

    result = rangerApi.getPolicy("HDFS Global Allow")
    print(rangerApi)

    result = rangerApi.getService(1)
    print(rangerApi)

    result = rangerApi.getService("Sandbox_hadoop")
    print(rangerApi)

    # API for Users and groups management return an XML object
    result = rangerApi.getUsers()
    print(result)

    result = rangerApi.getUser("guest")
    print(result)

    result = rangerApi.getUser(48)
    print(result)

    result = rangerApi.getGroups()
    print(result)

    result = rangerApi.getGroup("admin")
    print(result)

    result = rangerApi.getGroup(12)
    print(result)

if __name__ == '__main__':
    # testAmbari()
    testRanger()
