# BigDataApi
A BigData Api library for managing Ambari and Ranger

- [BigDataApi](#bigdataapi)
  - [Goal of this project](#goal-of-this-project)
  - [Imports required](#imports-required)
  - [How to use it in python mode](#how-to-use-it-in-python-mode)
    - [Initiate an object](#initiate-an-object)
      - [Ambari](#ambari)
      - [Ranger](#ranger)
    - [Ranger Policies creation](#ranger-policies-creation)
      - [Hdfs](#hdfs)
      - [Hbase](#hbase)
      - [Hive](#hive)
      - [Kafka](#kafka)
      - [Knox](#knox)
      - [Yarn](#yarn)
  - [How to use it in Ansible mode](#how-to-use-it-in-ansible-mode)
    - [Ranger_policy Ansible module](#rangerpolicy-ansible-module)
      - [Ranger_policy examples](#rangerpolicy-examples)
  - [Classes Tree](#classes-tree)
  - [Api](#api)
  - [Ranger](#ranger-1)
  - [Ambari](#ambari-1)
  - [Author](#author)
  - [LICENSE](#license)

## Goal of this project

This project is for giving an api to interact with the Hortonworks components and their API.

This is a python project that expose classes to use in your python scripts for symplifying the interaction with the components.

You can use it like an Ansible module too

## Imports required

- inspect
- json
- time
- jinja2
- requests
- collections

## How to use it in python mode

For testing see the [test.py](./test.py) file with many examples.

### Initiate an object

#### Ambari 

```Python
ambariApi = AmbariApi("http", "127.0.0.1", "8080", "basic")
ambariApi.setCredentialsBasic("admin", "hortonworks")
result = ambariApi.getClusterName() # Get the cluster name
print(ambariApi) # Will show you the result
help(ambariApi) # Will show you the class methods
```

#### Ranger

```Python
rangerApi = RangerApi("http", "127.0.0.1", "6080", "basic")
rangerApi.setCredentialsBasic("raj_ops", "raj_ops")
result = rangerApi.getServices() # Get all the configured Services
print(rangerApi) # Will show you the result
help(rangerApi) # Will show you the class methods
```

### Ranger Policies creation

#### Hdfs

```Python
rangerApi.postApplyPolicy(policyTemplateType = "hdfs", serviceName = "Sandbox_hadoop", 
                          policyName = "lake_test", description = "policy for the lake test",
                          resources = ["/lake/test","/lake/project"], isRecursive = False, 
                          users = ["it1"], groups = [], 
                          accesses = "r-x")
```

#### Hbase

```Python
rangerApi.postCreatePolicy(policyTemplateType = "hbase", serviceName = "Sandbox_hbase", 
                          policyName = "hbase_test", description = "policy for the hbase test",
                          resources = {"column":{"isExcludes":"false","value":["*"]},"table":{"isExcludes":"false","value":["j*","d*"]},"column_family":{"isExcludes":"false","value":["*"]}}, 
                          users = ["it1"], groups = [], 
                          accesses = ["read","write","create","admin"])
```

#### Hive

```Python
rangerApi.postCreatePolicy(policyTemplateType = "hive", serviceName = "Sandbox_hive", 
                          policyName = "hive_test", description = "policy for the hive test",
                          resources = {"column":{"isExcludes":"false","value":["*"]},"table":{"isExcludes":"false","value":["j*","d*"]},"database":{"isExcludes":"false","value":["*"]}},
                          users = ["it1"], groups = [],
                          accesses = ["select","update","create","drop","alter","index","lock","all","read","write"])
```

#### Kafka

```Python
rangerApi.postCreatePolicy(policyTemplateType = "kafka", serviceName = "Sandbox_kafka", 
                          policyName = "kafka_test", description = "policy for the kafka test",
                          resources = ["topicLakeTest","topicProjectTest"], isRecursive = False, 
                          users = ["it1"], groups = [],
                          accesses = ["publish","consume","configure","describe","create","delete","kafka_admin"])
```

#### Knox

```Python
rangerApi.postCreatePolicy(policyTemplateType = "knox", serviceName = "Sandbox_knox", 
                          policyName = "knox_test", description = "policy for the knox test",
                          resources = {"service":{"isExcludes":"false","value":["*"]},"topology":{"isExcludes":"false","value":["j*","d*"]}}, 
                          users = ["it1"], groups = [],
                          accesses = ["allow"])
```

#### Yarn

```Python
rangerApi.postCreatePolicy(policyTemplateType = "yarn", serviceName = "Sandbox_yarn", 
                          policyName = "yarn_test", description = "policy for the yarn test",
                          resources = ["default"], isRecursive = False, 
                          users = ["it1"], groups = [],
                          accesses = ["submit-app","admin-queue"])
```

## How to use it in Ansible mode

For testing see the [test_ranger_policy.yml](./test_ranger_policy.yml) file with many examples.

### Ranger_policy Ansible module

#### Ranger_policy examples

```yaml
- hosts: localhost
  tasks:
  - name: ranger policy creation
    ranger_policy:
      admin_url: "http://127.0.0.1:6080"
      ranger_user: "raj_ops"
      ranger_user_password: "raj_ops"
      policy_type: "hdfs"
      service_name: "Sandbox_hadoop"
      policy_name: "lake_test"
      description: "Policy test"
      resources:
          - /lake/test
          - /lake/data
      accesses: "rwx"
      users: 
          - it1
  - name: ranger policy deletion
    ranger_policy:
      admin_url: "http://127.0.0.1:6080"
      ranger_user: "raj_ops"
      ranger_user_password: "raj_ops"
      policy_type: "hdfs"
      service_name: "Sandbox_hadoop"
      policy_name: "lake_test"
      state: absent
```

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
 |  createUser(self, userName, firstName, lastName, emailAddress, description, password, groupIdList=[], userRoleList=[])
 |      create an internal user
 |      MAndatory values :
 |          "name","firstName","lastName","emailAddress","description","password","groupIdList","userRoleList"
 |  
 |  deleteDeletePolicyByServiceAndPolicyName(self, serviceName='', policyName='')
 |      Delete a policy by its name and service
 |      https://cwiki.apache.org/confluence/display/RANGER/Apache+Ranger+0.6+-+REST+APIs+for+Service+Definition%2C+Service+and+Policy+Management#ApacheRanger0.6
-RESTAPIsforServiceDefinition,ServiceandPolicyManagement-Deletepolicybyservice-nameandpolicy-name
 |  
 |  deleteUser(self, userNameOrId)
 |      delete a user
 |  
 |  getGroup(self, groupNameOrId)
 |      get the group by Name or Id
 |  
 |  getGroups(self)
 |      get the groups
 |  
 |  getPolicyByServiceAndPolicyName(self, serviceName, policyName)
 |      get a policy by Service and Policy Name
 |  
 |  getSearchPolicyInService(self, serviceName, policyName='')
 |      get a search on policy in a service
 |  
 |  getService(self, serviceNameOrId)
 |      get a service by Name or Id
 |  
 |  getServices(self, serviceType='')
 |      get the services
 |      
 |      serviceType string The service types(such as "hdfs","hive","hbase","knox","storm", "atlas")
 |  
 |  getUser(self, userNameOrId)
 |      get an user by Name or Id
 |  
 |  getUsers(self)
 |      get the users
 |  
 |  postApplyPolicy(self, **kwargs)
 |      post to update or create a policy
 |      https://cwiki.apache.org/confluence/display/RANGER/Apache+Ranger+0.6+-+REST+APIs+for+Service+Definition%2C+Service+and+Policy+Management#ApacheRanger0.6-RESTAPIsforServiceDefinition,ServiceandPolicyManagement-ApplyPolicy
 |      This request should not remove permissions, only add more permissions or create new ones
 |  
 |  postCreatePolicy(self, **kwargs)
 |      post to create a policy
 |      https://cwiki.apache.org/confluence/display/RANGER/Apache+Ranger+0.6+-+REST+APIs+for+Service+Definition%2C+Service+and+Policy+Management#ApacheRanger0.6-RESTAPIsforServiceDefinition,ServiceandPolicyManagement-CreatePolicy
 |      Arguments :
 |          policyTemplateType = one of ["hdfs", "yarn", "hbase", "hive", "knox", "storm", "solr", "kafka", "nifi", "atlas"] 
 |          serviceName = Name of the service
 |          policyName = Name of the policy
 |          description = description
 |          isRecursive = Is policy recursive
 |          users = Array of users
 |          groups = Array of groups
 |          resources = Resource affected by the policy ex :'["/lake/test"]', PolicyTemplateType dependent
 |          accesses = Permissions poistionned on the resource, PolicyTemplateType dependent
 |  
 |  putUpdatePolicyByServiceAndPolicyName(self, **kwargs)
 |      post to update or create a policy
 |      https://cwiki.apache.org/confluence/display/RANGER/Apache+Ranger+0.6+-+REST+APIs+for+Service+Definition%2C+Service+and+Policy+Management#ApacheRanger0.6-RESTAPIsforServiceDefinition,ServiceandPolicyManagement-UpdatePolicybyservice-nameandpolicy-name
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
## Author

Eric Deleforterie


## LICENSE

This repository is available under "GNU GENERAL PUBLIC LICENSE" (v. 3)

http://www.gnu.org/licenses/gpl.txt

![alt text](https://www.gnu.org/graphics/gplv3-127x51.png)
