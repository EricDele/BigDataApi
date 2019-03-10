# BigDataApi
A BigData Api library for managing Ambari and Ranger

- [BigDataApi](#bigdataapi)
  - [Goal of this project](#goal-of-this-project)
  - [Imports required](#imports-required)
  - [How to use it in python mode](#how-to-use-it-in-python-mode)
    - [Initiate an object](#initiate-an-object)
      - [Ambari](#ambari)
      - [Ambari Metrics](#ambari-metrics)
      - [Ranger](#ranger)
    - [Ranger Policies creation](#ranger-policies-creation)
      - [Hdfs](#hdfs)
      - [Hbase](#hbase)
      - [Hive](#hive)
      - [Kafka](#kafka)
      - [Knox](#knox)
      - [Yarn](#yarn)
    - [Create custom metrics in ambari metrics](#create-custom-metrics-in-ambari-metrics)
      - [Sending Zookeeper metrics to Ambari Metrics Collector](#sending-zookeeper-metrics-to-ambari-metrics-collector)
  - [How to use it in Ansible mode](#how-to-use-it-in-ansible-mode)
    - [Ranger_policy Ansible module](#rangerpolicy-ansible-module)
      - [Ranger_policy examples](#rangerpolicy-examples)
  - [Classes Tree](#classes-tree)
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
For testing Ambari Metrics see the [test_ams.py](./test_ams.py) which coudl help you to send new custom metrics to AMS

### Initiate an object

#### Ambari 

```Python
ambariApi = AmbariApi("http", "127.0.0.1", "8080", "basic")
ambariApi.setCredentialsBasic("admin", "hortonworks")
result = ambariApi.getClusterName() # Get the cluster name
print(ambariApi) # Will show you the result
help(ambariApi) # Will show you the class methods
```

#### Ambari Metrics

```Python
ambariMetricsApi = AmbariMetricsApi("http", "localhost", "6188", "basic")
ambariMetricsApi.setCredentialsBasic("admin", "")
ambariMetricsApi.getMetrics(metricNames="dfs.datanode.BlocksWritten", appId="datanode", hostname="sandbox-hdp.hortonworks.com", precision="seconds", startTime=int((time.time()-600)*1000), endTime=int(time.time()))
print(ambariMetricsApi)
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

### Create custom metrics in ambari  metrics

For testing Ambari Metrics see the [test_ams.py](./test_ams.py) which coudl help you to send new custom metrics to AMS

#### Sending Zookeeper metrics to Ambari Metrics Collector

For sending output of **mntr** and **wchc** commands to AMS see below shell to use with [test_ams.py](./test_ams.py)

```Shell
[BigDataApi]> echo mntr | nc localhost 2181 | ./test_ams.py --type mntr --hostname sandbox-hdp.hortonworks.com
[BigDataApi]> echo wchc | nc localhost 2181 | cur -d'/' | egrep -v "^0x|^$" | sort | uniq -c | sort -n | ./test_ams.py --type wchc --hostname sandbox-hdp.hortonworks.com
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
    |-- AmbariMetrics
```

## Author

Eric Deleforterie


## LICENSE

This repository is available under "GNU GENERAL PUBLIC LICENSE" (v. 3)

http://www.gnu.org/licenses/gpl.txt

![alt text](https://www.gnu.org/graphics/gplv3-127x51.png)
