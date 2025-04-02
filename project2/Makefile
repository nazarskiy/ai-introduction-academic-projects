OBJS = main.o path.o tmatrix.o bruteforce.o genetic.o
TARGET = bi-zum-salesman
CC = g++
CXXFLAGS = -Wall -O2 -std=c++17

all:	${OBJS}
	g++ -o ${TARGET} ${OBJS}

clean:
	rm -rf *.o ${TARGET}

