#! /bin/bash

bucket_name=$(aws s3 ls | grep "examgpt"| awk '{print $3}')
echo "Deleting objects from bucket: $bucket_name"
aws s3 rm s3://$bucket_name --recursive