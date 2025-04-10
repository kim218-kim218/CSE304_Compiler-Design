FROM python:3.9-slim

WORKDIR /src

COPY . /src


CMD [ "python", "Phase_II_Tests/test_ST.py"  ]
