# coding=utf-8
import traceback
from decimal import getcontext

from Vector import Vector

getcontext().prec = 30


class matrix(object):
    ALL_Vector_MUST_BE_IN_SAME_DIM_MSG = 'All vector in the system should live in the same dimension'
    NO_SOLUTIONS_MSG = 'No solutions'
    INF_SOLUTIONS_MSG = 'Infinitely many solutions'

    def __init__(self, Vector):
        try:
            d = Vector[0].dimension
            for v in Vector:
                assert v.dimension == d

            self.Vector = Vector
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

    def matxRound(self, decPts=4):
        for i, v in enumerate(self.Vector):
            list = []
            for n, m in enumerate(v):
                list.append(round(m, decPts))
            self[i] = Vector(list)
