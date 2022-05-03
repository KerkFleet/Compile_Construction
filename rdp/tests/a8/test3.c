int a,b,d;
int fun(int a, int b, int d){
    int c;
    c= a*b+d;
    cout << "The answer is " << c << endl;
    return 0;
}

int main(){
    a=5;
    b=10;
    d=20;
    a=fun(b,d,a);
    return 0;

}