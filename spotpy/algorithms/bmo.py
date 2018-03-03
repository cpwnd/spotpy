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



import collections
import math

from _algorithm import _algorithm

def get_fitness(bird):
    print("Bird = ", bird)
    return bird.fitness()

def split_gender(soc):
    males = []
    females = []

    for b in soc:
        if b.isFemale:
            females.append(b)
        else:
            males.append(b)

    return males, females

def specify_breeding(soc):
    #TODO: implement this
    return soc, soc, soc

def selection(soc):
    """ Removes the worst birds and create new birds with chaotic sequence"""
    #TODO:
    return soc

def breed_monogamous(soc):
    return soc

def breed_polygynous(soc):
    return soc

def breed_polyandrous(soc):
    return soc

def breed_promicious(soc):
    return soc

def breed_pathenogenetic(soc):
    return soc

def replacement(soc, mono, polya, polyg, promicious, parthenogenetic):
    return soc

class Bird():
    """Specifies a bird by its features"""
    def __init__(self, isFemale=True, sex='p', params=0):

        self.isFemale = isFemale
        self.sex = sex

        # Paremter set
        self.genes = params

        self._fitness = math.inf

    # Objectivefunction
    def fitness(self):
        """Computes birds logistical fitness as double, where 0 is good and infinity is bad"""
        return 0.0

    def __repr__(self):
        return '<Bird g=%s s=%s>' % (('f' if self.isFemale else 'm', self.sex))

class bmo(_algorithm):
    """Algorithm implementation based on Bird Mating Optimization, Askarzadeh (2014)"""
    def __init__(self, spot_setup, dbname=None, dbformat=None, parallel='seq', save_sim=True):
        """

        """
        # init parameters
        #  as provided in the paper
        self.society_size = 10
        monogamous = 0.5
        polygynous = 0.3
        promiscuous = 0.1
        polyandrous = 0.05
        parthenogenetics = 0.05
        maximum_generation = 10e4

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

    def update_parameter(self):
        return 0

    def sample(self, n):
        """
        n :param: defines max epochs of society breeding/evolution
        """

        def compute_fitness(soc):
            """
            Computes fitness of a given (sub)set of a bird society
            """
            print(soc)
            for i in range(len(soc)):
                print(i)
                print("Bird =", soc[i])
                soc[i]._fitness = soc[i].fitness()
                print(soc[i]._fitness)
            return soc

        print(self.society[0])

        print(dir(self.spot_setup))

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

            # compute objective function
            society = compute_fitness(self.society)

            # sort birds based on their objective function
            society = sorted(society, key=get_fitness)

            # partition society into males and females
            males, females = split_gender(society)

            # Specify monogamous, polygynous, and polyandrous birds
            mono, polyg, polya = specify_breeding(society)

            # Remove the worst birds and generate promiscuous birds based on the chaotic sequence
            promicious_birds = selection(society)

            # Compute objective function of the promiscuous birds
            promicious_birds = compute_fitness(promicious_birds)

            # BREED MONOGAMOUS BIRDS
            mono = breed_monogamous(mono)

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

if __name__ == '__main__':

    print(bmo)

    #Create samplers for every algorithm:
    results=[]
    spot_setup=spot_setup()
    rep=5000

    sampler=bmo(spot_setup, dbname='RosenMC', dbformat='csv')
    sampler.sample(rep)
    results.append(sampler.getdata())
