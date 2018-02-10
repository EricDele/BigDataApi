# BigDataApi
A BigData Api library for managing Ambari and Ranger

## Goal of this project

This project is for giving an api to interact with the Hortonworks components and their API.

This is a python project that expose classes to use in your python scripts for symplifying the interaction with the components.

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
 |  setCredentialsKerberos(self, principal)
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
 |  getPolicies(self)
 |      get the policies
 |  
 |  getPolicy(self, policyNameOrId)
 |      get a policy by Name or Id
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
 |  getV2PolicyByServiceAndPolicyName(self, serviceName, policy)
 |      get a policy by Service and Policy Name
 |  
 |  getV2SearchPolicyInService(self, serviceName, policyName='')
 |      get a search on policy in a service
 |  
 |  getV2Services(self, serviceType='')
 |      get the services
 |      
 |      serviceType string The service types(such as "hdfs","hive","hbase","knox","storm", "atlas")
 |  
 |  postV2ApplyPolicy(self, serviceName, policyName, description, path=[], recursive=False, user='', group='', permissions='---')
 |      post to update or create a policy
 |      This request should not remove permissions, only add more permissions or create new ones
 |  
 |  postV2CreatePolicy(self, serviceName, policyName, description, path=[], recursive=False, user='', group='', permissions='---')
 |      post to create a policy
 |  
 |  putV2UpdatePolicyByServiceAndPolicyName(self, serviceName, policyName, description, path=[], recursive=False, user='', group='', permissions='---')
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
 |  getClusterStaleConfig(self)
 |      get the cluster service having stale config
 |  
 |  getClusterStatus(self)
 |      get the cluster sercvice status
 |  
 |  getQueuesFromAmbari(self)
 |      get the capacity scheduler queues from Ambari
 |  
 |  getResourceManagerHosts(self)
 |      get the cluster resource manager hosts
 |  
 |  postServiceCheck(self, serviceName)
 |      post a service check
 |  
 |  setClusterName(self, clusterName)
 |      set the cluster name and update the api path replaicng the mask by the real name
 |  
```
### How to use it

For testing see the *test.py* file with many examples.