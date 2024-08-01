#!/bin/bash

#set -e

ENV_FILE="examgpt_backend/.env"

if [ ! -f "${ENV_FILE}" ]; then
  echo "Error: ${ENV_FILE} not found. Are you running the script in the correct folder?"
  exit 1
fi

# Set environment variables from .env file if not already set
echo "Setting environment variables..."
while IFS= read -r line; do

    if [[ $line =~ ^# || -z $line ]]; then
        continue
    fi

    KEY=${line%%=*}
    VALUE=${line#*=}

    # Remove leading and trailing whitespace
    KEY=${KEY%% }
    KEY=${KEY## }
    VALUE=${VALUE%% }
    VALUE=${VALUE## }

    export "$KEY"="$VALUE"
done < $ENV_FILE


# echo "Building Solution..."
sam build 

# echo "Deploying Solution..."
sam deploy


