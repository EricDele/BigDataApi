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

    # Test RANGER API V1

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

    # Test RANGER API V2

    result = rangerApi.getV2Services()
    print(rangerApi)

    result = rangerApi.getV2PolicyByServiceAndPolicyName("Sandbox_hadoop", "HDFS Global Allow")
    print(rangerApi)

    result = rangerApi.getV2PolicyByServiceAndPolicyName("Sandbox_hive", "all - database, table, column")
    print(rangerApi)

    result = rangerApi.getV2SearchPolicyInService("Sandbox_hadoop", "HDFS Global Allow")
    print(rangerApi)

    result = rangerApi.postV2CreatePolicy("Sandbox_hadoop", "lake_test", "policy for the lake test", ["/lake/test"], True, "it1", "", "r--")
    print(rangerApi)

    result = rangerApi.postV2ApplyPolicy("Sandbox_hadoop", "lake_test", "policy for the lake test", ["/lake/test"], False, "it1", "", "r-x")
    print(rangerApi)

    result = rangerApi.putV2UpdatePolicyByServiceAndPolicyName("Sandbox_hadoop", "lake_test", "policy for the lake test", ["/lake/test"], False, "it1", "", "r--")
    print(rangerApi)

    result = rangerApi.deleteV2DeletePolicyByServiceAndPolicyName("Sandbox_hadoop", "lake_test")
    print(rangerApi)

    # API for Users and groups management

    result = rangerApi.getUsers()
    print(rangerApi)

    result = rangerApi.createUser("user77", "user77", "user77", "user77", "user77", "user77", [2], ["ROLE_USER"])
    print(rangerApi)

    result = rangerApi.getUser("user77")
    print(rangerApi)

    result = rangerApi.setRoleForUser("user77", "ROLE_SYS_ADMIN")
    print(rangerApi)

    result = rangerApi.getUser("user77")
    print(rangerApi)

    result = rangerApi.deleteUser("user77")
    print(rangerApi)

    result = rangerApi.getUser("user77")
    print(rangerApi)

    result = rangerApi.getGroups()
    print(rangerApi)

    result = rangerApi.getGroup("admin")
    print(rangerApi)

    result = rangerApi.getGroup(12)
    print(rangerApi)


if __name__ == '__main__':
    testAmbari()
    testRanger()
