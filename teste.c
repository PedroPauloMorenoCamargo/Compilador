


int soma(int x) {

  if (x < 3) {
    printf(x);
    soma(x+1);
  }
  return 0;
}

void main() {
  soma(1);
}