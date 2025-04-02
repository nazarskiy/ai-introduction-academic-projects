//---------------------------------------------------------------------------
//
//  Template for solving the Travelling Salesman Problem
//  (c) 2021 Ladislava Smítková Janků <ladislava.smitkova@fit.cvut.cz>
//
//  genetic.cpp: Implementation of genetic algorithm with these parameters:
//
//  Population:        500 individuals (can be modified by POPULATION constant)
//  Generations:       30 (can be modified by GENERATIONS constant)
//  Crossover method:  OX or PMX
//  Mutation method:   reversion of the path
//
//  Crossover probability:    95%  (PROBABILITY_CROSSOVER)
//  Mutation probability:     stepped by 5%  (PROBABILITY_MUT_STEP)
//
//  If the fitness value of the actual generation is better than last one,
//  mutation probability will be set to zero. In other case, mutation
//  probability will be increased by PROBABILITY_MUT_STEP.
//
//---------------------------------------------------------------------------

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <limits.h>
#include <algorithm>
#include <map>

#include "genetic.h"
#include "path.h"

#define POPULATION              100
#define PROBABILITY_CROSSOVER   0.95
#define PROBABILITY_MUT_STEP    0.05
#define GENERATIONS             200

typedef struct {
    std::vector<int> path;
    double fitness;
    double Pr;
    double q;
} TIndividual;

std::vector<TIndividual> individuals;

bool compareByFitness( const TIndividual &a, const TIndividual &b)
{
    return a.fitness > b.fitness;
}

double computeFitness( const std::vector<int> &path, TMatrix *matrix)
{
    //****************************************************************
    // ZDE IMPLEMENTUJTE FITNESS
    int distanceSum = calculatePathLength(path, matrix);
    if (distanceSum <= 0) distanceSum = 1;
    return 1.0 / distanceSum;
    //****************************************************************
}

void recalculate( TMatrix *matrix)
{
    // calculate fitness and Pr
    double sum_fitness = 0;
    for (auto ind = individuals.begin(); ind != individuals.end(); ++ind) {
        ind->fitness = computeFitness( ind->path, matrix);
        sum_fitness += ind->fitness;
    }

    // sort population by fitness
    std::sort( individuals.begin(), individuals.end(), compareByFitness);

    // compute Pr_i and q_i
    double q = 0;
    for (auto ind = individuals.begin(); ind != individuals.end(); ++ind) {
        ind->Pr = ind->fitness / sum_fitness;
        q += ind->Pr;
        ind->q = q;
    }
}

// tournament selection
void selection()
{
    //printf("Entering selection\n");
    std::vector<TIndividual> newGeneration;

    for (auto i=0; i<POPULATION; i++)
    {
		//****************************************************************
		// ZDE IMPLEMENTUJTE SELEKCI (tvorba nove generace)
		//

        TIndividual best;
        bool flag = true;
        int k = rand() % 3;
        k += 3;
        for (int j = 0; j < k; j++) {
            int randomIndex = rand() % individuals.size();
            TIndividual &competitor = individuals[randomIndex];

            if (flag || competitor.fitness > best.fitness) {
                best = competitor;
                flag = false;
            }
        }

        newGeneration.push_back(best);
        // newGeneration.push_back( ... );
		//****************************************************************
    }

    // new generation was borned
    individuals = newGeneration;
}

bool pathContainsCity( const std::vector<int> &path, int city)
{
    for (auto x = path.begin(); x != path.end(); ++x) {
        if (city == *x) return true;
    }
    return false;
}

std::pair<int, int> randomSwath(int size) {
    if (size < 3) return std::make_pair(0, std::max(1, size - 1));
    int num1 = rand() % size;
    int num2 = rand() % size;
    while ((num1 == num2) || (abs(num1 - num2) < 2)) {
        num2 = rand() % size;
    }
    if (num1 > num2) std::swap(num1, num2);
    return std::make_pair(num1, num2);
}

