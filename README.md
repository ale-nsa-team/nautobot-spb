# nautobot-awx-spb

> **Nautobot Plugin** for managing **Shortest Path Bridging (SPB)** network configurations on **ALE OmniSwitch (AOS8)** devices, with automated provisioning via **AWX/Ansible** triggered by Nautobot webhooks.

---
## Overview

`nautobot-spb` is a Nautobot application plugin that extends the Nautobot DCIM/IPAM platform with full SPB (IEEE 802.1aq) data modeling, UI management, and automated configuration deployment. When a network operator creates or updates an SPB object in Nautobot, a webhook fires an AWX job that pushes the configuration directly to the ALE switches.

```
Nautobot UI  ──webhook──►  AWX / Ansible  ──SSH──►  ALE OmniSwitch (AOS8)
   (nautobot-spb plugin)       (Playbooks)             (SPB Configuration)
```

---

## Features

- **Full SPB data model** in Nautobot: BVLANs, Services, SAPs, SDPs, Interfaces, ISIS instances, IPVPN Bindings & Redistributions, and Topologies
- **Dedicated SPB navigation tab** in Nautobot (Topology / Backbone / Layer 2 / Layer 3 / SAPs)
- **Device & Interface detail tabs**: SPB ISIS, SPB Interfaces, SPB Services, SPB Config — directly accessible from existing Nautobot device views
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

## Installation
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

