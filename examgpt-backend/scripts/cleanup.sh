#! /bin/bash

# Delete all objects in bucket
bucket_name=$(aws s3 ls | grep "examgpt"| awk '{print $3}')
echo "Deleting objects from bucket: $bucket_name"
aws s3 rm s3://$bucket_name --recursive

# Delete all items in all DynamoDB tables
tables=$(aws dynamodb list-tables --query "TableNames[]" --output text)

for table in $tables
do
  echo "Processing table: $table"

  # Scan the table and get all items
  items=$(aws dynamodb scan --table-name $table --attributes-to-get "exam_id" --query "Items[].exam_id.S" --output text)

  echo "Found $items items in table: $table"

  for item in $items
  do
    echo "Deleting item: $item from table: $table"

    # Delete each item by primary key
    aws dynamodb delete-item --table-name $table --key '{"exam_id": {"S": "'$item'"}}'
  done

  echo "All items deleted from table: $table"
done