#!/usr/bin/env python
# -*- coding: utf-8 -*-

import fileinput
import argparse
import re
import time
import json

from module_utils.ambari_metrics import AmbariMetricsApi

mntr_fields = ['zk_avg_latency','zk_max_latency','zk_min_latency','zk_packets_received','zk_packets_sent','zk_num_alive_connections','zk_outstanding_requests','zk_znode_count','zk_watch_count','zk_ephemerals_count','zk_approximate_data_size','zk_open_file_descriptor_count','zk_max_file_descriptor_count']
wchc_fields = ['nifi', 'hadoop-ha', 'hiveserver2', 'hiveserver2-http', 'yarn-leader-election', 'ambari-metrics-cluster', 'oozie', 'ams-hbase-secure', 'kafka', 'hbase-secure', 'smartsense']
fields = {"mntr": mntr_fields, "wchc": wchc_fields}
type_prefix = {"mntr": "zookeeper.", "wchc": "zookeeper.zk_path"}
patterns = {"mntr": re.compile("^(?P<key>\w+)\s+(?P<value>.*)$"), "wchc": re.compile("^\s*(?P<value>\d+)\s+(?P<key>.*)$")}

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='ZK4Letters test', prog='test_ams.py')
    parser.add_argument('--type', type=str, choices=['mntr','wchc'], required=True, help='Type of ZK 4Letters command')
    parser.add_argument('--hostname', type=str, required=True, help='hostname')
    args = parser.parse_args()
    timestamp = int(time.time()*1000)

    ambariMetricsApi = AmbariMetricsApi("http", "localhost", "6188", "basic")
    ambariMetricsApi.setCredentialsBasic("admin", "")

    # Test the Get 
    ambariMetricsApi.getMetrics(metricNames="dfs.datanode.BlocksWritten", appId="datanode", hostname="sandbox-hdp.hortonworks.com", precision="seconds", startTime=int((time.time()-600)*1000), endTime=int(time.time()))
    print(ambariMetricsApi)

    # Test the Put
    for line in fileinput.input(('-',)):
        match = patterns[args.type].match(line)
        if(match):
            if(match.group('key') in fields[args.type]):
                ambariMetricsApi.postMetrics(metricNames=type_prefix[args.type] + match.group('key'), appId='zookeeper', hostname=args.hostname,
                                            startTime=int(timestamp), timestamp=int(timestamp),
                                            metrics=json.dumps({str(timestamp): int(match.group('value'))}) )
