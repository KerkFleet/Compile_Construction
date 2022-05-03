int a,b;
int double(int x){
    int y;
    y = x;
    y = 2 * x;
    return y;
}

int main(){
    b = 5;
    a = double(b);
    cout << a << endl;
    return 0;
}