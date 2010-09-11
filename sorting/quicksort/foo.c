/***************************************************************************
 *   Copyright (C) 2008 by Pedro Werneck   *
 *   pjwerneck@gmail.com   *
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 *   This program is distributed in the hope that it will be useful,       *
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
 *   GNU General Public License for more details.                          *
 *                                                                         *
 *   You should have received a copy of the GNU General Public License     *
 *   along with this program; if not, write to the                         *
 *   Free Software Foundation, Inc.,                                       *
 *   59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.             *
 ***************************************************************************/

/* 

   This implementation is based on ideas and optimization details from
   several sources. 
   Bentley and McIlroy "Engineering a sort function";
   Sedgwick's "Implementing quicksort Programs"; 
   "The Art of Computer Programming" Vol 3 and "Introduction to Algorithms";
   Also some lines of code borrowed from glibc qsort.c.


   Some of the implementation details

   1. Non-recursive, using an array as a fast inline stack of pointers
      to store the next partition. Macros implementing the push and
      pop operations are based on qsort.c.

   2. In-place partitioning, just storing start pointers and size of
      next partition to be sorted.

   3. Dynamic pivot selection, using the pseudomedian obtained from a
      3 elements random sample if n < MEDIAN3 and a 9 elements sample
      if n > MEDIAN3. This is based on Bentley and McIlroy, and
      althought it was the better approach for testing on several data
      samples, including malicious lists built to make a static chosen
      pivot go quadratic, I'm not sure if it works best for real data.

   4. The larger of the two partitions is always pushed on the stack
      first, so the algorithm work on the smaller partitions
      first. This limits stack size to no more than log (n)
      elements. Bentley and McIlroy judge this trick not worth the
      effort, but the implementation here was very simple.

   5. Partitions with n < MIN_PARTITION are sorted using insertionsort
      which is faster for small partially sorted data. Sedgewick does
      one big final insertionsort instead of several small, and I
      tested both cases under several conditions. Althought the
      difference was marginal, I opted for sorting small partitions
      since it demanded a few less comparisons. All insertionsort
      variants, including binary search insertionsort and shellsort
      did not performed better than the simplest implementation.
      Considering that final data is partially sorted in such a way
      that an element is not farther than MIN_PARTITION elements from
      its correct position, maybe something specific can perform
      better.

   6. The swapping operation is a bit of a hack, using the largest
      datatype within the size of the element and then reducing it as
      needed. This allowed the code to do much faster swapping than if
      doing it by byte-wise swapping, one char at a time like qsort.c
      does.

*/


#include <stdlib.h>
#include <math.h>
#include "quicksort.h"

/* Stack node to store array indexes for next calls */
typedef struct{
  char *start;
  int len;
} node;

/* These define some stack operations */ 
#define PUSH(low, high) ((top->start=low), (top->len=high), ++top)
#define POP(low, high) (--top, (low=top->start), (high=top->len))

#define STACK_SIZE (int)log2(len)
#define STACK_NOT_EMPTY (stack < top)
#define LEN_L ((p_high - p_start)/size)
#define LEN_R (len-LEN_L-1)
#define START_L (p_start)
#define START_R (p_start + (LEN_L+1)*size)


/* Use insertionsort when n < MIN_PARTITION

   Note that the value here, 15, is much higher than the value used by
   other implementations tested on different platforms. */
#define MIN_PARTITION 15

/* Use median of 3 pivot when n < MEDIAN3 */
#define MEDIAN3 40

/* Some useful macros */
#define RANDINT(from, to) ((rand() % (to-from)) + from)


// "smart" swapping.. 
static void swapsmart(void *a, void *b, size_t size){
  // this needs some serious optimization, but it works fine and
  // performs much better than inlined byte-wise swapping for large
  // data and the function call overhead on smaller data is not worth
  // the change... Bentley and McIlroy suggest using a macro to choose
  // the best swapping method
  while (size >= sizeof(double)){
    double tmpd;
    tmpd = *(double*)a;
    *(double*)a = *(double*)b;
    *(double*)b = tmpd;
    a += sizeof(double);
    b += sizeof(double);
    size -= sizeof(double);
  }
  while (size >= sizeof(int)){
    register int tmpi;
    tmpi = *(int*)a;
    *(int*)a = *(int*)b;
    *(int*)b = tmpi;
    a += sizeof(int);
    b += sizeof(int);
    
    size -= sizeof(int);
  }
  while (size >= sizeof(short)){
    register short tmps;
    tmps = *(short*)a;
    *(short*)a = *(short*)b;
    *(short*)b = tmps;
    a += sizeof(short);
    b += sizeof(short);
    size -= sizeof(short);
  }
  while (size--){
    register char tmpc;
    tmpc = *(char*)a;
    *(char*)a = *(char*)b;
    *(char*)b = tmpc;
    a += sizeof(char);
    b += sizeof(char);
  }
}


