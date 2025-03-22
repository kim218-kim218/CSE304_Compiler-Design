FROM python:3.9-slim

WORKDIR /src

COPY . /src


CMD [ "python", "src/lexer.py"  ]
# run python by using lexer.py