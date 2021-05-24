# GVE_DevNet_Meraki_MX_Golden_Firewall_Rules
prototype code that allows the user to select and provision a golden set of firewall configurations (L3 and L7) onto multiple networks (MXs) . 


## Contacts
* Jorge Banegas

## Solution Components
* Meraki
*  MX
*  Python

## Installation/Configuration
1. First step will be to include your personal api key inside the config.py file for the script to use

```python
    api_key=""
    
```
2. Create virtual environment and name it env, then activate it

```console
foo@bar:~$ virtualenv env
foo@bar:~$ source env/bin/activate
```

4. Install the dependencies required for the python script
```console
foo@bar(env):~$ pip install -r requirements.txt
```

## Usage

```console
foo@bar(env):~$ python main.py
```

# Screenshots
This is the golden set of firewall rules that we will want to provision onto other networks

![/IMAGES/golden_policy.png](/IMAGES/golden_policy.png)


This is Testing Network's group policy page (currently has no group policies).

![/IMAGES/before_script.png](/IMAGES/before_script.png)

1 . Select what group policy to search for

![/IMAGES/step_1.png](/IMAGES/step_1.png)


2 . After finding a group policy under the provided name, view unmatched and matched group policies.

![/IMAGES/step_2.png](/IMAGES/step_2.png)


3 . View matched group policies and select the golden configuration set for the firewall rules

![/IMAGES/step_3.png](/IMAGES/step_3.png)


4 . View unmatched group policies and select which networks to provision the golden firewall confinguration rules

![/IMAGES/step_4.png](/IMAGES/step_4.png)


![/IMAGES/step_5.png](/IMAGES/step_5.png)


5 . After the script is finished running, the testing network now contains the configurations of the selected golden configuration

![/IMAGES/after_script.png](/IMAGES/after_script.png)

### Notes

Notice in the screenshot provided, it seems like country based L7 rules do not transfer over. 



### LICENSE

Provided under Cisco Sample Code License, for details see [LICENSE](LICENSE.md)

### CODE_OF_CONDUCT

Our code of conduct is available [here](CODE_OF_CONDUCT.md)

### CONTRIBUTING

See our contributing guidelines [here](CONTRIBUTING.md)

#### DISCLAIMER:
<b>Please note:</b> This script is meant for demo purposes only. All tools/ scripts in this repo are released for use "AS IS" without any warranties of any kind, including, but not limited to their installation, use, or performance. Any use of these scripts and tools is at your own risk. There is no guarantee that they have been through thorough testing in a comparable environment and we are not responsible for any damage or data loss incurred with their use.
You are responsible for reviewing and testing any scripts you run thoroughly before use in any non-testing environment.