// get median of 3 numbers... technically this is a bubblesort :)
// Someone suggest using a macro for this, but the compiler will
// probably inline it snyway and the code spend so little time in this
// that it's not worth the effort

static char* median(char *a, 
		    char *b, 
		    char *c, 
		    size_t size, 
		    int(*cmp)(const void*, const void*)){
  if (cmp(a, b) > 0){
    swapsmart(a, b, size);
  }
  if (cmp(b, c) > 0){
    swapsmart(b, c, size);
  }
  else
    return b;
  if (cmp(a, b) > 0){
    swapsmart(a, b, size);
  }
  return b;
}


// let's play... 
void quicksort(void *data, 
	       size_t len, 
	       const size_t size, 
	       int (*cmp)(const void*, const void*)){

  node stack[STACK_SIZE];
  node *top = stack;

  char *p_start, *p_end, *p_high, *p_low;
  char *p_mid, *p_mid_a, *p_mid_b, *p_mid_c;

  // Let's do it...
  p_start = data;

  PUSH(p_start, len);
  while (STACK_NOT_EMPTY){
    POP(p_start, len);
    
    // if n < insertionsort threshold, pass and leave this chunk of
    // data to be sorted by the full insertionsort at the end
    if (len < MIN_PARTITION){
      
      for (p_low=(p_start+size); p_low < (p_start + len*size); p_low+=size)
	for (p_high=p_low; 
	     p_high > (p_start) && (cmp(p_high-size, p_high)>0); 
	     p_high-=size)
	  swapsmart(p_high, p_high-size, size);

      continue;
    } 
    // if n < median threshold, use pseudomedian given by a 3 elements
    // pseudorandom sample
    else if (len < MEDIAN3){
      p_mid_a = p_start+(rand()%len)*size;
      p_mid_b = p_start+(rand()%len)*size;
      p_mid_c = p_start+(rand()%len)*size;
      p_mid = median(p_mid_a, p_mid_b, p_mid_c, size, cmp);
    } 

    else {
      // if there is enough data to make it worth spend time and comparisons on
      // this, increase pseudomedian to a 9 elements pseudorandom sample
      
      p_mid_a = median(p_start, 
		       p_start+(rand()%len)*size, 
		       p_start+(rand()%len)*size, 
		       size, cmp);

      p_mid = p_start + (len/2)*size;
      p_mid_b = median(p_mid-(rand()%(len/2))*size, 
		       p_mid, 
		       p_mid+(rand()%(len/2))*size, 
		       size, cmp);

      p_end = p_start + (len-1)*size;
      p_mid_c = median(p_end-(rand()%(len-1))*size, 
		       p_end-(rand()%(len-1))*size, 
		       p_end, 
		       size, cmp);

      p_mid = median(p_mid_a, p_mid_b, p_mid_c, size, cmp);
    }
    
    // set vars to enter mainloop
    swapsmart(p_mid, p_start, size);
    
    p_end = p_start + len*size;
    p_low =  p_start;
    p_high = p_end;

    do {
      // The Bentley McIlroy algorithm implements a more complex
      // solution to deal with 
      do 
	(p_low += size); 
      while ((p_low < p_end) && cmp(p_low, p_start) < 0);
      
      do 
	(p_high -= size); 
      while (cmp(p_high, p_start) > 0);
      
      if (p_high > p_low)
	swapsmart(p_low, p_high, size);

    } while (p_high > p_low);
    swapsmart(p_start, p_high, size);

      
    

    // this switch-case and the flag were set here for the case I
    // would make a single insertionsort at the end and some extra
    // tweaking for each case... as I am still not sure of the best
    // thing to do, I'll leave it here... it works better than the
    // if-else if chain anyway...
    int sort_order = 0;
    
    sort_order += (LEN_L < MIN_PARTITION)*2;
    sort_order += (LEN_R < MIN_PARTITION)*4;
    
    if (LEN_L > LEN_R)
      sort_order += 8;
    else if (LEN_L < LEN_R)
      sort_order += 16;

    switch (sort_order){
    case 8:
      // L > R, both > M, push left first
      PUSH(START_L, LEN_L);
      PUSH(START_R, LEN_R);
      break;
    case 16:
      // R > L, both > M, push right first
      PUSH(START_R, LEN_R);
      PUSH(START_L, LEN_L);
      break;
    default:
      PUSH(START_L, LEN_L);
      PUSH(START_R, LEN_R);
      break;
    }
  }

}
