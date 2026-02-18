# nautobot-awx-spb

> **Nautobot Plugin** for managing **Shortest Path Bridging (SPB)** network configurations on **ALE OmniSwitch (AOS8)** devices, with automated provisioning via **AWX/Ansible** triggered by Nautobot webhooks.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#Nautobot-Plugin-Installation)
- [Data Models](#data-models)
- [Ansible Roles](#ansible-roles)
- [Ansible Inventory](#ansible-inventory--nautobot-dynamic-inventory)
- [Project Structure](#project-structure)
- [Usage](#usage)
- [Author](#author)

---

## Overview

`nautobot-spb` is a Nautobot application plugin that extends the Nautobot DCIM/IPAM platform with full SPB (IEEE 802.1aq) data modeling, UI management, and automated configuration deployment. When a network operator creates or updates an SPB object in Nautobot, a webhook fires an AWX job that pushes the configuration directly to the ALE switches.

```
Nautobot UI  ──webhook──►  AWX / Ansible  ──SSH──►  ALE OmniSwitch (AOS8)
   (nautobot-spb plugin)       (Playbooks)             (SPB Configuration)
```

---

## Features

- **Full SPB data model** in Nautobot: BVLANs, Services, SAPs, Interfaces, ISIS instances, IPVPN Bindings & Redistributions, and Topologies
- **Dedicated SPB navigation tab** in Nautobot (Topology / Backbone / Layer 2 / Layer 3 / SAPs)
- **Device & Interface detail tabs**: SPB ISIS, SPB Interfaces, SPB Services, SPB Config directly accessible from existing Nautobot device views
- **Webhook-enabled models**: all SPB objects trigger change logging and webhook events on create/update/delete
- **Multi-device / multi-interface forms**: create a service or SAP across multiple devices at once
- **Auto-creation of BVLANs**: creating a Topology automatically provisions the required Control and Data BVLANs
- **AWX Ansible automation**: three Ansible roles handle end-to-end SPB provisioning
  - `SPB_config_L2` — full topology (BVLANs + ISIS + interfaces)
  - `SPB_service_L2` — L2 SPB service (ISID/BVLAN binding)
  - `SPB_SAP` — Service Access Points with encapsulation
- **CSV bulk import** for BVLANs and Services
- **Idempotent Ansible plays**: existing configuration is retrieved before applying changes (create vs. update logic)

---
## Requirements

| Dependency | Version |
|---|---|
| Nautobot | ≥ 2.4.0 |
| Python | ≥ 3.8 |
| AWX / Ansible AWX Operator | any recent |
| Ansible collection `ale.aos8` | latest |
| ALE OmniSwitch | AOS8 |

---

## Nautobot Plugin Installation
### 1. Clone the repository

```bash
git clone https://github.com/<your-org>/nautobot-spb.git
cd nautobot-spb
```

### 2. Install the plugin

```bash
pip install -e .
```

Or copy the `nautobot_spb/` directory into your Nautobot project.

### 3. Register the plugin in Nautobot

In your `nautobot_config.py`:

```python
PLUGINS = ["nautobot_spb"]

PLUGINS_CONFIG = {
    "nautobot_spb": {}
}
```

### 4. Run database migrations

```bash
nautobot-server migrate
```

### 5. Restart Nautobot

```bash
sudo systemctl restart nautobot nautobot-worker
```

---
## Data Models

| Model | Description |
|---|---|
| `SPB_Topology` | High-level topology object grouping BVLANs, devices, and interfaces. |
| `SPB_BVLAN` | Backbone VLAN (control or data). Only one control BVLAN allowed. |
| `SPB_Service` | SPB L2 service instance, tied to a device, ISID and BVLAN. |
| `SPB_SAP` | Service Access Point: associates a service with a device port and encapsulation(s). |
| `SPB_Interface` | Physical interface participating in SPB ISIS. |
| `SPB_ISIS` | ISIS-SPB instance configuration (bridge priority, SPF/LSP timers, graceful restart). |
| `SPB_IPVPN_Bind` | Binding between a VRF and an SPB service (L3 over SPB). |
| `SPB_IPVPN_Redist` | Route redistribution between VRFs/ISIDs. |

> **Note:** BVLANs are automatically created when a Topology is saved and validated. However, the **Control BVLAN must never be changed** after initial deployment modifying it requires reconfiguring every device in the architecture. Similarly, any device or configuration added outside of the Topology workflow must be carefully reviewed to ensure its assignments remain consistent with the existing infrastructure.
---
## Ansible Roles

Roles are located under `playbooks/roles/updates_from_nautobot/` and triggered by the main playbook `interface_config_playbook.yml`.

### Role dispatch (webhook `role` variable)

| `role` value | Ansible role invoked | Purpose |
|---|---|---|
| `SPB_TOPOLOGY` | `SPB_config_L2` | Configure BVLANs, ISIS, interfaces |
| `SPB_SERVICE` | `SPB_service_L2` | Create/update an SPB service |
| `SPB_SAP` | `SPB_SAP` | Create SAP and bind encapsulations |

### Example webhook payload variables

```json
{
  "role": "SPB_TOPOLOGY",
  "topology_name": "DC-CORE",
  "control_bvlan_id": "1000",
  "data_bvlan_ids": "2001,2002,2003",
  "devices": ["switch-01", "switch-02"],
  "interfaces": ["switch-01:1/1/1", "switch-02:1/1/1"],
  "iface_type": "p2p",
  "hello_interval": 9,
  "hello_multiplier": 3,
  "metric": 10,
  "admin_state": true
}
```

---
## Ansible Inventory — Nautobot Dynamic Inventory

Devices are pulled **dynamically from Nautobot** using the `networktocode.nautobot` collection. No static hosts file is needed.

### `inventory/nautobot_sync.yml` — GraphQL inventory plugin

```yaml
plugin: networktocode.nautobot.gql_inventory
api_endpoint: "https://<nautobot-ip>/"
token: "<nautobot-api-token>"
validate_certs: false
query:
  devices:
    id: null
    name: null
    primary_ip4: host
    platform:
      napalm_driver
      network_driver
compose:
  ansible_host: primary_ip4.host
  ansible_network_os: >-
    {{
      'ale.aos8.aos8'
      if platform.napalm_driver == 'aos'
      else 'unsupported'
    }}
  ansible_connection: network_cli
  ansible_user: "switch-username"
  ansible_password: "switch-password"
  ansible_command_timeout: 60
  ansible_connect_timeout: 90
group_by:
  - role.name
```
- Devices are grouped by their **Nautobot device role** (`role.name`)
- `ansible_network_os` is automatically set to `ale.aos8.aos8` for AOS devices based on the Nautobot platform `napalm_driver` field

### Required Ansible collection

```bash
ansible-galaxy collection install networktocode.nautobot
```

Or via `requirements.yml`:

```yaml
collections:
  - name: networktocode.nautobot
  - name: kubernetes.core
    version: ">=2.3.2"
  - name: operator_sdk.util
    version: "0.5.0"
```

### `ansible.cfg`

Key settings used in this project:

```ini
[defaults]
inventory             = ./ansible/inventory
host_key_checking     = False
forks                 = 15
gathering             = smart
stdout_callback       = yaml
collections_paths     = ./collections
jinja2_extensions     = jinja2.ext.loopcontrols,jinja2.ext.do

[persistent_connection]
command_timeout = 45

[ssh_connection]
ssh_args = -o StrictHostKeyChecking=no

[inventory]
enable_plugins = networktocode.nautobot.inventory, networktocode.nautobot.gql_inventory, yaml, ini
```

---

## Project Structure

```
nautobot_spb/
├── __init__.py          # NautobotAppConfig (plugin entry point)
├── models.py            # Django ORM models for all SPB objects
├── forms.py             # Create/edit/filter/CSV forms
├── views.py             # List, detail, add, edit, delete views
├── tables.py            # django-tables2 table definitions
├── urls.py              # URL routing for all SPB views
├── navigation.py        # Nautobot nav menu (SPB tab)
├── extend.py            # Device & Interface detail tab extensions
├── registration.py      # Webhook & change logging feature registration
├── templates/           # Jinja2 HTML templates
├── api/                 # REST API (serializers, views, URLs)
└── migrations/          # Django database migrations

playbooks/
├── interface_config_playbook.yml          # Main dispatcher playbook
└── roles/updates_from_nautobot/
    ├── SPB_config_L2/tasks/main.yaml      # Topology role
    ├── SPB_service_L2/tasks/main.yml      # Service role
    └── SPB_SAP/tasks/main.yml             # SAP role

ansible/
├── ansible.cfg                            # Ansible global configuration
├── requirements.yml                       # Collection dependencies
└── inventory/
    ├── nautobot_sync.yml                  # Dynamic inventory (Nautobot GQL plugin)
    └── group_vars/
        └── all.yml                        # Global variables
```

---

## Usage

### Prerequisites — Verify Initial State

Before any configuration, ensure all switches are running with **no existing SPB configuration**.

### Prerequisites — AWX & Webhooks Setup

Before configuring anything in Nautobot, ensure AWX is ready:

In AWX, the following must already exist:
- A **Project** linked to the Git repository
- An **Execution Environment** containing the `ale.aos8` collection
- A **Job Template** (the template ID is visible in the AWX URL)

In Nautobot, configure **three dedicated webhooks** (one per object type: Topology, Service, SAP).
Each webhook includes a **Body Template** that passes dynamic variables to AWX via REST API,
and targets a specific Job Template ID.

---

### Step 1 — SPB Topology (Backbone)

Navigate to **SPB → Topology → SPB Topologies → Add** and define:
- Topology name and optional description
- Control BVLAN
- Data BVLANs *(must be identical across all devices)*
- SPB interfaces for each switch

Once saved, the webhook triggers AWX automatically. The job starts, receives all parameters
from Nautobot, and pushes the backbone configuration to all switches.

---

### Step 2 — SPB Services

Navigate to **SPB → Layer 2 → SPB Services → Add** and define:
- Service ID
- ISID
- Target devices

Saving triggers the AWX webhook again. The job template deploys the service configuration
to all selected switches.

---

### Step 3 — SAP Configuration

Navigate to **SPB → SAPs → SAPs → Add** and define the access port(s) and encapsulation(s).
Nautobot triggers AWX once more to push the SAP configuration to the target devices.


---

### Validation

Ping between the two client machines connected on your devices
Successful connectivity confirms the SPB backbone, services, and SAPs are fully operational.

The SPB configuration is fully automated, deployed, and validated using:
- **Nautobot** — Source of Truth
- **Webhooks** — Event-driven triggers
- **AWX** — Automation Engine
- **ALE AOS8 switches** — Target network devices



