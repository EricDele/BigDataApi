#!/usr/bin/env python
# -*- coding: utf-8 -*-

from api import Api
import inspect
import json

class AmbariMetricsApiError(Exception):
    """
    Exception for API call.
    """
    def __init__(self, value, cause=None):
        if(cause is None):
            cause = "An error occured in AmbariMetricsApi class with {}".format(value)
        super(AmbariMetricsApiError, self).__init__(cause)
        self.value = value

    def __str__(self):
        return self.value


class AmbariMetricsApi(Api):
    """
    AmbariMetrics Api Class for managing AmbariMetrics
    """

    def __init__(self, protocol="http", hostname="", port="", authenticationMethode="basic"):
        Api.__init__(self)
        self._protocol = protocol.lower()
        self._hostname = hostname
        self._port = port
        self._rootUrl = self._protocol + "://" + self._hostname + ":" + self._port
        self.setAuthenticationMethode(authenticationMethode)
        # Loading configuration file with all the api
        with open("module_utils/ambari_metrics_api.json") as jsonFile:
            self._config = json.load(jsonFile)
        self._api = self._config["api"]

    def __str__(self):
        return Api.__str__(self)

    def _callGenericMethode(self, methode, url, data=""):
        """
        generic methode as it is always the same routine
        """
        self.setUrl(self._rootUrl + url)
        self.setMethode(methode)
        if(data != ""):
            self.setData(data)
        self.callApi()
        return self._r

    def getMetrics(self, **kwargs):
        """
        get Metrics
        """
        return self._callGenericMethode("get", self.renderUrl(self._api[inspect.currentframe().f_code.co_name], **kwargs))
    
    def postMetrics(self, **kwargs):
        """
        put Metrics
        """
        self.setHeaders({"Content-Type": "application/json", "Accept": "application/json"})
        return self._callGenericMethode("post", self._api[inspect.currentframe().f_code.co_name], self.renderData("ambari_metrics_data.json.j2", **kwargs))