int fillUpEnd(TIndividual &son, TIndividual &donor, TIndividual &dummyson, int size, int swathStart, int swathEnd) {
    int flag = swathEnd;
    int index = swathEnd + 1;

    for (int i = swathEnd + 1; i < size; i++) {
        if (!pathContainsCity(dummyson.path, donor.path[i])) {
            dummyson.path.push_back(donor.path[i]);
            son.path[index++] = donor.path[i];
            flag++;
        }
    }

    if (flag == size) return 0;

    int i = 0;
    for (; i <= swathEnd; i++) {
        if (!pathContainsCity(dummyson.path, donor.path[i])) {
            if (index >= size) break;
            dummyson.path.push_back(donor.path[i]);
            son.path[index++] = donor.path[i];
        }
        if (index == size) break;
    }

    return i;
}

void fillUpStart(TIndividual &son, TIndividual &donor, TIndividual &dummyson, int size, int swathStart, int swathEnd, int idx) {
    int i = idx;
    int index = 0;
    for (; i <= swathEnd; i++) {
        if (!pathContainsCity(dummyson.path, donor.path[i])) {
            dummyson.path.push_back(donor.path[i]);
            son.path[index++] = donor.path[i];
        }
    }
}

void doCrossoverOX(std::vector<TIndividual> &result, TMatrix *matrix, TIndividual &a, TIndividual &b) {
    TIndividual aa = a;
    TIndividual bb = b;

    int size = matrix->getNumberOfTargets();
    std::pair<int, int> swath = randomSwath(size);

    TIndividual dummyaa, dummybb;

    for (int i = swath.first; i <= swath.second; i++) {
        aa.path[i] = a.path[i];
        dummyaa.path.push_back(a.path[i]);
        bb.path[i] = b.path[i];
        dummybb.path.push_back(b.path[i]);
    }

    int idxs1 = fillUpEnd(aa, b, dummyaa, size, swath.first, swath.second);
    int idxs2 = fillUpEnd(bb, a, dummybb, size, swath.first, swath.second);

    fillUpStart(aa, b, dummyaa, size, swath.first, swath.second, idxs1);
    fillUpStart(bb, a, dummybb, size, swath.first, swath.second, idxs2);

    result.push_back(aa);
    result.push_back(bb);
}

void insertWithMaping(TIndividual &son, const std::map<int, int> &maping, int index) {
    int curr = son.path[index];
    while (maping.find(curr) != maping.end()) {
        curr = maping.at(curr);
    }
    son.path[index] = curr;
}

void doCrossoverPMX(std::vector<TIndividual> &result, TMatrix *matrix, TIndividual &a, TIndividual &b) {
    TIndividual aa, bb;

    aa = a;
    bb = b;

    int size = matrix->getNumberOfTargets();
    std::pair<int, int> swath = randomSwath(size);
    std::map<int, int> AtoB, BtoA;

    //****************************************************************
    // ZDE IMPLEMENTUJTE OPERATOR KRIZENI PMX

    for (int i = swath.first; i <= swath.second; i++) {
        aa.path[i] = b.path[i];
        bb.path[i] = a.path[i];
        AtoB[b.path[i]] = a.path[i];
        BtoA[a.path[i]] = b.path[i];
    }

    for (int i = 0; i < size; i++) {
        if (i < swath.first || i > swath.second) {
            if (std::find(aa.path.begin() + swath.first, aa.path.begin() + swath.second + 1, aa.path[i]) != aa.path.end()) {
                insertWithMaping(aa, AtoB, i);
            }
        }
    }
    for (int i = 0; i < size; i++) {
        if (i < swath.first || i > swath.second) {
            if (std::find(bb.path.begin() + swath.first, bb.path.begin() + swath.second + 1, bb.path[i]) != bb.path.end()) {
                insertWithMaping(bb, BtoA, i);
            }
        }
    }
    //****************************************************************

    // propagate only childs
    result.push_back( aa);
    result.push_back( bb);
}


