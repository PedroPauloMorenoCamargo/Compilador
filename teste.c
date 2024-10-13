
{
    /*Logical operators*/
    int a, b;
    a = 1;
    b = 2;
    printf(1 && (a == a));
    printf(b && (a > 1));
    printf(0 || (a < 1));
    printf(a || (b < a));
    printf(!a);
    printf(!b);
    printf(!0);
}