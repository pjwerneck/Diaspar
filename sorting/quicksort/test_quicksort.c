#include <stdio.h>
#include <assert.h>
#include <math.h>
#include "utils.h"
#include <sys/time.h>
#include <stdlib.h>
#include <time.h>
#include "quicksort.h"
#include "fqsort.h"

/* testing ... */


int cmpcount1 = 0;
int cmpcount2 = 0;

int elapsed(struct timeval startTime, struct timeval endTime ) {
  return (endTime.tv_sec - startTime.tv_sec ) * 1000000 + (endTime.tv_usec - startTime.tv_usec );
}

int cmp1(const void *a, const void *b){
  cmpcount1 += 1;
  return (*(int*)a - *(int*)b);
}

int cmp2(const void *a, const void *b){
  cmpcount2 += 1;
  return (*(int*)a - *(int*)b);
}

int ncmp(const void *a, const void *b){
  return (*(int*)a - *(int*)b);
}


/* sample functions */


void range(int* data, int n){
  populate(data, n);
}

void rrange(int* data, int n){
  int i;
  for (i=0; i < n; i++)
    data[i] = n-i-1;
}

void fullrand(int* data, int n){
  int i;
  for (i=0; i < n; i++)
    data[i] = randint(0, 100);
}

void randbin(int* data, int n){
  populate(data, n);
  shuffle(data, n);
  int i;
  for (i=0; i < n; i++)
    data[i] = data[i]%2;
}

void sample(int* data, int n){
  populate(data, n);
  shuffle(data, n);
}

void unique(int* data, int n){
  int i;
  for (i=0; i < n; i++)
    data[i] = 1;
}

void killer(int* data, int n){
  
  int i, m, u, even, odd;
  int steps[n/2 - 1];
  
  u = (int)log2(n);
  
  even = 0;
  for (m=0; m < u-1; m++){
    for (i=(int)pow(2, m)-1; i < n/2; i += (int)pow(2, (m+1))){
      steps[i] = even;
      even += 2;
    }
  }

  for (i=0; i < n/2 - 1; i++)
    data[i] = steps[i];

  data[i++] = n-1;

  for (odd=1; odd < n-1; odd+=2, i++)
    data[i] = odd;
  
  data[i] = n - 2;

}



int test_sort(void (*samplefunc)(), 
	      void (*sortfunc)(), 
	      int (*cmpfunc)(), 
	      char *samplename, 
	      char *sortname, 
	      int n, 
	      int t, 
	      float seed,
	      int* cmpcount){

  struct timeval startTime, endTime;
  float total = 0.0;
  int i, v, j, cmplimit;
  v = 0;
  cmplimit = n * log10(n);
  for (i=0; i < t; i++){
    int datatest[n];
    int data[n];
    srand(seed+=10);
    samplefunc(data, n);
    for (j=0; j < n; j++){
      datatest[j] = data[j];
    }

    qsort(datatest, n, sizeof(int), ncmp);
    //printsample(data, n);
    gettimeofday(&startTime, 0 );
    sortfunc(data, n, sizeof(int), cmpfunc);
    //quicksort(data, n, sizeof(int), cmp);
    //insertionsort(data, (char*)&data[0], n, sizeof(int), cmp);
    gettimeofday(&endTime, 0 );
    
    for (j=0; j < n; j++){
      v = (data[j] == datatest[j]);
      if (!v){
	printf("Failed, %s, %s, i=%d\n", sortname, samplename, j);
	printsample(data, n);
	printsample(datatest, n);
	break;
      }
    }
    assert(v);

    total += (int)elapsed(startTime, endTime);
  }
  *cmpcount /= t;
  printf("%2s, %s(%d): %0.2f usec, %d cmps", sortname, samplename, n, (total/t), *cmpcount);
  
  printf(" (%0.3f n log n)\n", ((float)*cmpcount/cmplimit));

  return total/t;
}





