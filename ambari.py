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
    Ambari Api Class for managing Ambri
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
        self.setUrl(self._rootUrl + url)
        self.setMethode("get")
        self.callApi()
        return self._r

    def getAdminViewVersion(self):
        return self._getGenericMethode(self._api[inspect.currentframe().f_code.co_name])

    def getClusterName(self):
        return self._getGenericMethode(self._api[inspect.currentframe().f_code.co_name])

    def getClusterStatus(self):
        return self._getGenericMethode(self._api[inspect.currentframe().f_code.co_name])

    def getClusterStaleConfig(self):
        return self._getGenericMethode(self._api[inspect.currentframe().f_code.co_name])

    def getResourceManagerHosts(self):
        return self._getGenericMethode(self._api[inspect.currentframe().f_code.co_name])

    def getQueuesFromAmbari(self):
        return self._getGenericMethode(self._api[inspect.currentframe().f_code.co_name])

    def setClusterName(self, clusterName):
        self._clusterName = clusterName
        # Replace the clustername mask by the real name of the cluster
        for apiName in self._api:
            self._api[apiName] = self._api[apiName].replace(self._clusterNameMask, self._clusterName)
