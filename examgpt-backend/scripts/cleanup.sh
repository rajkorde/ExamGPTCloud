#! /bin/bash

# Delete all objects in bucket
bucket_name=$(aws s3 ls | grep "examgpt"| awk '{print $3}')
echo "Deleting objects from bucket: $bucket_name"
aws s3 rm s3://$bucket_name --recursive

# Delete all DynamoDB tables
tables=$(aws dynamodb list-tables --query "TableNames[]" --output text)

for table in $tables; do
  aws dynamodb delete-table --table-name $table --return-values NONE
  echo "Deleted table ${table}"
done