void crossover( TMatrix *matrix, TCrossoverMethod crossoverMethod)
{
    std::vector<TIndividual> crossovered;
    std::vector<TIndividual>::iterator candidate = individuals.end();

    for (auto ind = individuals.begin(); ind != individuals.end(); ++ind) {
        // select candidates to the crossover process
        if (drand48() <= PROBABILITY_CROSSOVER) {
            if (candidate == individuals.end()) {
                // this is the first parent
                candidate = ind;
            }
            else {
                // now we have both parents, we can do crossover
                if (crossoverMethod == CROSSOVER_METHOD_PMX)
                    doCrossoverPMX( crossovered, matrix, *ind, *candidate);
                else
                    doCrossoverOX( crossovered, matrix, *ind, *candidate);

                candidate = individuals.end();
            }
        }
        else
            crossovered.push_back( *ind);
    }

    // If we got odd number of parents, do nothing with this candidate and push it directly
    // into the new generation.
    if (candidate != individuals.end())
        crossovered.push_back( *candidate);

    // crossover is done
    individuals = crossovered;
}

void mutation( double probability)
{
    for (auto ind = individuals.begin(); ind != individuals.end(); ++ind) {
        if (drand48() <= probability) {

			//****************************************************************
			// ZDE IMPLEMENTUJTE OPERATOR MUTACE
            // INVERSION
            int size = ind->path.size();
            if (size < 2) continue;
            std::pair<int, int> ids = randomSwath(size);

            std::reverse(ind->path.begin() + ids.first, ind->path.begin() + ids.second + 1);
            //****************************************************************

        }
    }
}

void printState( int generation)
{
    //("printing the state..., %lld\n", -individuals.at(0).fitness);
    printf("[%d]  %lf\n", generation, -individuals.at(0).fitness);
}

std::vector<int> salesmanProblemGenetic(TMatrix *matrix, TCrossoverMethod crossoverMethod)
{
    //printf("Inside salesmanProblemGenetic\n");
    unsigned i, j;
    int x;
    std::vector<int>::iterator p;
    double mutation_probability = 0;
    double lastFitness = -std::numeric_limits<double>::max();
    std::vector<int> best;
    double bestFitness = -std::numeric_limits<double>::max();

    // initialization of random number generator
    srand( getpid());
    // born first population
    for (i=0; i<POPULATION; i++) {
        //printf("Entering Generation %d\n", i);
        TIndividual ind;

        // Generate some random path: Place city indexes to the vector in some random order.
        // At index 0 will be city we start from.
        ind.path.clear();
        ind.path.push_back(0);
        j=1;
        while (j < matrix->getNumberOfTargets()) {
            x = random() % matrix->getNumberOfTargets();
            p = find( ind.path.begin(), ind.path.end(), x);
            if (p == ind.path.end()) {
                ind.path.push_back(x);
                j++;
            }
        }

        // Store this path into table of individuals.
        // Fitness and other parameters will be computaed later.
        individuals.push_back( ind);
    }
    // compute fitnesses and sort individuals
    recalculate( matrix);
    printState(0);
    // remember the best solution
    best = individuals.at(0).path;
    bestFitness = individuals.at(0).fitness;
    // run simulation
    for (i=1; i<GENERATIONS; i++) {
        // selection: select individuals for a new generation
        //printf("Generation %d of %d\n", i, GENERATIONS);

        //printf("Before selection\n");
        selection();
        //printf("After selection\n");

        // crossover
        crossover( matrix, crossoverMethod);

        // mutation
        if (mutation_probability > 0) mutation( mutation_probability);

        // print the best result
        recalculate( matrix);
        printState(i);

        // if fitness < lastFitness, increase mutation probability by one step
        if (individuals.at(0).fitness < lastFitness)
            mutation_probability += PROBABILITY_MUT_STEP;
        else
            mutation_probability = 0;

        lastFitness = individuals.at(0).fitness;

        if (lastFitness > bestFitness) {
            best = individuals.at(0).path;
            bestFitness = individuals.at(0).fitness;
        }
    }

    return best;
}
