# -*- coding: utf-8 -*-
"""

:author: Chris Weber

This class holds the Bird Mating Optimization (BMO) algorithm, based on Askarzadeh (2014):

Alireza Askarzadeh, Department of Energy Management and Optimization, Institute of Science and High Technology and Environmental Sciences, Graduate University of Advanced Technology, Kerman, Iran

:see: https://doi.org/10.1016/j.cnsns.2013.08.027

"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import spotpy
from spotpy.examples.spot_setup_rosenbrock import spot_setup

from pprint import pprint

import collections
import math
from random import randint

from _algorithm import _algorithm

class BREEDING():

    # Parthenogenesis, Females is able to raise children alone
    PATHENOGENETIC = 'PATHENOGENETIC'
    # Polyandry, female bird mates with two or more males
    POLYANDROUS = 'POLYANDROUS'

    # Monogamy, one male mates with one female
    MONOGAMOUS = 'MONOGAMOUS'
    # Polygyny, one male mates with two or more females
    POLYGYNOUS = 'POLYGYNOUS'
    # Promiscuity, mating betwenn two birds is one-time-event
    PROMISCUOUS = 'PROMISCUOUS'

FEMALE_BREEDING = [BREEDING.PATHENOGENETIC, BREEDING.POLYANDROUS]
MALE_BREEDING = [BREEDING.MONOGAMOUS, BREEDING.POLYGYNOUS, BREEDING.PROMISCUOUS]

#
# Util
#
def get_fitness(bird):
    #print("Bird = ", bird)
    return bird._fitness

def split_gender(soc):
    males = []
    females = []

    for b in soc:
        if b.isFemale:
            females.append(b)
        else:
            males.append(b)

    return males, females

class Chaotic_Bird_Generator():

    # last chaotic value
    last = 0

    @classmethod
    def next(cls, f):
        def create_parameter_from(chaotic_value):
            # TODO make cls.last chaotic_value
            return f()
        cls.last = create_parameter_from(cls.last)
        return cls.last




#
def specify_breeding(self, soc):
    """Returns specified society
    Step 4 of algorithm"""

    # saves references of birds
    females = []
    males = []

    # Split society into male/female
    # - females are the most promising ones
    # - males are the others
    for i in range(round(len(soc))):
        # soc is already ordered
        if i < round(len(soc) / 2):
            soc[i].isFemale = True
            females.append(soc[i])
        else:
            soc[i].isFemale = False
            males.append(soc[i])

    # Split females equally parthenogenetic (better ones) and polyandrous
    for i in range(len(females)):
        if i < round(len(females) / 2):
            females[i].sex = BREEDING.PATHENOGENETIC
        else:
            females[i].sex = BREEDING.POLYANDROUS

    # Males split into: Monogamous (better ones) and polygynous
    for i in range(len(males)):
        if i < round(len(males) / 3):
            males[i].sex = BREEDING.MONOGAMOUS
        elif i < round((len(males) / 3) * 2):
            males[i].sex = BREEDING.POLYGYNOUS
        else:
            # STEP 5 third group is removed from society
            #        and generated using a chaotic sequence
            # TODO: chaotic sequence
            males[i].genom = Chaotic_Bird_Generator.next(self.parameter)
            males[i].sex = BREEDING.PROMISCUOUS

    return soc

def breed_monogamous(soc):
    """Breed monogamous birds"""

    # problem dimension
    n = len(soc[0].genom)

    def breeding(f, m, brood):
        """Returns bird"""

        def randomize(bird):
            """Returns Bird"""
            return bird

        def weight(bird):
            # weight over time
            weight = 0.1

            return bird


        #brood = m.genom + weight(randomize(f.genom - m.genom))
        brood = m + weight(randomize(f - m))
        c = randint(1, n)
        if r_1 > mcf:
            brood[c] = lower_bound(c) - r_2 * (lower_bound(c) - upper_bound(c))
            return broot[c]
    brood = []
    females = []
    males = []

    # match elite females with monogamous males
    for i in range(len(soc)):
        if soc[i].sex == BREEDING.MONOGAMOUS:
            males.append(i)
            for j in range(len(soc)):
                if soc[j].sex == BREEDING.PATHENOGENETIC:
                    if j in females:
                        continue
                    females.append(j)
                    break

    # has to be the same
    assert len(females) == len(males)

    for i in range(len(females)):
        bird = breeding(soc[females[i]], soc[males[i]], brood)
        brood.append(bird)

    pprint(females)
    pprint(males)

    return brood

def breed_polygynous(soc):
    return soc

def breed_polyandrous(soc):
    return soc

def breed_promicious(soc):
    return soc

def breed_pathenogenetic(soc):
    return soc

def replacement(soc, mono, polya, polyg, promicious, parthenogenetic):
    """Replacement of individuals of society with different new breds"""

    # determine fittest individuals

    # place into soc
    return soc

class Bird():
    """Specifies a bird by its features"""
    def __init__(self, isFemale=True, sex='p', params=0):

        self.isFemale = isFemale
        self.sex = sex

        # Paremter set
        self.genom = params

        self._fitness = math.inf

    # Objectivefunction
    def fitness(self, setup):
        """Computes birds logistical fitness as double, where 0 is good and infinity is bad"""
        return setup.objectivefunction(setup.simulation([e[0] for e in self.genom]), setup.evaluation())

    def genomrepr(self):
        """Returns genom representation out of parameters"""
        return "".join([str.ljust(str(e[0]) if str(e[0]).startswith('-') else '+'+str(e[0]), GENOM_LEN_MAX,'0') for e in self.genom])

    def __repr__(self):
        return '<Bird g=%s s=%s [%s]>' % (('f' if self.isFemale else 'm', self.sex, self._fitness))

    def __add__(self, other):
        self._fitness += other._fitness
        return self

    def __sub__(self, other):
        self._fitness -= other._fitness
        return self

def sort_soc(soc):
    return sorted(society, key=get_fitness, reverse=True)

GENOM_LEN_MAX = 18
class bmo(_algorithm):
    """Algorithm implementation based on Bird Mating Optimization, Askarzadeh (2014)"""

    def __init__(self, spot_setup, dbname=None, dbformat=None, parallel='seq', save_sim=True):
        """

        """
        # init parameters
        #  as provided in the paper
        self.society_size = 12
        #_algorithm.__init__(self, spot_setup, dbname=dbname,
        #                    dbformat=dbformat, parallel=parallel, save_sim=save_sim)


        # init parameters
        self.monogamous = 0.5
        self.polygynous = 0.3
        self.promiscuous = 0.1
        self.polyandrous = 0.05
        self.parthenogenetics = 0.05
        self.maximum_generation = 10e4

        # Mutation control factor
        self.mcf = 0.1

        self.spot_setup = spot_setup

        # init society
        #self.society = collections.defaultdict(str)
        self.society = []
        for i in range(0, self.society_size):

            self.society.append(\
                Bird(\
                  isFemale=(False if (i % 2 == 0) else True)))


        _algorithm.__init__(self, spot_setup, dbname=dbname,
                            dbformat=dbformat, parallel=parallel, save_sim=save_sim)

    def selection(self, soc):
        """ Removes the worst birds and create new birds with chaotic sequence"""
        #TODO is there an queue like collection
        worst = [soc[0]]
        best_of_worst = soc[0]._fitness

        # iterate all individuals
        #  and add to worst collection if best of worst is > i
        for i in range(len(soc)):
            if soc[i]._fitness < best_of_worst:
                # append to worst
                worst.append(soc[i])
                # TODO selection size
                if len(worst) > 10:
                    # sort highfit < lowfit
                    worst = sort_soc(worst)
                    # remove highestfit and set new highest fit
                    worst.remove(0)
                    best_of_worst = worst[0]._fitness
        # TODO: creation
        # create new birds with chaotic sequence
        for i in range(len(soc)):
            self.society[i].genom = self.parameter()

        return soc

    def update_parameter(self):
        return 0

    def getdata(self):
        return []

    def sample(self, n=10e4, monogamous = .5, polygynous = .3, promiscuous = .1, polyandrous = .05,
    pathenogenetic = .05):
        """
        n :param: defines max epochs of society breeding/evolution
        """

        def compute_fitness(soc):
            """
            Computes fitness of a given (sub)set of a bird society
            """

            for i in range(len(soc)):
                #print(self.setup.objectivefunction(self.setup.simulation([e[0] for e in soc[i].genom]), self.setup.evaluation()))
                soc[i]._fitness = soc[i].fitness(self.setup)
            return soc

        print("Starting BMO algorithm using\n####################"+
        "\n\n\tsociety-size\t\t{}\n\tmax epochs\t\t{}".format(self.society_size, n))


        # init population

        self.set_repetiton(n)

        #print(self.parameter())

        self.min_bound, self.max_bound = self.parameter(
        )['minbound'], self.parameter()['maxbound']

        #print(self.min_bound, self.max_bound)
        #repetitions = int(n / nChains)

        #ndraw_max = repetitions * nChains
        #maxChainDraws = int(ndraw_max / nChains)

        params = self.get_parameters()

        for i in range(0, self.society_size):
            for p in params:
                self.society[i].genom = self.parameter()

                try:
                    assert(len(self.society[i].genomrepr()) == ( GENOM_LEN_MAX * len(params)))
                except AssertionError:
                    print(self.society[i].genomrepr())
                    print(len(self.society[i].genomrepr()),( GENOM_LEN_MAX * len(params)))
                    break


        #for i in self.spot_setup.params:
        #    print(i.name)
    #        print(i.optguess)
        #    print(i.minbound)
        #    print(i.maxbound)
        #    print(i.step)

        #print(self.spot_setup.parameters)

        #print(dir(self.spot_setup))

        # compute n epochs
        for i in range(0, n):
            print("Epoch\t{} ...".format(i))

            # compute objective function
            society = compute_fitness(self.society)


            # sort birds based on their objective function
            society = sorted(society, key=get_fitness, reverse=True)

            # partition society from gender into males and females
            # Specify monogamous, polygynous, and polyandrous birds
            society = specify_breeding(self, society)

            society = compute_fitness(society)

            # Remove the worst birds and generate promiscuous birds based on the chaotic sequence
            # promicious_birds = self.selection(society)
            # Compute objective function of the promiscuous birds
            # promicious_birds = compute_fitness(promicious_birds)

            # BREED MONOGAMOUS BIRDS
            mono_brood = breed_monogamous(society)

            print("#######################")
            pprint(society)
            pprint(mono_brood)
            exit()


            # BREED POLYGYNOUS BIRDS
            polyg = breed_polygynous(polyg)

            # BREED POLYANDROUS BIRDS
            polya = breed_polyandrous(polya)

            # BREED PROMICIOUS BIRDS
            promicious_birds = breed_promicious(promicious_birds)

            # BREED PARTHENOGENETIC BIRDS
            parthenogenetic_birds = breed_pathenogenetic(society)

            # Compute objective function of the broods
            for s in [mono, polyg, polya, promicious_birds]:
                s = compute_fitness(s)

            # Perform replacement stage
            self.society = replacement(society, mono, polya, polyg, promicious_birds, parthenogenetic_birds)

            # Update parameters
            self.update_parameter()

 #           print('hello')
#            pprint(self.society)

if __name__ == '__main__':

    #Create samplers for every algorithm:
    results=[]
    spot_setup=spot_setup()
    rep=40

    sampler=bmo(spot_setup, dbname='RosenMC', dbformat='csv')
    sampler.sample(rep)
    results.append(sampler.getdata())
