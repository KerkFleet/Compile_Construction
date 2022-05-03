int a,b;

int func(){
    int c, d;
    cout << "Enter a number ";
    cin >> a;
    b=10;
    d=20;
    c=d+a*b;
    cout << "The answer is " << c << endl;
    return 0;
}

int main(){
    a = func();
    return 0;
}