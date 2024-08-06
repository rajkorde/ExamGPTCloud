#!/bin/bash

# DEPRECATED: use store_env_in_cloud.py instead!
echo "DEPRECATED: use store_env_in_cloud.py instead!"

ENV_FILE="examgpt_backend/.env"
PROJECT_NAME="examgpt"
AWS_REGION=$(aws configure get region)

if [ ! -f "${ENV_FILE}" ]; then
  echo "Error: ${ENV_FILE} not found. Are you running the script in the correct folder?"
  exit 1
fi

while IFS= read -r line || [ -n "$line" ]; do
    if [[ $line =~ ^# || -z $line ]]; then
        continue
    fi

    # Extract the key-value pair
    KEY=${line%%=*}
    VALUE=${line#*=}

    # Remove leading and trailing whitespace
    KEY=$(echo "$KEY" | xargs)
    VALUE=$(echo "$VALUE" | xargs)

    aws ssm put-parameter --name "/${PROJECT_NAME}/${KEY}" --value "${VALUE}" --type "SecureString" --overwrite --region "${AWS_REGION}"

    echo "${KEY} key put in parameter store"
done < "${ENV_FILE}"