int a;
int b;
int theSum;
int bignum;

function int dude(int a, int b)
{
    theSum = a * a + b * b;
    return theSum;
}

main () {
  a = 5;
  b = 10;

  bignum = dude(a, b);
  print bignum;
}
