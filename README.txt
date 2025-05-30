# How to build and run cse304-phase4

1. Build Docker image:
   docker build -t cse304-phase4 .

2. Create MyTest Folder
   mkdir -p Phase_IV_Tests/MyTest

3. Run Docker container:
   docker run -it --rm \
      -v $(pwd)/Phase_IV_Tests/basic_rascl:/app/tests \
      -v $(pwd)/Phase_IV_Tests/MyTest:/app/output \
      -v $(pwd)/src:/app/src \
      -w /app/src \
      cse304-phase4

4. When prompted, enter one of the test files, for example:
   T00_rascl_test_exprs1.rsc
   T02_rascl_test_exprs3.rsc
   T03_rascl_test_exprs4.rsc
   T71_Functions.rsc
   ...

5. Output .rsp and .rso files will appear in Phase_IV_Tests/MyTest
