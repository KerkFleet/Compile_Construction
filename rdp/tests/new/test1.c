int main(int z)
{
   int a,b,c;
   a=10;
   b=5;
   c=a+b;
   c=a*b;
   cout << "Enter a number between " << b << " and " << c << ": ";
   cin >> a >> b >> c;
   cout << "You entered: " << a;
   c=a+10;
   c = main();
   return 0;
}
