#!/usr/bin/env python

"""
    Author: Eyal Godovich
    Date created: 11/09/2018
    Python Version: 3.6
"""


class Twister(object):
    """
    Implements a Mersenne-Twister (MT19937), including a backtrack algorithm to revert to a seed given a list
    of 624 generated numbers
    """

    xor_mask = 0x9908b0df
    initialization_multiplier = 0x6c078965
    tempering_b = 0x9d2c5680
    tempering_d = 0x7fffffff
    tempering_c = 0xefc60000
    shift_size = 397
    state_size = 624

    def __init__(self, seed=0):
        """
        Initialize state to a
        :type seed: int
        """

        assert isinstance(seed, int), 'Seed must be a 32-bit integer'

        self.index = self.state_size
        self.state = [0] * self.index
        self.state[0] = seed

        for i in range(1, self.state_size):
            self.state[i] = 0xffffffff & (
                    self.initialization_multiplier * (self.state[i - 1] ^ self.state[i - 1] >> 30) + i)

    def random(self):
        """
        Returns a floating point between 0.0 and 1.0
        :rtype: int
        """

        return float(((self.random32() >> 5) * 0x4000000 + (self.random32() >> 6)) * (1 / 0x20000000000000))

    def getrandbits(self, n):
        """
        Alias to random 32, only accepts 32 bits
        :rtype: int
        """

        assert n == 32, 'The function only accepts 32 bits at this point'
        return self.random32()

    def twist(self):
        """
        Twists the state to create the next set of random numbers
        """

        for k in range(self.state_size):
            y = (self.state[k] & 0x80000000) | (self.state[(k + 1) % self.state_size] & self.tempering_d)
            self.state[k] = self.state[(k + self.shift_size) % self.state_size] ^ (y >> 1)

            if y % 2:
                self.state[k] ^= self.xor_mask

        self.index = 0

    def random32(self):
        """
        Returns the next 32 bit random number
        :rtype: int
        """

        # Twist state if we're past the initial phase
        if self.index >= self.state_size:
            self.twist()

        # Increment the index by one to mark we used that number
        self.index += 1

        # Get the next random number
        return self.__transform(self.state[self.index - 1])

    def backtrack(self, numbers):
        """
        Sets the current state of the PRNG based on a list of the first 624 numbers generated from another MT19937
        pseudo-random number generator
        """

        assert len(numbers) == 624, 'A list of 624 32-bit integers is required'
        self.state = [self.__revert_transformation(x) for x in numbers]


    def __transform(self, num):
        """
        Applies the MT19937 transformation on a given integer
        :param num: int
        :return: int
        """

        num ^= (num >> 11)
        num ^= (num << 7) & self.tempering_b
        num ^= (num << 15) & self.tempering_c
        return num ^ (num >> 18)

    def __revert_transformation(self, num):
        """
        The revert function of __transform, should revert the effects of the MT19937 transformation.
        For every x, __revert_transformation(__transform(x)) == x should hold
        :param num: int
        :return: int
        """
        num ^= (num >> 0x12) ^ (num >> 0x24)
        num ^= ((num & 0x7fff) << 15) & self.tempering_c
        num ^= ((num & 0x3fff8000) << 15) & self.tempering_c
        num ^= (((num & 0x1fffc0000000) << 15) & self.tempering_c)
        num ^= ((num & 0x7f) << 7) & self.tempering_b
        num ^= ((num & 0x3f80) << 7) & self.tempering_b
        num ^= ((num & 0x1fc000) << 7) & self.tempering_b
        num ^= ((num & 0xfe00000) << 7) & self.tempering_b
        num ^= (((num & 0x7f0000000) << 7) & self.tempering_b)
        num ^= (num >> 0x0b) ^ (num >> 0x16)
        return num