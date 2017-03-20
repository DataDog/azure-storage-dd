#azure
from azure.storage import CloudStorageAccount, Metrics

#package
from cli.storage_sas_generator import StorageSASGenerator


class StorageCLI(object):

    def __init__(self, sub_parsers):
        parser = sub_parsers.add_parser("storage", help="Commands to setup Azure Storage Monitoring with DD")
        storage_sub_parsers = parser.add_subparsers(help="commands")
        monitor_account_parser = storage_sub_parsers.add_parser(
            "monitor_storage_account", help="Setup storage account for DD monitoring")
        monitor_account_parser.add_argument(
            "storage_account_name", help="Name of the storage account")
        monitor_account_parser.add_argument(
            "storage_account_key", help="Primary Access key of the storage account")
        monitor_account_parser.set_defaults(func=self.setup_for_monitoring)

    def setup_for_monitoring(self, args):
        storage_account_name = args.storage_account_name
        storage_account_key = args.storage_account_key
        sc = StorageSASGenerator(storage_account_name, storage_account_key)
        sas_token = sc.get_token()
        self._turn_on_minute_metrics(storage_account_name, storage_account_key)
        print "One minute metrics have been enabled. Add the following to Datadog's Azure Storage integration configuration"
        print "Storage account: %s \nStorage SAS Token: %s" % (storage_account_name, sas_token)

    def _turn_on_minute_metrics(self, name, key):
        account = CloudStorageAccount(account_name=name, account_key=key, sas_token=None)
        metrics = Metrics(enabled=True, include_apis=True)
        table_service = account.create_table_service()
        table_service.set_table_service_properties(minute_metrics=metrics)
        blob_service = account.create_page_blob_service()
        blob_service.set_blob_service_properties(minute_metrics=metrics)
        file_service = account.create_file_service()
        file_service.set_file_service_properties(minute_metrics=metrics)
        queue_service = account.create_queue_service()
        queue_service.set_queue_service_properties(minute_metrics=metrics)


