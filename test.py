#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ambari import AmbariApi

if __name__ == '__main__':
    ambariApi = AmbariApi("http", "127.0.0.1", "8080", "basic")
    ambariApi.setCredentialsBasic("admin", "hortonworks")

    result = ambariApi.getAdminViewVersion()
    print(ambariApi)

    result = ambariApi.getClusterName()
    print(ambariApi)
    ambariApi.setClusterName(result.json()["items"][0]["Clusters"]["cluster_name"])

    result = ambariApi.getClusterStatus()
    print(ambariApi)

    result = ambariApi.getClusterStaleConfig()
    print(ambariApi)

    result = ambariApi.getResourceManagerHosts()
    print(ambariApi)

    result = ambariApi.getQueuesFromAmbari()
    print(ambariApi)
