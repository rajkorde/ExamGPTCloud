FROM public.ecr.aws/lambda/python:3.12

COPY . ./

RUN python3.12 -m pip install -r requirements.txt -t .

CMD ["chunker.handler"]