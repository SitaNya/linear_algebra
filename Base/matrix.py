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
        matrix_list = []
        for i in vector:
            matrix_list.append(Vector(i))
        try:
            d = matrix_list[0].dimension
            for v in matrix_list:
                assert v.dimension == d

            self.Vector = matrix_list
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

    @staticmethod
    def shape(M):
        if type(M) == list:
            M = matrix(M)
        m_len = M.__len__()
        m_dimensiou = M.dimension
        # temp = ['Len is: {},col_num is: {}'.format(m_len, m_dimensiou)]
        # return "\nMatrix size is:\n" + str(temp)
        return m_len, m_dimensiou

    @staticmethod
    def matxRound(M, dec_pts=4):
        for Vector_index, vector in enumerate(M):
            for number_index, number in enumerate(vector):
                M[Vector_index][number_index] = (round(number, dec_pts))

    @staticmethod
    def transpose(M):
        ma = matrix(M)
        result_matrix_list = []
        vector_index = 0
        for number_index in range(0, ma.dimension):
            temp_vector = []
            for Vector_number, vector in enumerate(ma.Vector):
                temp_vector.append(vector[number_index])
            result_matrix_list.append(temp_vector)
            vector_index += 1
        return result_matrix_list

    @staticmethod
    def matxMultiply(A, B):
        try:
            if B.__len__() != A[0].__len__():
                raise ValueError(1)
            ma1 = matrix(A)
            ma2 = matrix(matrix.transpose(B))
            result_matrix_list=[]
            for ma1_index, ma1_vector in enumerate(ma1.Vector):
                temp_vector = []
                for ma2_index, ma2_vector in enumerate(ma2.Vector):
                    temp_vector.append(ma1_vector.dot(ma2_vector))
                result_matrix_list.append(temp_vector)
            return result_matrix_list
        except ValueError as e:
            raise e
