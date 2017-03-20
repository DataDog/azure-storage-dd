"""
CLI for Azure
"""

#stdlib
import argparse

# cli modules
from cli.storage_azure import StorageCLI

if __name__ == "__main__":

    tools = [
       StorageCLI,
    ]

    parser = argparse.ArgumentParser(
        description="Azure CLI to create/manage resource groups, namespaces, and generate data")
    sub_parsers = parser.add_subparsers(help="commands")
    for tool in tools:
        tool(sub_parsers)
    args = parser.parse_args()
    args.func(args)
