#include <stdio.h>
#include <stdlib.h>


int randint(int from, int to){
  return (int)(rand() % (to-from)) + from;
}


void swap(int* x, int* y){
  int t;
  t = *x;
  *x = *y;
  *y = t;
}


void populate(int* data, int n){
  int i;
  for (i=0; i < n; i++)
    data[i] = i;
}


void shuffle(int* data, int n){
  int i;
  for (i=0; i < n-1; i++)
    swap(&data[i], &data[randint(i+1, n)]);
}


int check(int* data, int n){
  int i;
  int comp[n];

  populate(comp, n);

  for (i=0; i < n; i++){
    if (data[i] != comp[i])
      return 0;
  }
  return 1;
}

void printsample(int *sample, int n){
  int i;
  printf("[");
  if (n > 0){
    for (i=0; i < n-1; i++){
      printf("%d, ", sample[i]);
    }
    printf("%d", sample[n-1]);
  }
  printf("]\n");
}


int permute(int* values, int n){
  /* generate the permutations to find the median of 3 */
  int k = n-1;
  int m = n-1;

  while((k > 0) && (values[k] <= values[k-1]))
    k--;

  k--;

  if(k < 0)
    return 0;

  m = n-1;
  while((m > k) && (values[m] <= values[k]))
    m--;

  swap(&values[k], &values[m]);

  n--;
  k++;

  while(n > k){
    swap(&values[n], &values[k]);
    k++;
    n--;
  }

  return 1;
}


int median(int* data, int start, int n){
  int i[3];
  i[0] = start;
  i[1] = start+(n-1);
  i[2] = start+(n/2);

  do {
    if (
        ((data[i[0]] <= data[i[1]]) && (data[i[1]] <= data[i[2]]))
        ||
        ((data[i[2]] <= data[i[1]]) && (data[i[1]] <= data[i[0]]))
        )
      break;
  }
  while (permute(i, 3));
  return i[1];

}