int main(int argc, char* argv[]){

  //  int n = 2 << 10;
  int n = 2 << 18;
  int t = 10;
  int a, b, v, i;
  int seed = time(0);
  printf("\n");


  i = 0;
  v = 0;
  
  // full randomized sample
  a = test_sort(fullrand, quicksort, cmp2, "fullrand", " quicksort", n, t, seed, &cmpcount2);
  b = test_sort(fullrand, _quicksort, cmp1, "fullrand", "_quicksort", n, t, seed, &cmpcount1);
  printf("tdiff: %d usec, cmpdiff: %d, %0.3f\n\n", (a-b), (cmpcount2-cmpcount1), (float)cmpcount2/(float)cmpcount1);  v += (a-b); i++;
  cmpcount1=0;
  cmpcount2=0;


  // randomized 2 keys (0, 1) sample
  a = test_sort(randbin, quicksort, cmp2, "randbin", " quicksort", n, t, seed, &cmpcount2);
  b = test_sort(randbin, _quicksort, cmp1, "randbin", "_quicksort", n, t, seed, &cmpcount1);
  printf("tdiff: %d usec, cmpdiff: %d, %0.3f\n\n", (a-b), (cmpcount2-cmpcount1), (float)cmpcount2/(float)cmpcount1);  v += (a-b); i++;
  cmpcount1=0;
  cmpcount2=0;
  
  // randomized unique keys sample
  a = test_sort(sample, quicksort, cmp2, "sample", " quicksort", n, t, seed, &cmpcount2);
  b = test_sort(sample, _quicksort, cmp1, "sample", "_quicksort", n, t, seed, &cmpcount1);
  printf("tdiff: %d usec, cmpdiff: %d, %0.3f\n\n", (a-b), (cmpcount2-cmpcount1), (float)cmpcount2/(float)cmpcount1);
  v += (a-b); i++;
  cmpcount1=0;
  cmpcount2=0;

  // ordered 0...n range
  a = test_sort(range, quicksort, cmp2, "range", " quicksort", n, t, seed, &cmpcount2);
  b = test_sort(range, _quicksort, cmp1, "range", "_quicksort", n, t, seed, &cmpcount1);
  printf("tdiff: %d usec, cmpdiff: %d, %0.3f\n\n", (a-b), (cmpcount2-cmpcount1), (float)cmpcount2/(float)cmpcount1);  v += (a-b); i++;
  cmpcount1=0;
  cmpcount2=0;


  // ordered n...0 range
  a = test_sort(rrange, quicksort, cmp2, "rrange", " quicksort", n, t, seed, &cmpcount2);
  b = test_sort(rrange, _quicksort, cmp1, "rrange", "_quicksort", n, t, seed, &cmpcount1);
  printf("tdiff: %d usec, cmpdiff: %d, %0.3f\n\n", (a-b), (cmpcount2-cmpcount1), (float)cmpcount2/(float)cmpcount1);  v += (a-b); i++;
  cmpcount1=0;
  cmpcount2=0;


  // unique key sample
  a = test_sort(unique, quicksort, cmp2, "unique", " quicksort", n, t, seed, &cmpcount2);
  b = test_sort(unique, _quicksort, &cmp1, "unique", "_quicksort", n, t, seed, &cmpcount1);
  printf("tdiff: %d usec, cmpdiff: %d, %0.3f\n\n", (a-b), (cmpcount2-cmpcount1), (float)cmpcount2/(float)cmpcount1);  v += (a-b); i++;
  cmpcount1=0;
  cmpcount2=0;


  // "qsort killer" malicious sample
  a = test_sort(killer, quicksort, cmp2, "killer", " quicksort", n, t, seed, &cmpcount2);
  b = test_sort(killer, _quicksort, cmp1, "killer", "_quicksort", n, t, seed, &cmpcount1);
  printf("tdiff: %d usec, cmpdiff: %d, %0.3f\n\n", (a-b), (cmpcount2-cmpcount1), (float)cmpcount2/(float)cmpcount1);  v += (a-b); i++;
  cmpcount1=0;
  cmpcount2=0;

  printf("avg: %d\n\n", v/i);
  
  
  return 0;
}


