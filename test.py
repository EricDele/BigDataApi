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

    # result = ambariApi.getClusterServices()
    # for item in result.json()["items"]:
    #     print(item["ServiceInfo"]["service_name"])

    # result = ambariApi.putClusterServiceStart("OOZIE")
    # result = ambariApi.getRequestStatus(result.json()["Requests"]["id"])

    # result = ambariApi.putClusterServiceStop("OOZIE")
    # ambariApi.waitUntilRequestsCompleted(result.json()["Requests"]["id"])

    # resultArray = ambariApi.putClusterServiceStopAll()
    # ambariApi.waitUntilRequestsCompleted(resultArray)

    # resultArray = ambariApi.putClusterServiceStartAll()
    # ambariApi.waitUntilRequestsCompleted(resultArray)

    # result = ambariApi.getClusterStaleConfig()
    # print(ambariApi)

    # result = ambariApi.getResourceManagerHosts()
    # print(ambariApi)

    # result = ambariApi.getQueuesFromAmbari()
    # print(ambariApi)

    # result = ambariApi.postServiceCheck("HDFS")
    # print(ambariApi)

    # resultArray = ambariApi.postAllServicesCheck()
    # ambariApi.waitUntilRequestsCompleted(resultArray)

    # result = ambariApi.getRequests()
    # print(ambariApi)

    # result = ambariApi.putAbortStuckRequest(189)
    # print(ambariApi)

def testRanger():
    # Test RANGER API V2

    rangerApi = RangerApi("http", "127.0.0.1", "6080", "basic")
    rangerApi.setCredentialsBasic("raj_ops", "raj_ops")

    result = rangerApi.getService(1)
    print(rangerApi)

    result = rangerApi.getService("Sandbox_hadoop")
    print(rangerApi)

    result = rangerApi.getServices()
    print(rangerApi)

    result = rangerApi.getPolicyByServiceAndPolicyName("Sandbox_hadoop", "HDFS Global Allow")
    print(rangerApi)

    result = rangerApi.getPolicyByServiceAndPolicyName("Sandbox_yarn", "all - queue")
    print(rangerApi)

    result = rangerApi.getPolicyByServiceAndPolicyName("Sandbox_hive", "all - database, table, column")
    print(rangerApi)

    result = rangerApi.getSearchPolicyInService("Sandbox_hadoop", "HDFS Global Allow")
    print(rangerApi)

    result = rangerApi.postCreatePolicy("Sandbox_hadoop", "lake_test", "policy for the lake test", ["/lake/test"], True, "it1", "", "r--")
    print(rangerApi)

    result = rangerApi.postApplyPolicy("Sandbox_hadoop", "lake_test", "policy for the lake test", ["/lake/test"], False, "it1", "", "r-x")
    print(rangerApi)

    result = rangerApi.putUpdatePolicyByServiceAndPolicyName("Sandbox_hadoop", "lake_test", "policy for the lake test", ["/lake/test"], False, "it1", "", "rwx")
    print(rangerApi)

    result = rangerApi.getPolicyByServiceAndPolicyName("Sandbox_hadoop", "lake_test")
    print(rangerApi)

    result = rangerApi.deleteDeletePolicyByServiceAndPolicyName("Sandbox_hadoop", "lake_test")
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
    # testAmbari()
    testRanger()
