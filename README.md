# zabbix-ansible
1. Install zabbix server and agent in Centos 7.x
2. Make sure close selinux
3. Use postgres as the zabbix database 
4. Agent default is active mode

## Install Zabbix Server
Update vars/zabbix_basic.yml
```
#path of zabbix configuration
zabbix_conf_path: /etc/zabbix

zabbix_user: zabbix
zabbix_group: zabbix

#rpm key of zabbix
zabbix_key_url: "http://repo.zabbix.com/RPM-GPG-KEY-ZABBIX"
#rpm of zabbix
zabbix_rpm_url: "http://repo.zabbix.com/zabbix/3.4/rhel/7/x86_64/zabbix-release-3.4-2.el7.noarch.rpm" # this is the zabbix version 3.4.2 is the latest version

# service port
service_ports:
  - "80"
  - "10051"
  
```
Update vars/zabbix_server.yml

```
---
#time zone
timezone: 'Asia/Shanghai' # use your own time zone

#postgres     postgres infomation, make sure you have created it  
db_host: '172.16.251.33'
db_port: '5432'
db_name: 'zabbix'
db_user: 'zabbix'
db_password: 'nfsetso12fdds9s'
db_schema: 'zabbix'
#db_type: mysql,postgres,sqlite, for now, just support postgres
db_type: 'postgres'

# install postgres client ,you can update the version from [postgres for redhat]( https://www.postgresql.org/download/linux/redhat/)
# postgres client, default 9.6
postgres_rpm_url: 'https://download.postgresql.org/pub/repos/yum/9.6/redhat/rhel-7-x86_64/pgdg-redhat96-9.6-3.noarch.rpm'
postgres_client: 'postgresql96'

# install list 
# zabbix-server-mysql,zabbix-server-pgsql, zabbix-server-sqlite3
zabbix_server_install:
    - 'zabbix-server-pgsql'
    - 'zabbix-web-pgsql'

#Start services
services:
   - 'zabbix-server'
   - 'httpd'

```

Update hosts
```
[zabbix_server]
172.16.251.75
```

Update init_zabbix_server.yml

```
---
- name: Init Zabbix Server
  hosts: zabbix_server
  #define variable for zabbix
  vars:
     #install zabbix server when install is true
     install: true
     #config the zabbix-server configuration when config is true
     config: true
  vars_files:
    - vars/zabbix_basic.yml
    - vars/zabbix_server.yml
  user: root
  roles:
   - basic
   - postgres
   - init_zabbix_server
   - service

```


then you can run like:

```
ansible-playbook -i hosts init_zabbix_server.yml
```
now you can visit the http://your_ip/zabbix to finish the installation

## Config Zabbix Server
After installation, you should config the template and discovery
1. Change Linux Template To ActiveMode(Use Zabbix Agent)
2. Create discovery action and auto registration action
3. Enable actions and discovery  

Just Baidu it, what? You can touch google? OK,google it

## Install Zabbix Agent
Update vars/zabbix_agent.yml

```
---

need_script: true

user_parameter_list:
   - "http.status[*],python {{zabbix_conf_path}}/script/http_monitor.py $1"

zabbix_script_list:
   - "http_monitor.py"


#installation of zabbix
zabbix_agent_install:
  - "zabbix-agent"

#zabbix master ip
server_active_ip: 172.16.251.75 # your zabbix master ip

#refress time
refresh_active_checks: 60

services: 
  - 'zabbix-agent'

```

Update hosts
```
[zabbix_agent]
172.16.251.76
172.16.251.77
```

Update init_zabbix_agent.yml

```
- name: Init Zabbix Agent
  hosts: zabbix_agent
  #define variable for zabbix
  vars:
     #install zabbix agent when install is true
     install: true
     #config the zabbix-agent configuration when config is true
     config: true
  vars_files:
    - vars/zabbix_basic.yml
    - vars/zabbix_agent.yml
  user: root
  roles:
   - init_zabbix_agent
   - service


```


Now you can run like:

```
ansible-playbook -i hosts init_zabbix_agent.yml
```

## License
source code is licensed under the Apache Licence, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0.html).