# Environment set up for NDFC (VXLAN) as Code Lab 

This lab is a companion to the NDFC-as-Code Digitized Delivery bootcamp. The tasks cover what tools are needed and how to install them in your environment. If you already have these tools installed, you can skip this and go directly to the lab guide itself.

## Setting up environment for the collection

Installation of a Python virtual environment is needed in order to install the collection and it's requirements. Ansible also has a dependency on the version of Python you run. We also want to install a version of Python outside of the system version of Python that may be installed on the system.

We recommend [pyenv](https://github.com/pyenv/pyenv) which provides a robust Python virtual environment capability that also allows for management of different Python versions. The following instructions are detailed around using pyenv. For pipeline execution please refer to the *pipeline section* which is documented at container level.

We also recommend installing Visual Studio Code from Microsoft for an Integrated Development Environment (IDE). You can download [`Visual Studio Code`](https://code.visualstudio.com/) from their site for the version of OS you are running.

Visual Studio Code also has the capabilities to add functionality through the use of Extensions. For the lab (and further use with NDFC as Code), we recommend installing the following extensions:

- [Ansible VSCode Extension](https://marketplace.visualstudio.com/items?itemName=redhat.ansible)
- [YAML](https://marketplace.visualstudio.com/items?itemName=redhat.vscode-yaml)

If you are running the the Windows Subsystem for Linux (WSL), then you may want to install this extension in your windows environment (where Linux is installed):

- [WSL](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-wsl)

### Step 1 - Installing the example repository

To simplify getting started with this collection we are providing you with an [example repository](https://github.com/netascode/ansible-dc-vxlan-example) that you can clone from GitHub.  This repository creates the required skeleton structure including examples needed to quickly get started using NDFC-as-Code. Cloning this repository requires the installation of [git client](https://git-scm.com/downloads) which is available for all platforms.

Run the following command in the location of interest.

```bash
git clone https://github.com/netascode/ansible-dc-vxlan-example.git nac-vxlan
```

This will clone the repository into the directory nac-vxlan.

### Step 2 - Create the virtual environment with pyenv

In this directory create a new virtual environment and install a Python version of your choice. At the _time of writing_, a commonly used version is Python version 3.12.10.  Command `pyenv install 3.12.10` will install this version. For detailed instructions please visit the [pyenv](https://github.com/pyenv/pyenv) site.

After you installed the Python version, you need to set it using the following commmand:

```bash
pyenv local 3.12.10
```

You can verify this is the Python version you are using with the following command:

```bash
python -V
```

Once your system has installed this version of Python, we can go ahead and create a virtual environment that we will use. To do this, we will need to run the following commands.

Change into the cloned directory:
```bash
cd nac-vxlan
```

Create a virtual environment in that directory:

```bash
python -m venv .
```

To move into that virtual environment, we need to run the following command:

```bash
source bin/activate
```

You should notice that your prompt has changed. It now reflects the virtual environment that you both created and are now in:

```bash
(nac_vxlan)  threnzy@THRENZY-M-W9PQ >
```

The `(nac_vxlan)` let's you know that you are in the virtual environment that you just created. To exit out of it, just type the following (don't do it at the moment, since we're going to be working in the virtual environment for the rest of the lab):

```bash
deactivate
```

Now we need to install some additional Python libraries needed to work with NDFC as Code which we will do in the next step.

### Step 3 - Install Ansible and additional required tools

Included in the example repository is the requirements file to install Ansible and other tools that we will use. Before doing the installation, we want to first upgrade PIP to latest version. (PIP is a Python package installer)

```bash
pip install --upgrade pip
```

Next, we will install the additional Python packages that we will need. You can install these individually or use a requirements file (`requirements.txt`) to tell Python what to install. This allows us to define multiple packages/libraries that we want Python to install.

In the cloned directory, you can see the `requirements.txt` file. If you open it up in VSCode, you can see the packages we want to install and even the versions of those packages. To install these packages, we will use the following command:

```bash
pip install -r requirements.txt
```

To verify what has been installed, you can run the following command:

```bash
pip list
```

One thing to note, though we specified certain packages for pip to install, those packages may have dependencies on other packages being installed. This is why you may see a list that is significantly more that what we defined in our `requirements.txt` file.


### Step 4 - Install Ansible Galaxy Collection 

_Please note_ that this step will fail if you are on our Corporate VPN - make sure you are disconnected before continuing. 

Ansible collections are the standard distribution format for sharing Ansible content. It allows the capability to install the required modules and plugins for Ansible (and our playbooks) to use them.

The default placement for Ansible Galaxy Collections is in your home directory under `~.ansible/collections/ansible_collections/`. For this lab, we are going to install them in the same directory that we are going to work in (the cloned on locally on your system). To install Galaxy Collection inside the repository you are creating with this example repository, you can run the following command:

```bash
ansible-galaxy collection install -p collections/ -r requirements.yaml
```

Since this is not the default behavior of where Ansible installs collections, you will need to configure your Ansible configuration (`ansible.cfg`) file to point to the correct collection location. 

This sets the correct path for all the Python modules and libraries in the virtual environment that was created. If you look in that directory you will find the collections package locations. Below is the base `ansible.cfg` file. You will need to adjust the `collections_path` to your environment paths:

```bash
[defaults]
collections_path = ./collections/
```

In the cloned repository, this modification has already been made.

### Step 5 - Change Ansible callbacks

If you wish to add any ansible callbacks ( the listed below expand on displaying time execution ) you can add the following to the `ansible.cfg` file:

```ini
callback_whitelist=ansible.posix.timer,ansible.posix.profile_tasks,ansible.posix.profile_roles
callbacks_enabled=ansible.posix.timer,ansible.posix.profile_tasks,ansible.posix.profile_roles
bin_ansible_callbacks = True
```

If you look at the `ansible.cfg` file in the cloned repository, you will see that these updates have already been made. 

### Step 6 - Verify the Ansible installation

Verify that the ansible configuration file is being read and all the paths are correct inside of this virtual environment. 

```bash
ansible --version
```

Your output should be somewhat similar to the output below, though there will be differences:

```bash
  ansible [core 2.17.10]
  config file = /Users/threnzy/Nexus_as_Code/network-as-code/nac-vxlan/ansible.cfg
  configured module search path = ['/Users/threnzy/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  ansible python module location = /Users/threnzy/Nexus_as_Code/nac_vxlan/lib/python3.11/site-packages/ansible
  ansible collection location = /Users/threnzy/Nexus_as_Code/network-as-code/nac-vxlan/collections
  executable location = /Users/threnzy/Nexus_as_Code/nac_vxlan/bin/ansible
  python version = 3.11.11 (main, Apr  3 2025, 21:26:26) [Clang 15.0.0 (clang-1500.3.9.4)] (/Users/threnzy/Nexus_as_Code/nac_vxlan/bin/python)
  jinja version = 3.1.6
  libyaml = True
```

### Step 7 - NDFC environment variables.

We now want to set up environment variables that our Ansible playbooks can reference in their playbooks. This will contain things like the IP address of the NDFC, username/password, and other information.

To created this in VSCode, you can go to `File` -> `New Text File`. This will open a new window within the VSCode environment. Once there, you can add the following:

```bash
export ND_HOST="198.18.133.100"
export ND_USERNAME="admin"
export ND_PASSWORD="C1sco12345"
export ND_DOMAIN="local"
export NDFC_SW_USERNAME="admin"
export NDFC_SW_PASSWORD="C1sco12345"
```

We can now save this file. Within VSCode, click on `File` -> `Save As` and then save it as `.env`. Once saved, you can source these environment variables with the following command:

```bash
source .env
```

These are now defined and you can verify them with the following command:
```bash
set | grep ND_HOST
```

This should provide you with the IP address you defined in the `.env` file.

We are now ready to do the rest of the tasks in the lab. You can find the lab guide on the [netascode](https://netascode.cisco.com/docs/guides/vxlan/nd/learning_lab/building-data-model/).

You can start from the section on "Working with the NaC Data Model" and go through to the section on "NaC Testing". 

Feel free to go through the rest of the scenarios throughout the site, including the Data Models for other technologies. We hope you enjoy the lab.
