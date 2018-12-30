# BigDataApi
A BigData Api library for managing Ambari and Ranger

- [BigDataApi](#bigdataapi)
  - [Goal of this project](#goal-of-this-project)
  - [Imports required](#imports-required)
  - [Classes Tree](#classes-tree)
  - [Api](#api)
  - [Ranger](#ranger)
  - [Ambari](#ambari)
    - [How to use it](#how-to-use-it)

## Goal of this project

This project is for giving an api to interact with the Hortonworks components and their API.

This is a python project that expose classes to use in your python scripts for symplifying the interaction with the components.

## Imports required

- inspect
- json
- time
- jinja2
- requests
- collections

## Classes Tree

This is how the Classes are organized

```
|-- Api
    |-- Ranger
    |-- Ambari
```

## Api
```
class Api(__builtin__.object)
 |  Api Class to be used by other class for calling API
 |  
 |  Methods defined here:
 |  
 |  __init__(self)
 |  
 |  __str__(self)
 |  
 |  callApi(self)
 |  
 |  checkReturnCode(self)
 |      Check the HTTP response code, see https://fr.wikipedia.org/wiki/Liste_des_codes_HTTP
 |  
 |  setAuthenticationMethode(self, authenticationMethode)
 |  
 |  setCompleteUrl(self, url, methode, authenticationMethode, headers, data)
 |  
 |  setCredentialsBasic(self, user, password)
 |  
 |  setData(self, data)
 |  
 |  setHeaders(self, headers)
 |  
 |  setMethode(self, methode)
 |  
 |  setUrl(self, url)
 |  

```
## Ranger

```
class RangerApi(api.Api)
 |  Ranger Api Class for managing Ranger
 |  
 |  Method resolution order:
 |      RangerApi
 |      api.Api
 |      __builtin__.object
 |  
 |  Methods defined here:
 |  
 |  __init__(self, protocol='http', hostname='', port='', authenticationMethode='basic')
 |  
 |  __str__(self)
 |  
 |  createUser(self, userName, firstName, lastName, emailAddress, description, password, groupIdLi
st=[], userRoleList=[])
 |      create an internal user
 |      MAndatory values :
 |          "name","firstName","lastName","emailAddress","description","password","groupIdList","u
serRoleList"
 |  
 |  deleteUser(self, userNameOrId)
 |      delete a user
 |  
 |  deleteV2DeletePolicyByServiceAndPolicyName(self, serviceName='', policyName='')
 |      Delete a policy by its name and service
 |  
 |  getGroup(self, groupNameOrId)
 |      get the group by Name or Id
 |  
 |  getGroups(self)
 |      get the groups
 |  
 |  getService(self, serviceNameOrId)
 |      get a service by Name or Id
 |  
 |  getServices(self)
 |      get the services
 |  
 |  getUser(self, userNameOrId)
 |      get an user by Name or Id
 |  
 |  getUsers(self)
 |      get the users
 |  
 |  getPolicyByServiceAndPolicyName(self, serviceName, policy)
 |      get a policy by Service and Policy Name
 |  
 |  getSearchPolicyInService(self, serviceName, policyName='')
 |      get a search on policy in a service
 |  
 |  getServices(self, serviceType='')
 |      get the services
 |      
 |      serviceType string The service types(such as "hdfs","hive","hbase","knox","storm", "atlas")
 |  
 |  postApplyPolicy(self, serviceName, policyName, description, path=[], recursive=False, user='', group='', permissions='---')
 |      post to update or create a policy
 |      This request should not remove permissions, only add more permissions or create new ones
 |  
 |  postCreatePolicy(self, serviceName, policyName, description, path=[], recursive=False, user='', group='', permissions='---')
 |      post to create a policy
 |  
 |  putUpdatePolicyByServiceAndPolicyName(self, serviceName, policyName, description, path=[], recursive=False, user='', group='', permissions='---')
 |      post to update or create a policy
 |      This request should remove permissions
 |  
 |  setRoleForUser(self, userNameOrId, role='ROLE_USER')
 |      Set a user with an admin role
 |      Mandatory values :
 |            "id", "name", "description","userRoleList": ["ROLE_SYS_ADMIN" OR "ROLE_USER"]
 |  

```

## Ambari
```
class AmbariApi(api.Api)
 |  Ambari Api Class for managing Ambari
 |  
 |  Method resolution order:
 |      AmbariApi
 |      api.Api
 |      __builtin__.object
 |  
 |  Methods defined here:
 |  
 |  __init__(self, protocol='http', hostname='', port='', authenticationMethode='basic')
 |  
 |  __str__(self)
 |  
 |  getAdminViewVersion(self)
 |      get the Admin View Version and set the corresponding headers
 |  
 |  getClusterName(self)
 |      get the cluster name and call the setClusterName methode
 |  
 |  getClusterServices(self)
 |      get the cluster sercvice status
 |  
 |  getClusterStaleConfig(self)
 |      get the cluster service having stale config
 |  
 |  getClusterStatus(self)
 |      get the cluster sercvice status
 |  
 |  getQueuesFromAmbari(self)
 |      get the capacity scheduler queues from Ambari
 |  
 |  getRequestStatus(self, requestId)
 |      get the status of a request
 |  
 |  getRequests(self)
 |      get all the requests
 |  
 |  getResourceManagerHosts(self)
 |      get the cluster resource manager hosts
 |  
 |  postAllServicesCheck(self)
 |      post all services check
 |  
 |  putAbortStuckRequest(self, requestId)
 |      put a request abort for a stuck request
 |  
 |  putClusterServiceStart(self, serviceName)
 |      put a start for a service
 |  
 |  putClusterServiceStartAll(self)
 |      put a start for all services
 |      retrun an array of requestsId
 |  
 |  putClusterServiceStop(self, serviceName)
 |      put a stop for a service
 |  
 |  putClusterServiceStopAll(self)
 |      put a stop for all services
 |      retrun an array of requestsId
 |  
 |  setClusterName(self, clusterName)
 |      set the cluster name and update the api path replaicng the mask by the real name
 |  
 |  waitUntilRequestsCompleted(self, requestId)
 |      Will wait until all the requests are completed
 |  

```
### How to use it

For testing see the *test.py* file with many examples.