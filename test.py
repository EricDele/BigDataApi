#!/usr/bin/env python
# -*- coding: utf-8 -*-

from module_utils.ambari import AmbariApi
from module_utils.ranger import RangerApi
import json


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

    result = rangerApi.getPolicyByServiceAndPolicyName("Sandbox_hadoop", "all - path")
    print(rangerApi)

    result = rangerApi.getPolicyByServiceAndPolicyName("Sandbox_hadoop", "HDFS Global Allow")
    print(rangerApi)

    result = rangerApi.getPolicyByServiceAndPolicyName("Sandbox_yarn", "all - queue")
    print(rangerApi)

    result = rangerApi.getPolicyByServiceAndPolicyName("Sandbox_hive", "all - database, table, column")
    print(rangerApi)

    result = rangerApi.getSearchPolicyInService("Sandbox_hbase", "all - table, column-family, column")
    print(rangerApi)

    result = rangerApi.getSearchPolicyInService("Sandbox_knox", "all - topology, service")
    print(rangerApi)

    result = rangerApi.getSearchPolicyInService("Sandbox_kafka", "all - topic")
    print(rangerApi)

    ## Create User for policies
    result = rangerApi.createUser("it1", "it1", "it1", "it1", "it1", "it1it1it1", [2], ["ROLE_USER"])
    print(rangerApi)

    ## HDFS Policies
    result = rangerApi.postCreatePolicy(policyTemplateType = "hdfs", serviceName = "Sandbox_hadoop", policyName = "lake_test", description = "policy for the lake test",
                                        resources = ["/lake/test","/lake/project"], isRecursive = False, users = ["it1"], groups = [], accesses = "r--")
    print(rangerApi)

    result = rangerApi.postApplyPolicy(policyTemplateType = "hdfs", serviceName = "Sandbox_hadoop", policyName = "lake_test", description = "policy for the lake test",
                                       resources = ["/lake/test","/lake/project"], isRecursive = False, users = ["it1"], groups = [], accesses = "r-x")
    print(rangerApi)

    result = rangerApi.putUpdatePolicyByServiceAndPolicyName(policyTemplateType = "hdfs", serviceName = "Sandbox_hadoop", policyName = "lake_test", description = "policy for the lake test",
                                                             resources = ["/lake/test","/lake/project"], isRecursive = False, users = ["it1"], groups = [], accesses = "rwx")
    print(rangerApi)

    result = rangerApi.getPolicyByServiceAndPolicyName("Sandbox_hadoop", "lake_test")
    print(rangerApi)

    result = rangerApi.deleteDeletePolicyByServiceAndPolicyName("Sandbox_hadoop", "lake_test")
    print(rangerApi)

    ## HBASE Policies
    result = rangerApi.postCreatePolicy(policyTemplateType = "hbase", serviceName = "Sandbox_hbase", policyName = "hbase_test", description = "policy for the hbase test",
                                        resources = {"column":{"isExcludes":"false","value":["*"]},"table":{"isExcludes":"false","value":["j*","d*"]},"column_family":{"isExcludes":"false","value":["*"]}}, users = ["it1"], groups = [],
                                        accesses = ["read","write","create","admin"])
    print(rangerApi)

    result = rangerApi.getPolicyByServiceAndPolicyName("Sandbox_hbase", "hbase_test")
    print(rangerApi)
    
    result = rangerApi.deleteDeletePolicyByServiceAndPolicyName("Sandbox_hbase", "hbase_test")
    print(rangerApi)

    ## HIVE Policies
    result = rangerApi.postCreatePolicy(policyTemplateType = "hive", serviceName = "Sandbox_hive", policyName = "hive_test", description = "policy for the hive test",
                                        resources = {"column":{"isExcludes":"false","value":["*"]},"table":{"isExcludes":"false","value":["j*","d*"]},"database":{"isExcludes":"false","value":["*"]}}, users = ["it1"], groups = [],
                                        accesses = ["select","update","create","drop","alter","index","lock","all","read","write"])
    print(rangerApi)

    result = rangerApi.getPolicyByServiceAndPolicyName("Sandbox_hive", "hive_test")
    print(rangerApi)
    
    result = rangerApi.deleteDeletePolicyByServiceAndPolicyName("Sandbox_hive", "hive_test")
    print(rangerApi)

    ## KAFKA Policies
    result = rangerApi.postCreatePolicy(policyTemplateType = "kafka", serviceName = "Sandbox_kafka", policyName = "kafka_test", description = "policy for the kafka test",
                                        resources = ["topicLakeTest","topicProjectTest"], isRecursive = False, users = ["it1"], groups = [],
                                        accesses = ["publish","consume","configure","describe","create","delete","kafka_admin"])
    print(rangerApi)

    result = rangerApi.getPolicyByServiceAndPolicyName("Sandbox_kafka", "kafka_test")
    print(rangerApi)
    
    result = rangerApi.deleteDeletePolicyByServiceAndPolicyName("Sandbox_kafka", "kafka_test")
    print(rangerApi)

    ## KNOX Policies
    result = rangerApi.postCreatePolicy(policyTemplateType = "knox", serviceName = "Sandbox_knox", policyName = "knox_test", description = "policy for the knox test",
                                        resources = {"service":{"isExcludes":"false","value":["*"]},"topology":{"isExcludes":"false","value":["j*","d*"]}}, users = ["it1"], groups = [],
                                        accesses = ["allow"])
    print(rangerApi)

    result = rangerApi.getPolicyByServiceAndPolicyName("Sandbox_knox", "knox_test")
    print(rangerApi)
    
    result = rangerApi.deleteDeletePolicyByServiceAndPolicyName("Sandbox_knox", "knox_test")
    print(rangerApi)

    ## YARN Policies
    result = rangerApi.postCreatePolicy(policyTemplateType = "yarn", serviceName = "Sandbox_yarn", policyName = "yarn_test", description = "policy for the yarn test",
                                        resources = ["default"], isRecursive = False, users = ["it1"], groups = [],
                                        accesses = ["submit-app","admin-queue"])
    print(rangerApi)

    result = rangerApi.getPolicyByServiceAndPolicyName("Sandbox_yarn", "yarn_test")
    print(rangerApi)
    
    result = rangerApi.deleteDeletePolicyByServiceAndPolicyName("Sandbox_yarn", "yarn_test")
    print(rangerApi)

    # API for Users and groups management

    # result = rangerApi.getUsers()
    # print(rangerApi)

    # result = rangerApi.createUser("user77", "user77", "user77", "user77", "user77", "user77", [2], ["ROLE_USER"])
    # print(rangerApi)

    # result = rangerApi.getUser("user77")
    # print(rangerApi)

    # result = rangerApi.setRoleForUser("user77", "ROLE_SYS_ADMIN")
    # print(rangerApi)

    # result = rangerApi.getUser("user77")
    # print(rangerApi)

    # result = rangerApi.deleteUser("user77")
    # print(rangerApi)

    # result = rangerApi.getUser("user77")
    # print(rangerApi)

    # result = rangerApi.getGroups()
    # print(rangerApi)

    # result = rangerApi.getGroup("admin")
    # print(rangerApi)

    # result = rangerApi.getGroup(12)
    # print(rangerApi)


if __name__ == '__main__':
    # testAmbari()
    testRanger()
