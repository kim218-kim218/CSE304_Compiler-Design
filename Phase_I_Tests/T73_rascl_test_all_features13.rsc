int a;
int b;
int bignum;
int sqr;
float avg;
int numbers[5];
int even;
int index;

function int isEven (int val) {
    if (val == 0) {
       return 1
    } else {
      if (val == 1) {
       return 0
       } else {
          return isEven((val - 2))
       }
    }
}


function void outputArray(int nums[], int length) {
    int index;
    index = 0;
    while (index < length) {
       print nums[index]
   }
}
function int dummy() 
{
  index = 0;
  even = 0;

  numbers[0] = 50;
  numbers[1] = -52;
  numbers[2] = -12;
  numbers[3] = 31;
  numbers[4] = -17;
  call outputArray(numbers, 5);

  index = 0;  
  while !(numbers[index] == -101) && (index < 5) {
     if (numbers[index] > 0) && (isEven(numbers[index]) == 1) {
         print numbers[index]
     }
  }

}

main() {
   print even
}
