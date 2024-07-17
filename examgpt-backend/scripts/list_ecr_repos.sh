#! /bin/bash

aws ecr describe-repositories --query 'repositories[].repositoryName' --output table