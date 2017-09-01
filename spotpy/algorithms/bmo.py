# -*- coding: utf-8 -*-
"""

:author: Chris Weber

This class holds the Bird Mating Optimization (BMO) algorithm, based on Askarzadeh (2014):

Alireza Askarzadeh, Department of Energy Management and Optimization, Institute of Science and High Technology and Environmental Sciences, Graduate University of Advanced Technology, Kerman, Iran

:see: https://doi.org/10.1016/j.cnsns.2013.08.027

"""

from collections import defaultdict

class Bird():
    """Specifies a bird by its features"""
    def __init__(self, isFemale=True):

        self.isFemale = isFemale

    def fitness(self):
        return

class bmo(_algorithm):
"""Algorithm implementation based on Bird Mating Optimization, Askarzadeh (2014)"""
    def __init__(self, spot_setup, dbname=None, dbformat=None, parallel='seq', save_sim=True):
        """

        """
        _algorithm.__init__(self, spot_setup, dbname=dbname,
                            dbformat=dbformat, parallel=parallel, save_sim=save_sim)

    def sample():
        """

        """
        # init parameters
        society_size = 1000
        monogamous = 0.5
        polygynous = 0.3
        promiscuous = 0.1
        polyandrous = 0.05
        parthenogenetics = 0.05
        maximum_generation = 10e4

        # compute objective function
        society = defaultdict(str)

        # sort birds based on their objective function
        collection.sort(society)
