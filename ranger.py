#!/usr/bin/env python
# -*- coding: utf-8 -*-

from api import Api
import inspect
import json
import xml.dom.minidom


class RangerApiError(Exception):
    """
    Exception for API call.
    """
    def __init__(self, value, cause=None):
        if(cause is None):
            cause = "An error occured in RangerApi class with {}".format(value)
        super(RangerApiError, self).__init__(cause)
        self.value = value

    def __str__(self):
        return self.value


class RangerApi(Api):
    """
    Ranger Api Class for managing Ranger
    """

    def __init__(self, protocol="http", hostname="", port="", authenticationMethode="basic"):
        Api.__init__(self)
        self._protocol = protocol.lower()
        self._hostname = hostname
        self._port = port
        self._rootUrl = self._protocol + "://" + self._hostname + ":" + self._port
        self.setAuthenticationMethode(authenticationMethode)
        # Loading configuration file with all the api
        with open("ranger_api.json") as jsonFile:
            self._config = json.load(jsonFile)
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

    # API for Users and groups management return an XML object

    def getUsers(self):
        """
        get the users
        """
        result = self._getGenericMethode(self._api[inspect.currentframe().f_code.co_name])
        return xml.dom.minidom.parseString(self._r.text).toprettyxml()

    def getUser(self, user):
        """
        get an user by Name or Id
        """
        if(type(user) is str):
            url = self._api[inspect.currentframe().f_code.co_name + "ByName"] + user
        else:
            url = self._api[inspect.currentframe().f_code.co_name + "ById"] + str(user)
        result = self._getGenericMethode(url)

        return xml.dom.minidom.parseString(self._r.text).toprettyxml()

    def getGroups(self):
        """
        get the groups
        """
        result = self._getGenericMethode(self._api[inspect.currentframe().f_code.co_name])
        return xml.dom.minidom.parseString(self._r.text).toprettyxml()

    def getGroup(self, group):
        """
        get the group by Name or Id
        """
        if(type(group) is str):
            url = self._api[inspect.currentframe().f_code.co_name + "ByName"] + group
        else:
            url = self._api[inspect.currentframe().f_code.co_name + "ById"] + str(group)
        result = self._getGenericMethode(url)
        return xml.dom.minidom.parseString(self._r.text).toprettyxml()

    # API V1 ##################################

    def getServices(self):
        """
        get the services
        """
        result = self._getGenericMethode(self._api[inspect.currentframe().f_code.co_name])
        return result

    def getService(self, service):
        """
        get a service by Name or Id
        """
        if(type(service) is str):
            url = self._api[inspect.currentframe().f_code.co_name + "ByName"] + service
        else:
            url = self._api[inspect.currentframe().f_code.co_name + "ById"] + str(service)
        result = self._getGenericMethode(url)
        return result

    def getPolicies(self):
        """
        get the policies
        """
        result = self._getGenericMethode(self._api[inspect.currentframe().f_code.co_name])
        return result

    def getPolicy(self, policy):
        """
        get a policy by Name or Id
        """
        if(type(policy) is str):
            url = self._api[inspect.currentframe().f_code.co_name + "ByName"] + policy
        else:
            url = self._api[inspect.currentframe().f_code.co_name + "ById"] + str(policy)
        result = self._getGenericMethode(url)
        return result

    # API V2 ##################################

    def getV2Services(self, serviceType=""):
        """
        get the services

        serviceType string The service types(such as "hdfs","hive","hbase","knox","storm", "atlas")
        """
        if(serviceType == ""):
            urlSuffix = ""
        else:
            urlSuffix = "?serviceType=" + serviceType
        result = self._getGenericMethode(self._api[inspect.currentframe().f_code.co_name] + urlSuffix)
        return result

    def getV2PolicyByServiceAndPolicyName(self, service, policy):
        """
        get a policy by Service and Policy Name
        """
        url = self._api[inspect.currentframe().f_code.co_name].replace('{service-name}', service).replace('{policy-name}', policy)
        result = self._getGenericMethode(url)
        return result

    def getV2SearchPolicyInService(self, service, policy=""):
        """
        get a search on policy in a service
        """
        if(policy == ""):
            urlSuffix = ""
        else:
            urlSuffix = "?policyName=" + policy
        url = self._api[inspect.currentframe().f_code.co_name].replace('{service-name}', service) + urlSuffix
        result = self._getGenericMethode(url)
        return result
