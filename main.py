""" 
Copyright (c) 2020 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
           https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""

import meraki 
import json
import config 
import pprint
import sys
import datetime


dashboard = meraki.DashboardAPI(config.api_key,single_request_timeout=999999,output_log=False,print_console=False)
policy_found = False

policy_name = input("Enter policy name : ")
    

orgs = dashboard.organizations.getOrganizations()

networks_with_policy = []
networks_without_policy = []
golden_policy = None
network_ids = None

for org in orgs:
    networks = dashboard.organizations.getOrganizationNetworks(organizationId=org["id"])
    for network in networks:
        try:
            group_policies = dashboard.networks.getNetworkGroupPolicies(networkId=network["id"])
        except meraki.AsyncAPIError as e:
            print(f"Meraki API error: {e}")
            continue
        except Exception as e:
            print(f"some other error: {e}")

        for group_policy in group_policies:
            if policy_name.lower() == group_policy["name"].lower():
                policy_found = True

                temp = {}
                temp["network"] = network["name"]
                temp["network_id"] = network["id"]
                temp["org"] = org["name"]
                temp["policy_name"] = group_policy["name"]
                temp["l3_rules"] = group_policy["firewallAndTrafficShaping"]["l3FirewallRules"]
                temp["l7_rules"] = group_policy["firewallAndTrafficShaping"]["l7FirewallRules"]
                temp["policy_id"] = group_policy["groupPolicyId"]
                networks_with_policy.append(temp)

                print('Policy found. Network name: ', network["name"], "Organization name: ", org["name"])
                print("-------------------------------------------------------------------")

            else:
                temp = {}
                temp["network"] = network["name"]
                temp["org"] = org["name"]
                temp["policy_name"] = group_policy["name"]
                temp["l3_rules"] = group_policy["firewallAndTrafficShaping"]["l3FirewallRules"]
                temp["l7_rules"] = group_policy["firewallAndTrafficShaping"]["l7FirewallRules"]
                temp["policy_id"] = group_policy["groupPolicyId"]
                temp["network_id"] = network["id"]
                networks_without_policy.append(temp)


if policy_found == False:
                    print("Could not find any policy with the name ",policy_name)
                    print("Shutting down")
                    sys.exit()
res = ''

while res.lower() != 'e':
    if golden_policy != None and network_ids != None:
        res1 = input("Do you wish to continue to push policy " + golden_policy + " onto the networks " + network_ids +  " (Y)es or (N)o " + " : " )

        if res1.lower() == "n":
            print("shutting down")
            sys.exit()

        if res1.lower() == "y":
            network_id = golden_policy.split(',')[0]
            policy_id = golden_policy.split(',')[1]

            policy = dashboard.networks.getNetworkGroupPolicy(networkId=network_id,groupPolicyId=policy_id)

            firewall_rules = policy["firewallAndTrafficShaping"]
            policy_name = policy["name"]

            for network in network_ids.split(','):
                try:
                    response = dashboard.networks.createNetworkGroupPolicy(name=policy_name,networkId=network,firewallAndTrafficShaping=firewall_rules)

                except meraki.APIError as e:
                    print(f'meraki API error:{e}')
                    print(f'status error:{e.status}')
                    print(f'reason:{e.reason}')
                    print(f'error:{e.message}')

                    network_name = dashboard.networks.getNetwork(networkId=network)
                    # Open a file with access mode 'a'
                    text = "Status : " +  str(e.status) + "| Error Reason : " + str(e.message) + " for network " + network_name["name"] +  " and policy " + policy_name + " " + str(datetime.datetime.now()) + "\n"
                    file_object = open('error.txt', 'a')
                    # Append 'hello' at the end of file
                    file_object.write(text)
                    # Close the file
                    file_object.close()
                    #pprint.pprint(response)`
                    continue

                network_name = dashboard.networks.getNetwork(networkId=network)
            
                # Open a file with access mode 'a'
                text = "policy " + response["name"] + " pushed onto network " + network_name["name"] +  " " + str(datetime.datetime.now()) + "\n"
                file_object = open('log.txt', 'a')
                # Append 'hello' at the end of file
                file_object.write(text)
                # Close the file
                file_object.close()
                #pprint.pprint(response)


    res = input("View (U)nmatched policies | View (M)atched policies | (E)nd program : ")

    if res.lower() == 'm':
        print("Network's with matched policies")

        for network_with_policy in networks_with_policy:
            pprint.pprint(network_with_policy)
            print("---------------------------------------")
            print("*******************************************")

        golden_policy = input("Choose the network id and policy id of the golden policy Ex . [networkid,policyid]: ")

    if res.lower() == 'u':
        print("Network's with unmatched policies")

        for network_without_policy in networks_without_policy:
            pprint.pprint(network_without_policy)
            print("---------------------------------------")
            print("*******************************************")

        network_ids = input("Choose the Network IDs to push golden policy to (ex. networkid1,networkid2,networkid3) : ")