FROM public.ecr.aws/lambda/python:3.12

# WORKDIR ${LAMBDA_TASK_ROOT}

COPY . ./

RUN python3.12 -m pip install -r requirements.txt -t .

CMD ["upload.handler"]