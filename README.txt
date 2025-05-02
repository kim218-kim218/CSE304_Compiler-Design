# How to build and run phase3-parser-test

1. Build Docker image:
   docker build -t phase3-parser-test .

2. Create MyTest Folder
   mkdir -p Phase_III_Tests/MyTest

3. Run Docker container:
   docker run -it --rm \
      -v $(pwd)/Phase_III_Tests/basic_rascl:/app/tests \
      -v $(pwd)/Phase_III_Tests/MyTest:/app/output \
      -v $(pwd)/src:/app/src \
      -w /app/src \
      phase3-parser-test

4. When prompted, enter one of the test files, for example:
   T00_rascl_test_exprs1.rsc
   T02_rascl_test_exprs3.rsc
   T03_rascl_test_exprs4.rsc
   ...

5. Output .rsp files will appear in Phase_III_Tests/MyTest
