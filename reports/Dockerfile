FROM amazon/aws-lambda-python

WORKDIR ${LAMBDA_TASK_ROOT}

# Copy requirements.txt
COPY requirements.txt .

# Install the specified packages
RUN pip install -r requirements.txt

# Copy function code
COPY summary_queries_func.py .
COPY summary_script.py .


# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "summary_script.handler" ]
