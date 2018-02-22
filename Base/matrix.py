# coding=utf-8
from copy import deepcopy
from decimal import getcontext

from Vector import Vector

getcontext().prec = 30


class matrix(object):
    ALL_Vector_MUST_BE_IN_SAME_DIM_MSG = 'All vector in the system should live in the same dimension'
    NO_SOLUTIONS_MSG = 'No solutions'
    INF_SOLUTIONS_MSG = 'Infinitely many solutions'

    def __init__(self, vector):
        try:
            d = vector[0].dimension
            for v in vector:
                assert v.dimension == d

            self.Vector = vector
            self.dimension = d

        except AssertionError:
            raise Exception(self.ALL_Vector_MUST_BE_IN_SAME_DIM_MSG)

    def __len__(self):
        return len(self.Vector)

    def __getitem__(self, i):
        return self.Vector[i]

    def __setitem__(self, i, x):
        try:
            assert x.dimension == self.dimension
            self.Vector[i] = x

        except AssertionError:
            raise Exception(self.ALL_Vector_MUST_BE_IN_SAME_DIM_MSG)

    def __str__(self):
        ret = 'Matrix:\n'
        temp = ['Equation {}: {}'.format(i + 1, p) for i, p in enumerate(self.Vector)]
        ret += '\n'.join(temp)
        return ret

    def shape(self):
        m_len = self.__len__()
        m_dimensiou = self.dimension
        temp = ['Len is: {},col_num is: {}'.format(m_len, m_dimensiou)]
        return "\nMatrix size is:\n" + str(temp)

    def matxround(self, dec_pts=4):
        for Vector_index, vector in enumerate(self.Vector):
            temp_vector = []
            for number_index, number in enumerate(vector):
                temp_vector.append(round(number, dec_pts))
            self[Vector_index] = Vector(temp_vector)

    def transpose(self):
        system = deepcopy(self)
        vector_index = 0
        for number_index in range(0, self.dimension):
            temp_vector = []
            for Vector_number, vector in enumerate(self.Vector):
                temp_vector.append(vector[number_index])
            system[vector_index] = Vector(temp_vector)
            vector_index += 1
        return system

    def matxmultiply(self, b):
        system = deepcopy(self)
        for Vector_index, vector in enumerate(self.Vector):
            temp_vector = []
            for number_index, number in enumerate(vector):
                temp_vector.append(number * b)
            system[Vector_index] = Vector(temp_vector)
        return system
