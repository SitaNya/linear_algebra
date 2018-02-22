# coding=utf-8
import traceback
from decimal import Decimal, getcontext

from Vector import Vector

getcontext().prec = 30


class Plane(object):
    NO_NONZERO_ELTS_FOUND_MSG = 'No nonzero elements found'
    NO_NONZERO_TO_EQ = '\'NoneType\' object has no attribute \'minus\''
    basepoint_difference = None
    vector_normal = None

    def __init__(self, normal_vector=None, constant_term=None):
        self.basepoint = None
        self.dimension = 3

        if not normal_vector:
            all_zeros = ['0'] * self.dimension
            normal_vector = Vector(all_zeros)
        self.normal_vector = normal_vector

        if not constant_term:
            constant_term = Decimal('0')
        if type(constant_term)!=list:
            self.constant_term = Decimal(constant_term)
        else:
            self.constant_term = Decimal(constant_term[0])

        self.set_basepoint()

    def set_basepoint(self):
        try:
            vector_normal = self.normal_vector
            vector_constant = self.constant_term
            basepoint_coords = ['0'] * self.dimension

            initial_index = Plane.first_nonzero_index(vector_normal)
            initial_coefficient = vector_normal[initial_index]

            basepoint_coords[initial_index] = vector_constant / initial_coefficient
            self.basepoint = Vector(basepoint_coords)

        except Exception as e:
            if str(e) == Plane.NO_NONZERO_ELTS_FOUND_MSG:
                pass
            else:
                raise 'traceback.format_exc():\n%s' % traceback.format_exc()

    def __str__(self):
        output=[]
        for i in self.normal_vector:
            output.append(i)
        output.append(self.constant_term)
        return output



    @staticmethod
    def first_nonzero_index(iterable):
        for k, item in enumerate(iterable):
            if not MyDecimal(item).is_near_zero():
                return k
        raise Exception(Plane.NO_NONZERO_ELTS_FOUND_MSG)

    def is_parallel_to(self, ell):
        n1 = self.normal_vector
        n2 = ell.normal_vector

        return n1.is_parallel_to(n2)

    def intersection_with(self, ell):
        try:
            a, b = self.normal_vector.coordinates
            c, d = ell.normal_vector.coordinates
            k1 = self.constant_term
            k2 = ell.constant_term
            x_numerator = d * k1 - b * k2
            y_numerator = -c * k1 + a * k2
            one_over_denom = Decimal('1') / (a * d - b * c)

            return Vector([x_numerator, y_numerator]).times_scaler(one_over_denom)

        except ZeroDivisionError:
            if self == ell:
                return self
            else:
                return None

    def __eq__(self, ell):
        global basepoint_difference
        if not self.is_parallel_to(ell):
            return False
        x0 = self.basepoint
        y0 = ell.basepoint

        # 这里做了一点小改变。考虑到x0和y0可能为0向量，不能让程序就此终止也不能不报，因此这里判断为0后程序继续，打印一行错误。
        # 我有些担心如果x0不为0，y0为0后会如何。不过还有一种可能的解决方案是给setbasepoint方法中self.basepoint = None改为
        # self.basepoint = Vector(basepoint_coords)，这里的basepoint_coords已经被初始化[0,0,0……]而未被赋予别的值
        try:
            basepoint_difference = x0.minus(y0)
            return basepoint_difference.is_orthogonal_to(self.normal_vector)
        except Exception as e:
            if str(e) == Plane.NO_NONZERO_TO_EQ:
                print '被除数为0'
                return basepoint_difference.is_orthogonal_to(self.normal_vector)


class MyDecimal(Decimal):
    # noinspection PyTypeChecker
    def is_near_zero(self, eps=1e-10):
        return abs(self) < eps