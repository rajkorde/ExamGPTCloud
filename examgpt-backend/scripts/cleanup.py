import sys

import boto3
from tqdm import tqdm


def delete_s3_bucket_contents(bucket_name: str):
    s3 = boto3.resource("s3")
    bucket = s3.Bucket(bucket_name)

    print(f"Deleting all objects in bucket: {bucket_name}")
    for obj in tqdm(bucket.objects.all()):
        obj.delete()
        print(f"Deleted object: {obj.key}")

    # Scan the table and delete all items


def delete_dynamodb_table_items(table_name):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(table_name)

    print(f"Deleting all items in table: {table_name}")

    key_schema = table.key_schema
    scan = table.scan()
    with table.batch_writer() as batch:
        for item in tqdm(scan["Items"]):
            key = {
                attr["AttributeName"]: item[attr["AttributeName"]]
                for attr in key_schema
            }
            batch.delete_item(Key=key)

    # Continue scanning and deleting if there are more items
    while "LastEvaluatedKey" in scan:
        scan = table.scan(ExclusiveStartKey=scan["LastEvaluatedKey"])
        with table.batch_writer() as batch:
            for item in tqdm(scan["Items"]):
                key = {
                    attr["AttributeName"]: item[attr["AttributeName"]]
                    for attr in key_schema
                }
                batch.delete_item(Key=key)


def main():
    # Initialize boto3 clients
    s3_client = boto3.client("s3")
    dynamodb_client = boto3.client("dynamodb")

    # List and process S3 buckets
    s3_buckets = s3_client.list_buckets()["Buckets"]
    for bucket in s3_buckets:
        if "examgpt" in bucket["Name"].lower():
            print(f"Found matching S3 bucket: {bucket['Name']}")
            delete_s3_bucket_contents(bucket["Name"])
        else:
            print(f"Skipping S3 bucket: {bucket['Name']}")

    # List and process DynamoDB tables
    dynamodb_tables = dynamodb_client.list_tables()["TableNames"]
    for table in dynamodb_tables:
        if "examgpt" in table.lower():
            print(f"Found matching DynamoDB table: {table}")
            delete_dynamodb_table_items(table)
        else:
            print(f"Skipping DynamoDB table: {table} (does not contain 'examgpt')")


if __name__ == "__main__":
    main()
    print("Cleanup completed.")
