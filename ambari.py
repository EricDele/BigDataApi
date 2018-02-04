#!/usr/bin/env python
# -*- coding: utf-8 -*-

from api import Api
import inspect
import json


class AmbariApiError(Exception):
    """
    Exception for API call.
    """
    def __init__(self, value, cause=None):
        if(cause is None):
            cause = "An error occured in AmbariApi class with {}".format(value)
        super(AmbariApiError, self).__init__(cause)
        self.value = value

    def __str__(self):
        return self.value


class AmbariApi(Api):
    """
    Ambari Api Class for managing Ambari
    """

    def __init__(self, protocol="http", hostname="", port="", authenticationMethode="basic"):
        Api.__init__(self)
        self._protocol = protocol.lower()
        self._hostname = hostname
        self._port = port
        self._rootUrl = self._protocol + "://" + self._hostname + ":" + self._port
        self.setAuthenticationMethode(authenticationMethode)
        # Loading configuration file with all the api
        with open("ambari_api.json") as jsonFile:
            self._config = json.load(jsonFile)
        self._clusterNameMask = self._config["yourClusterName"]
        self._api = self._config["api"]

    def __str__(self):
        return Api.__str__(self)

    def _getGenericMethode(self, url):
        """
        generic get methode as it is always the same routine
        """
        self.setUrl(self._rootUrl + url)
        self.setMethode("get")
        self.callApi()
        return self._r

    def _postGenericMethode(self, url, data):
        """
        generic get methode as it is always the same routine
        """
        self.setUrl(self._rootUrl + url)
        self.setMethode("post")
        self.setData(data)
        self.callApi()
        return self._r

    def getAdminViewVersion(self):
        """
        get the Admin View Version and set the corresponding headers
        """
        result = self._getGenericMethode(self._api[inspect.currentframe().f_code.co_name])
        versionDigits = result.json()["versions"][0]["ViewVersionInfo"]["version"].split('.')
        self._headers = self._config["headers-by-version"]['.'.join([versionDigits[0], versionDigits[1]])]
        return result

    def getClusterName(self):
        """
        get the cluster name and call the setClusterName methode
        """
        result = self._getGenericMethode(self._api[inspect.currentframe().f_code.co_name])
        self.setClusterName(result.json()["items"][0]["Clusters"]["cluster_name"])
        return result

    def getClusterStatus(self):
        """
        get the cluster sercvice status
        """
        return self._getGenericMethode(self._api[inspect.currentframe().f_code.co_name])

    def getClusterStaleConfig(self):
        """
        get the cluster service having stale config
        """
        return self._getGenericMethode(self._api[inspect.currentframe().f_code.co_name])

    def getResourceManagerHosts(self):
        """
        get the cluster resource manager hosts
        """
        return self._getGenericMethode(self._api[inspect.currentframe().f_code.co_name])

    def getQueuesFromAmbari(self):
        """
        get the capacity scheduler queues from Ambari
        """
        return self._getGenericMethode(self._api[inspect.currentframe().f_code.co_name])

    def setClusterName(self, clusterName):
        """
        set the cluster name and update the api path replaicng the mask by the real name
        """
        self._clusterName = clusterName
        # Replace the clustername mask by the real name of the cluster
        for apiName in self._api:
            self._api[apiName] = self._api[apiName].replace(self._clusterNameMask, self._clusterName)

    def postServiceCheck(self, serviceName):
        """
        post a service check
        """
        data = '{"RequestInfo":{"context":"' + serviceName + ' Service Check","command":"' + serviceName + '_SERVICE_CHECK"},"Requests/resource_filters":[{"service_name":"' + serviceName + '"}]}'
        print(json.dumps(json.loads(data), indent=2))
        return self._postGenericMethode(self._api[inspect.currentframe().f_code.co_name], json.dumps(json.loads(data), indent=2))
