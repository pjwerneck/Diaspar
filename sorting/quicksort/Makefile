
CC = gcc
CFLAGS += -std=gnu99 -Wall -gdwarf-2 -O3 #-g -pg
OBJS = quicksort.o utils.o test_quicksort.o profile_quicksort.o test_quicksort_with_struct.o fqsort.o
LDFLAGS = -g -lm #-pg

all: quicksort.o utils.o quicksort


default: all


quicksort: quicksort.o utils.o fqsort.o

test_quicksort: test_quicksort.o quicksort.o utils.o fqsort.o
test_quicksort_with_struct: test_quicksort_with_struct.o quicksort.o utils.o

profile_quicksort: profile_quicksort.o quicksort.o utils.o


clean:
	rm -f *.[oa]
	rm -f quicksort test_quicksort profile_quicksort
