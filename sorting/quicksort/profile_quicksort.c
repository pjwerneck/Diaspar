#include <stdio.h>
#include <assert.h>
#include <math.h>
#include "utils.h"
#include <sys/time.h>
#include <stdlib.h>
#include <time.h>
#include "quicksort.h"
#include <malloc.h>

#define SAWTOOTH 0
#define RAND 1
#define STAGGER 2
#define PLATEAU 3
#define SHUFFLE 4
#define KILLER 5


int cmp(const void *a, const void *b){
  return (*(int*)a - *(int*)b);
}


int main(){
  int i, j, k, m, n, dist;
  int *data;

  for (n=100; n <= 100000; n*=10){
    data = malloc(sizeof *data * n);
    for (m=1; m < 2*n; m*=2){
      for (dist=0; dist < 5; dist++){
	for (i=j=0, k=1; i < n; i++){
	  switch (dist){
	  case SAWTOOTH: 
	    data[i] = i%m;
	    break;
	  case RAND:
	    data[i] = rand() % m;
	    break;
	  case STAGGER:
	    data[i] = (i*m + i) % n;
	    break;
	  case PLATEAU:
	    data[i] = i;
	    break;
	  case SHUFFLE:
	    data[i] = rand()%m? (j+=2): (k+=2);
	    break;
	  }
	}
	// sample done
	quicksort(data, n, sizeof(int), cmp);
      }
      
    }
    free(data);
  }




  printf("done!\n");
  return 0;
}
