FROM python:3.9-slim

# Create working directory
WORKDIR /app

# Create input/output folders
RUN mkdir -p /app/tests /app/output

# Copy source code
COPY src/ /app/src/

# Set working directory
WORKDIR /app/src

CMD [ "python", "parser.py"  ]
