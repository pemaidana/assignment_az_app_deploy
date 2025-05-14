# Azure

## Python libraries

To interact with Azure, we need a couple of Python libraries to be present in the system.

```bash
pip3 install ansible[azure] --user
pip3 install msrestazure
```

## Ansible Collections

We will also need the Ansible [collection for Azure](https://github.com/ansible-collections/azure#ansible-collection-for-azure).

```bash
ansible-galaxy collection install -r collections/requirements.yml
```

## Azure credentials
 
Please provide these variables; `subscription_id`, `client_id`, `secret` and `tenant` for the next steps.

- `AZURE_SUBSCRIPTION_ID`: [Find your Azure subscription](https://docs.microsoft.com/en-us/azure/media-services/latest/setup-azure-subscription-how-to?tabs=portal)
- `AZURE_CLIENT_ID` and `AZURE_TENANT`: [Register an application with Azure AD and create a service principal](https://docs.microsoft.com/en-us/azure/active-directory/develop/howto-create-service-principal-portal#register-an-application-with-azure-ad-and-create-a-service-principal)
- `AZURE_SECRET`: [Create a new application secret](https://docs.microsoft.com/en-us/azure/active-directory/develop/howto-create-service-principal-portal#option-2-create-a-new-application-secret)

### Create an Azure service principal

An Azure service principal gives you a dedicated account to manage Azure resources with Ansible.

Run the following code to create an Azure service principal using Azure CLI:

```bash
az ad sp create-for-rbac --name ansible \
            --role Contributor \
            --scopes /subscriptions/<subscription_id>
```

>[!NOTE]
>Store the password from the output in a secure location.


### Assign a role to the Azure service principal

By default service principals don't have the access necessary to manage resources in Azure.

Run the following command to assign the **Contributor** role to the service principal:

```bash
az role assignment create --assignee <appID> \
    --role Contributor \
    --scope /subscriptions/<subscription_id>
```

<p align="center">
<img src="./static/azure_app_secret.png">
</p>

### Grant the application access to a resource on Azure 

<p align="center">
<img src="./static/azure_app_grant1.png">
</p>


### Grant the application access to a resource on Azure - Assign roles

<p align="center">
<img src="./static/azure_app_grant2.png">
</p>


### Grant the application access to a resource on Azure - Assign members

<p align="center">
<img src="./static/azure_app_grant2.png">
</p>

## SSH Public key

You need to provide an SSH Key pair, so Azure can add the public SSH Key to `~/.ssh/authorized_keys` in the instances it creates. Ansible uses the Private Key to configure these instances after they are created.

```yaml
ssh_pubkey: 'ssh-rsa AAAAB3NzaC1y.....'
```

<p align="center">
<img src="./pictures/tower_SSH_Key.png">
</p>
