BEGIN { count = 0 }
{ if (count % 3 == 0) printf("\n") }
{ print $0 ; count++ }
END { printf("----------\n") }
