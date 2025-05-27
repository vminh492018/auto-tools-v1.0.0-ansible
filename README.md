# Automated Deployment & Compliance Checking Tool

[![Ansible Version](https://img.shields.io/badge/Ansible-2.15.13-red.svg)](https://docs.ansible.com/)
[![Python Version](https://img.shields.io/badge/Python-3.10-blue.svg)](https://www.python.org/)

**Author:** MinhVu  
**Version:** v1.0.0  

## Overview
An automation tool built with Ansible for:
- Automated deployment of enterprise applications: MariaDB (10.6.21 ++), Redis (6.2.12 ++), etc...
- Configuration management and standardization
- Compliance checking and reporting
- Health monitoring and validation

The tool supports both:
- Physical/virtual server environments
- Containerized deployments

## Important Notes for Inventory Configuration

When configuring the inventory file (`hosts.ini`), you must follow these group naming conventions:

| Application | Required Group Name  | Description |
|------------|---------------------|-------------|
| MariaDB    | `[MariaDB_servers]` | Group name for MariaDB cluster nodes |
| Redis      | `[Redis_servers]`   | Group name for Redis/Sentinel nodes |

These group names are mandatory as they are referenced in the playbooks and roles. Example inventory structure:

```ini
# Example inventory structure
[MariaDB_servers]
192.168.80.111 ansible_host=192.168.80.111 ansible_user=minhvx ansible_ssh_pass=1 ansible_become_password=1
192.168.80.112 ansible_host=192.168.80.112 ansible_user=minhvx ansible_ssh_pass=1 ansible_become_password=1
192.168.80.113 ansible_host=192.168.80.113 ansible_user=minhvx ansible_ssh_pass=1 ansible_become_password=1

[Redis_servers]
192.168.153.21 ansible_host=192.168.153.21 ansible_user=minhvx ansible_ssh_pass=1 ansible_become_password=1
192.168.153.22 ansible_host=192.168.153.22 ansible_user=minhvx ansible_ssh_pass=1 ansible_become_password=1
192.168.153.23 ansible_host=192.168.153.23 ansible_user=minhvx ansible_ssh_pass=1 ansible_become_password=1
```

> **Note**: The tool will look for these exact group names when executing playbooks. Using different group names will result in playbook failures.

## Core Components
* Ansible 
  ```
  - Ansible [core 2.15.13]
  - Python version = 3.10.12 (main, Nov  6 2024, 20:22:13) [GCC 11.4.0] (/usr/bin/python3)
  - jinja version = 3.1.2
  - libyaml = True
  ```

### Optional Components
* Docker images
  ```
  - docker pull vminh492018/ansible-ubuntu:v1.0.0
  ```
* Docker run container via cmd:
  ```
  - docker run -d -it --name ansible -v /home/minhvx/ansible:/ansible vminh492018/ansible-ubuntu:v1.0.0
  ```

### Structure
```
auto-tool-v1.0.0-ansible/
├── inventory/
│   ├── dynamic_inventory.py   # Dynamic inventory using API calls
│   └── hosts.ini              # Static inventory defining hosts and groups
├── playbooks/
│   ├── mariadb_checklist.yml         # Checklist for MariaDB servers 
│   ├── mariadb_setup.yml             # Deploy a MariaDB replication/Maxscale cluster standards
│   ├── os_checklist.yml              # Checklist for Linux servers (CentOS 7/9, Ubuntu 20.04+) 
│   ├── redis_sentinel_checklist.yml  # Checklist for Redis/Sentinel servers 
│   └── ...                                    # Other playbooks
├── roles/
│   ├── report-generator/                # Role for generating report files for checklist-related roles/tasks
│   │   ├── tasks/
│   │   │   ├── main.yml                 # Main task file that includes all other tasks in the role
│   │   │   └── ...                      # Feature-specific tasks of the role
│   │   └── defaults/
│   │       └── main.yml                 # Default variables for the role
│   │
│   ├── mariadb-setup/                   # Role for installing, configuring, and setting up MariaDB replication
│   │   ├── tasks/
│   │   │   ├── mariadb_install.yml            # Task for installing base MariaDB
│   │   │   ├── mariadb_replication_setup.yml  # Task for configuring MariaDB replication
│   │   │   └── precheck_MariaDB.yml           # Task to check server prerequisites before deployment
│   │   ├── templates/
│   │   │   └── my.cnf.j2                      # MariaDB configuration template
│   │   ├── files/                             # Directory for MariaDB and Maxscale installation packages
│   │   └── defaults/
│   │       └── main.yml                       # Default variables for the role
│   │
│   ├── mariadb-checklist/                     # Role for checking MariaDB compliance with handover criteria
│   │   ├── tasks/
│   │   │   ├── main.yml                       # Main task file that includes all feature tasks
│   │   │   └── ...                            # Feature-specific tasks of the role
│   │   └── defaults/
│   │       └── main.yml                       # Default variables for the role
│   └── ...                                    # Other roles
│ 
├── ansible.cfg                # Project-wide Ansible configuration file
└── README.md                  # Project documentation and user guide
```

### How to run project?
* Running playbook, use the following command:
   ```bash
   ansible-playbook -i inventory/hosts.ini playbooks os_checklist.yml -b --become-method=su
   ```

* Running Ansible in a container from a local server (using a Docker container as the environment to execute Ansible, instead of running Ansible directly on the host server)
   ```bash
   docker exec -it [container_ID/container_name] bash -c "cd /PATH/TO/PROJECT && ansible-playbook -i inventory/hosts.ini playbooks/check_OS.yml" -b --become-method=su
   ```