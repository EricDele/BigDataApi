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
        with open("ranger_api.json") as jsonFile:
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
            url = self._api[inspect.currentframe().f_code.co_name + "ByName"] + userNameOrId
        else:
            url = self._api[inspect.currentframe().f_code.co_name + "ById"] + str(userNameOrId)
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
            url = self._api[inspect.currentframe().f_code.co_name + "ByName"] + groupNameOrId
        else:
            url = self._api[inspect.currentframe().f_code.co_name + "ById"] + str(groupNameOrId)
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
        url = self._api[inspect.currentframe().f_code.co_name].replace('{id}', str(data["id"]))
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
        url = self._api[inspect.currentframe().f_code.co_name].replace('{id}', str(userInfos["vXUsers"][0]["id"])) + "?forceDelete=true"
        result = self._callGenericMethode("delete", url)
        return self._r


    # API V1 ##################################

    def getServices(self):
        """
        get the services
        """
        result = self._callGenericMethode("get", self._api[inspect.currentframe().f_code.co_name])
        return result

    def getService(self, serviceNameOrId):
        """
        get a service by Name or Id
        """
        if(type(serviceNameOrId) is str):
            url = self._api[inspect.currentframe().f_code.co_name + "ByName"] + serviceNameOrId
        else:
            url = self._api[inspect.currentframe().f_code.co_name + "ById"] + str(serviceNameOrId)
        result = self._callGenericMethode("get", url)
        return result

    def getPolicies(self):
        """
        get the policies
        """
        result = self._callGenericMethode("get", self._api[inspect.currentframe().f_code.co_name])
        return result

    def getPolicy(self, policyNameOrId):
        """
        get a policy by Name or Id
        """
        if(type(policyNameOrId) is str):
            url = self._api[inspect.currentframe().f_code.co_name + "ByName"] + policyNameOrId
        else:
            url = self._api[inspect.currentframe().f_code.co_name + "ById"] + str(policyNameOrId)
        result = self._callGenericMethode("get", url)
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
        result = self._callGenericMethode("get", self._api[inspect.currentframe().f_code.co_name] + urlSuffix)
        return result

    def getV2PolicyByServiceAndPolicyName(self, serviceName, policy):
        """
        get a policy by Service and Policy Name
        """
        url = self._api[inspect.currentframe().f_code.co_name].replace('{service-name}', serviceName).replace('{policy-name}', policy)
        result = self._callGenericMethode("get", url)
        return result

    def getV2SearchPolicyInService(self, serviceName, policyName=""):
        """
        get a search on policy in a service
        """
        if(policyName == ""):
            urlSuffix = ""
        else:
            urlSuffix = "?policyName=" + policyName
        url = self._api[inspect.currentframe().f_code.co_name].replace('{service-name}', serviceName) + urlSuffix
        result = self._callGenericMethode("get", url)
        return result

    def postV2CreatePolicy(self, serviceName, policyName, description, path=[], recursive=False, user="", group="", permissions="---"):
        """
        post to create a policy
        https://cwiki.apache.org/confluence/display/RANGER/Apache+Ranger+0.6+-+REST+APIs+for+Service+Definition%2C+Service+and+Policy+Management#ApacheRanger0.6-RESTAPIsforServiceDefinition,ServiceandPolicyManagement-CreatePolicy
        """
        data = defaultdict(dict)
        data["service"] = serviceName
        data["name"] = policyName
        data["description"] = description
        data["resources"] = {"path": {"values": path, "isRecursive": recursive}}
        data["policyItems"] = []
        item = defaultdict(dict)
        if(user != ""):
            item["users"] = [user]
        else:
            item["users"] = []
        if(group != ""):
            item["groups"] = [group]
        else:
            item["groups"] = []
        if(permissions == "r--"):
            item["accesses"] = [{"isAllowed": True, "type": "read"}]
        elif(permissions == "r-x"):
            item["accesses"] = [{"isAllowed": True, "type": "read"}, {"isAllowed": True, "type": "execute"}]
        elif(permissions == "rwx"):
            item["accesses"] = [{"isAllowed": True, "type": "read"}, {"isAllowed": True, "type": "write"}, {"isAllowed": True, "type": "execute"}]
        else:
            item["accesses"] = []
        data["policyItems"].append(item)
        self.setHeaders({"Content-Type": "application/json", "Accept": "application/json"})
        url = self._api[inspect.currentframe().f_code.co_name]
        result = self._callGenericMethode("post", url, json.dumps(data))
        return result

    def postV2ApplyPolicy(self, serviceName, policyName, description, path=[], recursive=False, user="", group="", permissions="---"):
        """
        post to update or create a policy
        https://cwiki.apache.org/confluence/display/RANGER/Apache+Ranger+0.6+-+REST+APIs+for+Service+Definition%2C+Service+and+Policy+Management#ApacheRanger0.6-RESTAPIsforServiceDefinition,ServiceandPolicyManagement-ApplyPolicy
        This request should not remove permissions, only add more permissions or create new ones
        """
        data = defaultdict(dict)
        data["service"] = serviceName
        data["name"] = policyName
        data["description"] = description
        data["resources"] = {"path": {"values": path, "isRecursive": recursive}}
        # data["policyType"] = 0
        data["policyItems"] = []
        item = defaultdict(dict)
        if(user != ""):
            item["users"] = [user]
        else:
            item["users"] = []
        if(group != ""):
            item["groups"] = [group]
        else:
            item["groups"] = []
        if(permissions == "r--"):
            item["accesses"] = [{"isAllowed": True, "type": "read"}]
        elif(permissions == "r-x"):
            item["accesses"] = [{"isAllowed": True, "type": "read"}, {"isAllowed": True, "type": "execute"}]
        elif(permissions == "rwx"):
            item["accesses"] = [{"isAllowed": True, "type": "read"}, {"isAllowed": True, "type": "write"}, {"isAllowed": True, "type": "execute"}]
        else:
            item["accesses"] = []
        data["policyItems"].append(item)
        self.setHeaders({"Content-Type": "application/json", "Accept": "application/json"})
        url = self._api[inspect.currentframe().f_code.co_name]
        result = self._callGenericMethode("post", url, json.dumps(data))
        return result

    def putV2UpdatePolicyByServiceAndPolicyName(self, serviceName, policyName, description, path=[], recursive=False, user="", group="", permissions="---"):
        """
        post to update or create a policy
        https://cwiki.apache.org/confluence/display/RANGER/Apache+Ranger+0.6+-+REST+APIs+for+Service+Definition%2C+Service+and+Policy+Management#ApacheRanger0.6-RESTAPIsforServiceDefinition,ServiceandPolicyManagement-UpdatePolicybyservice-nameandpolicy-name
        This request should remove permissions
        """
        data = defaultdict(dict)
        data["service"] = serviceName
        data["name"] = policyName
        data["description"] = description
        data["resources"] = {"path": {"values": path, "isRecursive": recursive}}
        # data["policyType"] = 0
        data["policyItems"] = []
        item = defaultdict(dict)
        if(user != ""):
            item["users"] = [user]
        else:
            item["users"] = []
        if(group != ""):
            item["groups"] = [group]
        else:
            item["groups"] = []
        if(permissions == "r--"):
            item["accesses"] = [{"isAllowed": True, "type": "read"}]
        elif(permissions == "r-x"):
            item["accesses"] = [{"isAllowed": True, "type": "read"}, {"isAllowed": True, "type": "execute"}]
        elif(permissions == "rwx"):
            item["accesses"] = [{"isAllowed": True, "type": "read"}, {"isAllowed": True, "type": "write"}, {"isAllowed": True, "type": "execute"}]
        else:
            item["accesses"] = []
        data["policyItems"].append(item)
        self.setHeaders({"Content-Type": "application/json", "Accept": "application/json"})
        url = self._api[inspect.currentframe().f_code.co_name].replace('{service-name}', serviceName).replace('{policy-name}', policyName)
        result = self._callGenericMethode("put", url, json.dumps(data))
        return result

    def deleteV2DeletePolicyByServiceAndPolicyName(self, serviceName="", policyName=""):
        """
        Delete a policy by its name and service
        https://cwiki.apache.org/confluence/display/RANGER/Apache+Ranger+0.6+-+REST+APIs+for+Service+Definition%2C+Service+and+Policy+Management#ApacheRanger0.6-RESTAPIsforServiceDefinition,ServiceandPolicyManagement-Deletepolicybyservice-nameandpolicy-name
        """
        if(serviceName == "" or policyName == ""):
            raise RangerApiError("For deleting a policy you have to set the serviceName and policyName")
        else:
            urlSuffix = "?servicename=" + serviceName + "&policyname=" + policyName
        result = self._callGenericMethode("delete", self._api[inspect.currentframe().f_code.co_name] + urlSuffix)
        return result
