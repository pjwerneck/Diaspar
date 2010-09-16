#include <stdio.h>

int main(int argc, char *argv[]){

  FILE *fi, *fo;
  char *cp;
  int c;

  printf("hello\n");

  if ((cp = argv[1]) && *cp!='\0') {
    if ((fi = fopen(argv[2], "rb")) != NULL) {
      if ((fo = fopen(argv[3], "wb")) != NULL){
	printf("hello\n");
	while ((c = getc(fi)) != EOF) {
	  if (!*cp) cp = argv[1];
	  c ^= *(cp++);
	  putc(c, fo);
	}
	fclose(fo);
      }
      fclose(fi);
    }
  }
  return 0;
}
