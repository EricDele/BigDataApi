#!/usr/bin/env python
# -*- coding: utf-8 -*-

from api import Api
import inspect
import json
from collections import defaultdict

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
        with open("module_utils/ranger_api.json") as jsonFile:
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

    # API for Users and groups management

    def getUsers(self):
        """
        get the users
        """
        self.setHeaders({"Content-Type": "application/json", "Accept": "application/json"})
        result = self._callGenericMethode("get", self._api[inspect.currentframe().f_code.co_name])
        return self._r

    def getUser(self, userNameOrId):
        """
        get an user by Name or Id
        """
        if(type(userNameOrId) is str):
            url = self.renderUrl(self._api[inspect.currentframe().f_code.co_name + "ByName"], userName = userNameOrId)
        else:
            url = self.renderUrl(self._api[inspect.currentframe().f_code.co_name + "ById"], userId = str(userNameOrId))
        self.setHeaders({"Content-Type": "application/json", "Accept": "application/json"})
        result = self._callGenericMethode("get", url)
        return self._r

    def getGroups(self):
        """
        get the groups
        """
        self.setHeaders({"Content-Type": "application/json", "Accept": "application/json"})
        result = self._callGenericMethode("get", self._api[inspect.currentframe().f_code.co_name])
        return self._r

    def getGroup(self, groupNameOrId):
        """
        get the group by Name or Id
        """
        if(type(groupNameOrId) is str):
            url = self.renderUrl(self._api[inspect.currentframe().f_code.co_name + "ByName"], groupName = groupNameOrId)
        else:
            url = self.renderUrl(self._api[inspect.currentframe().f_code.co_name + "ById"], groupId = str(groupNameOrId))
        self.setHeaders({"Content-Type": "application/json", "Accept": "application/json"})
        result = self._callGenericMethode("get", url)
        return self._r

    def setRoleForUser(self, userNameOrId, role="ROLE_USER"):
        """
        Set a user with an admin role
        Mandatory values :
              "id", "name", "description","userRoleList": ["ROLE_SYS_ADMIN" OR "ROLE_USER"]
        """
        if(role.upper() not in ["ROLE_USER", "ROLE_SYS_ADMIN"]):
            raise RangerApiError("Role for user should be one of ROLE_USER or ROLE_SYS_ADMIN")
        data = defaultdict(dict)
        # Get the current infos from the user to grab mandatory fields
        userInfos = self.getUser(userNameOrId).json()
        data["id"] = userInfos["vXUsers"][0]["id"]
        data["name"] = userInfos["vXUsers"][0]["name"]
        data["description"] = userInfos["vXUsers"][0]["description"]
        data["firstName"] = userInfos["vXUsers"][0]["firstName"]
        data["lastName"] = userInfos["vXUsers"][0]["lastName"]
        data["userRoleList"] = [role.upper()]
        self.setHeaders({"Content-Type": "application/json", "Accept": "application/json"})
        url = self.renderUrl(self._api[inspect.currentframe().f_code.co_name], id = str(data["id"]))
        result = self._callGenericMethode("put", url, json.dumps(data))
        return self._r

    def createUser(self, userName, firstName, lastName, emailAddress, description, password, groupIdList=[], userRoleList=[]):
        """
        create an internal user
        MAndatory values :
            "name","firstName","lastName","emailAddress","description","password","groupIdList","userRoleList"
        """
        data = defaultdict(dict)
        data["name"] = userName
        data["firstName"] = firstName
        data["lastName"] = lastName
        data["emailAddress"] = emailAddress
        data["description"] = description
        data["password"] = password
        data["groupIdList"] = groupIdList
        data["userRoleList"] = userRoleList
        self.setHeaders({"Content-Type": "application/json", "Accept": "application/json"})
        url = self._api[inspect.currentframe().f_code.co_name]
        result = self._callGenericMethode("post", url, json.dumps(data))
        return self._r

    def deleteUser(self, userNameOrId):
        """
        delete a user
        """
        # Get the current infos from the user to grab mandatory fields
        userInfos = self.getUser(userNameOrId).json()
        self.setHeaders({"Content-Type": "application/json", "Accept": "application/json"})
        url = self.renderUrl(self._api[inspect.currentframe().f_code.co_name], id = str(userInfos["vXUsers"][0]["id"]))
        result = self._callGenericMethode("delete", url)
        return self._r

    # API V2 ##################################

    def getService(self, serviceNameOrId):
        """
        get a service by Name or Id
        """
        if(type(serviceNameOrId) is str):
            return self._callGenericMethode("get", self.renderUrl(self._api[inspect.currentframe().f_code.co_name + "ByName"], serviceName = serviceNameOrId ))
        else:
            return self._callGenericMethode("get", self.renderUrl(self._api[inspect.currentframe().f_code.co_name + "ById"], serviceId = str(serviceNameOrId) ))

    def getServices(self, serviceType=""):
        """
        get the services

        serviceType string The service types(such as "hdfs","hive","hbase","knox","storm", "atlas")
        """
        return self._callGenericMethode("get", self.renderUrl(self._api[inspect.currentframe().f_code.co_name], serviceType = serviceType))

    def getPolicyByServiceAndPolicyName(self, serviceName, policyName):
        """
        get a policy by Service and Policy Name
        """        
        return self._callGenericMethode("get", self.renderUrl(self._api[inspect.currentframe().f_code.co_name], policyName = policyName, serviceName = serviceName))

    def getSearchPolicyInService(self, serviceName, policyName=""):
        """
        get a search on policy in a service
        """
        return self._callGenericMethode("get", self.renderUrl(self._api[inspect.currentframe().f_code.co_name], policyName = policyName, serviceName = serviceName))

    def postCreatePolicy(self, **kwargs):
        """
        post to create a policy
        https://cwiki.apache.org/confluence/display/RANGER/Apache+Ranger+0.6+-+REST+APIs+for+Service+Definition%2C+Service+and+Policy+Management#ApacheRanger0.6-RESTAPIsforServiceDefinition,ServiceandPolicyManagement-CreatePolicy
        Arguments :
            policyTemplateType = one of ["hdfs", "yarn", "hbase", "hive", "knox", "storm", "solr", "kafka", "nifi", "atlas"] 
            serviceName = Name of the service
            policyName = Name of the policy
            description = description
            isRecursive = Is policy recursive
            users = Array of users
            groups = Array of groups
            resources = Resource affected by the policy ex :'["/lake/test"]', PolicyTemplateType dependent
            accesses = Permissions poistionned on the resource, PolicyTemplateType dependent
        """
        self.setHeaders({"Content-Type": "application/json", "Accept": "application/json"})
        return self._callGenericMethode("post", self._api[inspect.currentframe().f_code.co_name], self.renderData("general_policy.json.j2", **kwargs))

    def postApplyPolicy(self, **kwargs):
        """
        post to update or create a policy
        https://cwiki.apache.org/confluence/display/RANGER/Apache+Ranger+0.6+-+REST+APIs+for+Service+Definition%2C+Service+and+Policy+Management#ApacheRanger0.6-RESTAPIsforServiceDefinition,ServiceandPolicyManagement-ApplyPolicy
        This request should not remove permissions, only add more permissions or create new ones
        """
        self.setHeaders({"Content-Type": "application/json", "Accept": "application/json"})
        return self._callGenericMethode("post", self._api[inspect.currentframe().f_code.co_name], self.renderData("general_policy.json.j2", **kwargs))

    def putUpdatePolicyByServiceAndPolicyName(self, **kwargs):
        """
        post to update or create a policy
        https://cwiki.apache.org/confluence/display/RANGER/Apache+Ranger+0.6+-+REST+APIs+for+Service+Definition%2C+Service+and+Policy+Management#ApacheRanger0.6-RESTAPIsforServiceDefinition,ServiceandPolicyManagement-UpdatePolicybyservice-nameandpolicy-name
        This request should remove permissions
        """
        self.setHeaders({"Content-Type": "application/json", "Accept": "application/json"})
        return self._callGenericMethode("put", self.renderUrl(self._api[inspect.currentframe().f_code.co_name], policyName = kwargs['policyName'], serviceName = kwargs['serviceName']), self.renderData("general_policy.json.j2", **kwargs))

    def deleteDeletePolicyByServiceAndPolicyName(self, serviceName="", policyName=""):
        """
        Delete a policy by its name and service
        https://cwiki.apache.org/confluence/display/RANGER/Apache+Ranger+0.6+-+REST+APIs+for+Service+Definition%2C+Service+and+Policy+Management#ApacheRanger0.6-RESTAPIsforServiceDefinition,ServiceandPolicyManagement-Deletepolicybyservice-nameandpolicy-name
        """
        if(serviceName == "" or policyName == ""):
            raise RangerApiError("For deleting a policy you have to set the serviceName and policyName")
        else:
            return self._callGenericMethode("delete", self.renderUrl(self._api[inspect.currentframe().f_code.co_name], policyName = policyName, serviceName = serviceName))
