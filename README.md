## About this script
Currently, Azure doesn't enable storage metrics by default for each storage account.  In addition, minute level transaction metrics can only be enabled for a storage account using Powershell or programmatically.

In order for Datadog to gather metrics from your Azure Storage accounts, this needs to be enabled for each account you want to monitor. Since the storage account metrics are stored in tables in your storage account, we also need read access on your tables to query them for the metrics.

With the storage account name and primary access key, this script will turn on minute level metrics and generate a service level SAS token which will have read-only access for tables only for the respective storage account.

After enabling minute level metrics for a storage account, it can take Azure up to one hour to initially generate the tables. Metrics will not show up in Datadog until after that process completes.

### Warning
This will turn on minute level metrics for your storage account, which will create additional tables in your account. Azure charges you for the amount of data stored in an account. We allow you to define the length of the retention period in Azure for these tables, so we recommend a small period like 2 days to help minimize costs.  You can read more about charges associated with storage metrics on the official [azure-docs repo for storage](https://github.com/Microsoft/azure-docs/blob/master/articles/storage/storage-enable-and-view-metrics.md#what-charges-do-you-incur-when-you-enable-storage-metrics)

## To run this script

1. This script requires python, so please install it if you don't already have it. [Install Python](https://www.python.org/downloads/).

2. Since this depends on the [azure-storage](https://github.com/Azure/azure-storage-python) library, we recommend that you use a [virtual environment](https://docs.python.org/3/tutorial/venv.html) to run the script.  Here is how:

    ```
    pip install virtualenv
    virtualenv ddazurestorage
    cd ddazurestorage
    source bin/activate
    ```

3. Next clone the repository.

    ```
    git clone https://github.com/Datadog/azure-storage-dd.git
    ```

4. Install the azure-storage dependency using pip.

    ```
    cd azure-storage-dd
    pip install -r requirements.txt
    ```

5. Go to the storage account you want to integrate in the [Azure Portal](https://portal.azure.com) and navigate to Access Keys under the Settings section.
![Example Storage Account](/img/azure-storage-example.png)


6. To turn on one minute metrics for transactions and to generate a read-only SAS token for your Storage account, run the script with the account name and primary access key.:

    ```
    python azure_cli.py storage monitor_storage_account "{storage account name}" "{storage account primary access key}" "{number of days for retention period in Azure}"
    ```
    For easy input:

    ```
    python azure_cli.py storage monitor_storage_account "" "" "2"
    ```

7. Navigate to the [Azure Storage integration tile](https://app.datadoghq.com/account/settings#integrations/azure_storage) in Datadog and copy and paste into the configuration the account name and account SAS token that was output from the script.

8. Continue doing this for each storage account and then once done, click Update Configuration.

9. To exit the python virtual environment, the shell command is `deactivate`