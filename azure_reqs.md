# Configure components to integrate Ansible with Azure Cloud

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

### Azure credentials
 
Please provide these variables; `subscription_id`, `client_id`, `secret` and `tenant` for the next steps.

- `AZURE_SUBSCRIPTION_ID`: [Find your Azure subscription](https://docs.microsoft.com/en-us/azure/media-services/latest/setup-azure-subscription-how-to?tabs=portal)
- `AZURE_CLIENT_ID` and `AZURE_TENANT`: [Configure Azure CLI on Linux VM and get the values](https://learn.microsoft.com/en-us/cli/azure/get-started-with-azure-cli?view=azure-cli-latest)
- `AZURE_SECRET`: [Create a new application secret, will be retrieved on next steps of this guide](https://docs.microsoft.com/en-us/azure/active-directory/develop/howto-create-service-principal-portal#option-2-create-a-new-application-secret)

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

## Get Azure service principal information

To authenticate to Azure with a service principal, you need the following information:

* SubscriptionID
* Service Principal ApplicationId
* Service Principal password
* TenantID

Run the following commands to get the service principal information:

```bash
az account show --query '{tenantId:tenantId,subscriptionid:id}';

az ad sp list --display-name ansible --query '{clientId:[0].appId}'
```

## Test service principal permissions

Run the following command to create a new Azure resource group:

```bash
ansible localhost -m azure_rm_resourcegroup -a "name=<resource_group_name> location=<resource_group_location>"
```

Replace `<resource_group_name>` and `<resource_group_location>` with your new resource group values.

```Output
[WARNING]: No inventory was parsed, only implicit localhost is available
localhost | CHANGED => {
    "changed": true,
    "contains_resources": false,
    "state": {
        "id": "/subscriptions/<subscriptionID>/resourceGroups/azcli-test",
        "location": "eastus",
        "name": "azcli-test",
        "provisioning_state": "Succeeded",
        "tags": null
    }
}
```

Run the following command to delete the Azure resource group:

```bash
ansible localhost -m azure_rm_resourcegroup -a "name=<resource_group_name> state=absent force_delete_nonempty=yes"
```

Replace `<resource_group_name>` with the name of your resource group.

```Output
[WARNING]: No inventory was parsed, only implicit localhost is available
localhost | CHANGED => {
    "changed": true,
    "contains_resources": false,
    "state": {
        "id": "/subscriptions/subscriptionID>/resourceGroups/azcli-test",
        "location": "eastus",
        "name": "azcli-test",
        "provisioning_state": "Succeeded",
        "status": "Deleted",
        "tags": null
    }
}

```

## Next steps:

Use Ansible playbook for managing Azure environments.
