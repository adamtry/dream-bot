import os
from difflib import get_close_matches

import boto3
from mypy_boto3_dynamodb import ServiceResource
from mypy_boto3_dynamodb.service_resource import Table


def get_dynamodb_table(table_name: str) -> Table:
    """
    :param table_name: Name of the DynamoDB table to connect to (as on AWS)
    :return: A boto3 DynamoDB table object
    """
    # Env var is for local development, not set on AWS
    aws_profile = os.getenv("AWS_PROFILE")
    if aws_profile:
        boto3.setup_default_session(profile_name=aws_profile)

    db_resource: ServiceResource = boto3.resource("dynamodb")
    dynamo_table: Table = db_resource.Table(table_name)
    try:
        # Check that the table exists
        if dynamo_table.creation_date_time:
            print(f"Connected to DynamoDB table {table_name}")
    except dynamo_table.meta.client.exceptions.ResourceNotFoundException:
        valid_tables = [table.name for table in db_resource.tables.all()]
        raise ValueError(f" 🚨 Did not find table named: {table_name} 🚨\n"
                         f"Close matches: {get_close_matches(table_name, valid_tables)}")
    return dynamo_table
