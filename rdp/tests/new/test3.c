int a,b,c,d;
int x,y;
int func(int a, int b)
{
  a = x/y + ( b-a);
  a = func(a, b);
  return 0;
}
int main()
{
   c=a+b*d;
   y = func(c, 5);
   return 0;
}

