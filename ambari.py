#!/usr/bin/env python
# -*- coding: utf-8 -*-

from api import Api
import inspect
import json
import time

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
        self._clusterNameMask = self._config["clusterNameMask"]
        self._serviceNameMask = self._config["serviceNameMask"]
        self._requestIdMask = self._config["requestIdMask"]
        self._sleepingTimeInSeconds = self._config["sleepingTimeInSeconds"]
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
        generic post methode as it is always the same routine
        """
        self.setUrl(self._rootUrl + url)
        self.setMethode("post")
        self.setData(data)
        self.callApi()
        return self._r

    def _putGenericMethode(self, url, data):
        """
        generic put methode as it is always the same routine
        """
        self.setUrl(self._rootUrl + url)
        self.setMethode("put")
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

    def getRequests(self):
        """
        get all the requests
        """
        result = self._getGenericMethode(self._api[inspect.currentframe().f_code.co_name])
        return result

    def getRequestStatus(self, requestId):
        """
        get the status of a request
        """
        result = self._getGenericMethode(self._api[inspect.currentframe().f_code.co_name].replace(self._requestIdMask, str(requestId)))
        return result

    def getClusterName(self):
        """
        get the cluster name and call the setClusterName methode
        """
        result = self._getGenericMethode(self._api[inspect.currentframe().f_code.co_name])
        self.setClusterName(result.json()["items"][0]["Clusters"]["cluster_name"])
        return result

    def getClusterServices(self):
        """
        get the cluster sercvice status
        """
        return self._getGenericMethode(self._api[inspect.currentframe().f_code.co_name])

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
        return self._postGenericMethode(self._api[inspect.currentframe().f_code.co_name], json.dumps(json.loads(data), indent=2))

    def postAllServicesCheck(self):
        """
        post all services check
        """
        returnArray = []
        result = self.getClusterServices()
        for item in result.json()["items"]:
            if(item["ServiceInfo"]["service_name"] == "ZOOKEEPER"):
                itemResult = self.postServiceCheck(item["ServiceInfo"]["service_name"] + "_QUORUM")
            else:
                itemResult = self.postServiceCheck(item["ServiceInfo"]["service_name"])
            try:
                json_object = itemResult.json()
            except ValueError, e:
                pass
            else:
                if("Requests" in itemResult.json()):
                    returnArray.append(itemResult.json()["Requests"]["id"])
        return returnArray

    def putClusterServiceStart(self, serviceName):
        """
        put a start for a service
        """
        data = '{"RequestInfo": {"context" :"Start ' + serviceName + ' via REST"}, "Body": {"ServiceInfo": {"state": "STARTED"}}}'
        return self._putGenericMethode(self._api[inspect.currentframe().f_code.co_name].replace(self._serviceNameMask, serviceName), json.dumps(json.loads(data), indent=2))

    def putClusterServiceStop(self, serviceName):
        """
        put a stop for a service
        """
        data = '{"RequestInfo": {"context" :"Stop ' + serviceName + ' via REST"}, "Body": {"ServiceInfo": {"state": "INSTALLED"}}}'
        return self._putGenericMethode(self._api[inspect.currentframe().f_code.co_name].replace(self._serviceNameMask, serviceName), json.dumps(json.loads(data), indent=2))

    def putClusterServiceStartAll(self):
        """
        put a start for all services
        retrun an array of requestsId
        """
        returnArray = []
        result = self.getClusterServices()
        for item in result.json()["items"]:
            itemResult = self.putClusterServiceStart(item["ServiceInfo"]["service_name"])
            try:
                json_object = itemResult.json()
            except ValueError, e:
                pass
            else:
                if("Requests" in itemResult.json()):
                    returnArray.append(itemResult.json()["Requests"]["id"])
        return returnArray

    def putClusterServiceStopAll(self):
        """
        put a stop for all services
        retrun an array of requestsId
        """
        returnArray = []
        result = self.getClusterServices()
        for item in result.json()["items"]:
            print("Stopping " + item["ServiceInfo"]["service_name"])
            itemResult = self.putClusterServiceStop(item["ServiceInfo"]["service_name"])
            try:
                json_object = itemResult.json()
            except ValueError, e:
                pass
            else:
                if("Requests" in itemResult.json()):
                    returnArray.append(itemResult.json()["Requests"]["id"])
        return returnArray

    def waitUntilRequestsCompleted(self, requestId):
        """
        Will wait until all the requests are completed
        """
        requestsArray = []
        requestsCompletedArray = []
        if(type(requestId) == int):
            requestsArray.append(requestId)
        else:
            requestsArray = requestId
        while(len(requestsArray)):
            for reqId in requestsArray:
                result = self.getRequestStatus(reqId)
                try:
                    json_object = result.json()
                except ValueError, e:
                    pass
                else:
                    if("tasks" in result.json()):
                        taskComplete = True
                        for item in result.json()["tasks"]:
                            if(item["Tasks"]["status"] != "COMPLETED"):
                                taskComplete = False
                        if(taskComplete):
                            requestsCompletedArray.append(reqId)
                            print("Task : " + str(reqId) + " (" + item["Tasks"]["command_detail"] + ") for " + item["Tasks"]["role"] + " Completed")
                        else:
                            print("Task : " + str(reqId) + " (" + item["Tasks"]["command_detail"] + ") for " + item["Tasks"]["role"] + " NOT Completed")
            for reqId in requestsCompletedArray:
                requestsArray.remove(reqId)
            requestsCompletedArray = []
            if(len(requestsArray)):
                time.sleep(self._sleepingTimeInSeconds)
            print("Waiting tasks to complete...")
        print("All tasks completed.")

    def putAbortStuckRequest(self, requestId):
        """
        put a request abort for a stuck request
        """
        data = '{"Requests":{"request_status":"ABORTED","abort_reason":"Aborted by user"}}'
        result = self._putGenericMethode(self._api[inspect.currentframe().f_code.co_name].replace(self._requestIdMask, str(requestId)), json.dumps(json.loads(data), indent=2))
        return result
