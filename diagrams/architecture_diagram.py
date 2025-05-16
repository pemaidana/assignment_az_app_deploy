#!/usr/bin/env python3
from diagrams import Cluster, Diagram, Edge
from diagrams.azure.compute import VM, AutomanagedVM, AvailabilitySets
from diagrams.azure.network import LoadBalancers, NetworkSecurityGroupsClassic, VirtualNetworks, Subnets
from diagrams.onprem.container import Docker
from diagrams.onprem.network import Nginx
from diagrams.onprem.iac import Ansible
from diagrams.onprem.client import Users

# Create diagram with specified outformat and filename
with Diagram("Azure Web App Implemented by Ansible", show=False):
    
    # External Systems (outside Azure)
    admins = Users("Admins")
    ansible = Ansible("Ansible")
    app_users = Users("Application Users")
    
    # Azure Cloud Environment
    with Cluster("Azure Cloud"):
        azure_vnet = VirtualNetworks("Azure VNet")
        
        # Frontend Subnet
        with Cluster("Frontend Subnet"):
            frontend_nsg = NetworkSecurityGroupsClassic("Frontend NSG")
            lb = LoadBalancers("Azure Load Balancer\nPublic IP")
        
        # Backend Subnet
        with Cluster("Backend Subnet"):
            backend_nsg = NetworkSecurityGroupsClassic("Backend NSG")
            
            # Availability Set
            with Cluster("Availability Set"):
                avset = AvailabilitySets("Azure Availability Set")
                
                # VM01 with Docker and Nginx
                vm01 = VM("VM01\nNo Public IP")
                docker01 = Docker("Docker")
                nginx01 = Nginx("Nginx Demo")
                
                # VM02 with Docker and Nginx
                vm02 = VM("VM02\nNo Public IP")
                docker02 = Docker("Docker")
                nginx02 = Nginx("Nginx Demo")
                
                # VM Connections
                vm01 >> docker01 >> nginx01
                vm02 >> docker02 >> nginx02
                
                # VMs connected to Availability Set
                vm01 - avset
                vm02 - avset
        
        # Bastion Subnet
        with Cluster("AzureBastionSubnet"):
            bastion = AutomanagedVM("Azure Bastion")
    
    # Connect components
    lb >> Edge(label="TCP 443") >> backend_nsg
    backend_nsg >> Edge() >> vm01
    backend_nsg >> Edge() >> vm02
    
    # External connections
    admins >> Edge(label="SSH") >> bastion
    bastion >> Edge(label="SSH") >> vm01
    bastion >> Edge(label="SSH") >> vm02
    app_users >> Edge(label="HTTPS") >> lb

    # Ansible management
    ansible >> Edge(label="Management") >> azure_vnet
