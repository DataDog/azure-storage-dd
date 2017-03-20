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


6. To turn on one minute metrics for transactions and to generate a read-only SAS token for your Storage account, run the script with the account name and primary access key:

    ```
    python azure_cli.py storage monitor_storage_account "{storage account name}" "{storage account primary access key}"
    ```

7. Navigate to the [Azure Storage integration tile](https://app.datadoghq.com/account/settings#integrations/azure_storage) in Datadog and copy and paste into the configuration the account name and account SAS token that was output from the script.

8. Continue doing this for each storage account and then once done, click Update Configuration.

9. To exit the python virtual environment, the shell command is `deactivate`