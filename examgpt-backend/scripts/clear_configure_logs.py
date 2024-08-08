import boto3

cloudwatch = boto3.client("logs")
log_group_name_prefix = "/aws/lambda/examgpt"

response = cloudwatch.describe_log_groups(logGroupNamePrefix=log_group_name_prefix)


# Loop through the log groups and delete their logs and set the retention
for log_group in response["logGroups"]:
    log_group_name = log_group["logGroupName"]
    print(f"Processing log group: {log_group_name}")

    # Get the list of log streams in the log group
    log_stream_response = cloudwatch.describe_log_streams(logGroupName=log_group_name)

    # Delete the logs from each log stream
    for log_stream in log_stream_response["logStreams"]:
        log_stream_name = log_stream["logStreamName"]
        cloudwatch.delete_log_stream(
            logGroupName=log_group_name, logStreamName=log_stream_name
        )
        print(f"Deleted logs from log stream: {log_stream_name}")

    # Set the log retention to 3 days
    cloudwatch.put_retention_policy(logGroupName=log_group_name, retentionInDays=3)
    print(f"Set log retention to 3 days for log group: {log_group_name}")

print("Done configuring log groups.")
