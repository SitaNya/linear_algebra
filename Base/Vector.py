# coding=utf-8
import traceback
# 没有程序员会介意错误更详细一些
from math import sqrt, pi, acos
from decimal import Decimal, getcontext

getcontext().prec = 30


class Vector(object):
    CANNOT_NORMALIZE_ZERO_VECTOR_MSG = 'Cannot normalize the zero vector'
    ALL_Vector_MUST_BE_IN_SAME_DIM_MSG = 'All vector in the system should live in the same dimension'
    NO_UNIQUE_PARALLEL_COMPONENT_MSG = 'Zero vector NO UNIQUE PARALLEL COMPONENT'
    ONLY_DEFINED_IN_TOW_THREE_DIMS_MSG = 'ONLY_DEFINED_IN_TOW_THREE_DIMS_MSG'

    def __init__(self, coordinates):
        """
        将向量转换为Decimal（精度更高）类型后存储，并初始化其长度，并初始化其索引，用于后续的取值
        :param coordinates: 输入坐标系，否则将报错
        """
        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple(x for x in coordinates)
            self.dimension = len(coordinates)
            self.idx = 0

        except ValueError:
            raise ValueError('The coordinates must be nonempty')

        except TypeError:
            raise TypeError('The coordinates must be an iterable')

    def plus(self, v):
        """
        向量相加，每个向量之间相加
        :rtype: Vector
        """
        new_coordinates = [x + y for x, y in zip(self.coordinates, v.coordinates)]
        return Vector(new_coordinates)

    def minus(self, v):
        """
        向量相减，每个向量之间相减
        :param v:减数 
        :return: 返回被减后的向量
        """
        new_coordinates = [x - y for x, y in zip(self.coordinates, v.coordinates)]
        return Vector(new_coordinates)

    def times_scaler(self, c):
        """
        向量的点乘方法，每个值乘以一个常数，直接代表了将向量延长c倍
        :param c: 延长c倍
        :return: 返回被延长后的向量
        """
        new_coordinates = [Decimal(c) * x for x in self.coordinates]
        return Vector(new_coordinates)

    def magnitude(self):
        """
        标准化一个向量，需要把每个值的平方相加后再开方，代表
        :return: 
        """
        coordinates_squared = [x ** 2 for x in self.coordinates]
        return sqrt(sum(coordinates_squared))

    def normalized(self):
        try:
            magnitude = Decimal(self.magnitude())
            return self.times_scaler(Decimal('1.0') / magnitude)
        except ZeroDivisionError:
            raise self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG

    def dot(self, v):
        return sum([x * y for x, y in zip(self.coordinates, v.coordinates)])

    def angle_with(self, v, in_degrees=False):
        try:
            u1 = self.normalized()
            u2 = v.normalized()
            angle_in_radians = acos(Decimal(u1.dot(u2)).quantize(Decimal('0.000')))

            if in_degrees:
                degrees_per_radian = 180. / pi
                return angle_in_radians * degrees_per_radian
            else:
                return angle_in_radians
        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception("Cannot compute an angle with the zero vector")
            else:
                raise e

    def is_orthogonal_to(self, v, tolerance=1e-10):
        return abs(self.dot(v)) < tolerance

    def is_parallel_to(self, v):
        return (self.is_zero() or
                v.is_zero() or
                self.angle_with(v) == 0 or
                self.angle_with(v) == pi)

    def is_zero(self, tolerance=1e-10):
        return self.magnitude() < tolerance

    def component_parallel_to(self, basis):
        try:
            u = basis.normalized()
            weight = self.dot(u)
            return u.times_scaler(weight)
        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception(self.NO_UNIQUE_PARALLEL_COMPONENT_MSG)
            else:
                raise 'traceback.format_exc():\n%s' % traceback.format_exc()

    def component_orthogonal_to(self, basis):
        try:
            projection = self.component_orthogonal_to(basis)
            return self.minus(projection)
        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception(self.NO_UNIQUE_PARALLEL_COMPONENT_MSG)
            else:
                raise 'traceback.format_exc():\n%s' % traceback.format_exc()

    def cross(self, v):
        try:
            x_1, y_1, z_1 = self.coordinates
            x_2, y_2, z_2 = v.coordinates
            new_coordinates = Vector([y_1 * z_2 - y_2 * z_1,
                                      -(x_1 * z_2 - x_2 * z_1),
                                      x_1 * y_2 - x_2 * y_1])
            return new_coordinates
        except Exception as e:
            msg = str(e)
            if msg == 'need more than 2 values to unpack':
                self_embedded_in__r3 = Vector(self.coordinates + ('0',))
                v_embedded_in__r3 = Vector(v.coordinates + ('0',))
                return self_embedded_in__r3.cross(v_embedded_in__r3)
            elif (msg == 'too many values to unpack' or
                          msg == 'need more than 1 value to unpack'):
                raise Exception(self.ONLY_DEFINED_IN_TOW_THREE_DIMS_MSG)
            else:
                raise 'traceback.format_exc():\n%s' % traceback.format_exc()

    def area_of_parallelogram_with(self, v):
        cross_product = self.cross(v)
        return round(cross_product.magnitude(), 3)

    def area_of_triangle_with(self, v):
        cross = self.cross(v)
        return round(Decimal(cross.magnitude()) / Decimal('2.0'), 3)

    def __str__(self):
        return 'Vector: {}'.format(self.coordinates)

    def __eq__(self, v):
        return self.coordinates == v.coordinates

    def __getitem__(self, index):
        return self.coordinates[index]

    # 这里感谢mentor帮助，我先前发现重复运行代码存在不同的回显百思不得其解，询问后才了解到这里的基础代码应补充一行idx=0
    def __iter__(self):
        self.idx = 0
        return self

    def next(self):
        self.idx += 1
        try:
            return Decimal(self.coordinates[self.idx - 1])
        except IndexError:
            self.idx = 0
            raise StopIteration  # Done iterating.

# v1 = Vector([8.462, 7.893, -8.187])
# w1 = Vector([6.984, -5.975, 4.778])
#
# v2 = Vector([-8.987, -9.838, 5.031])
# w2 = Vector([-4.268, -1.861, -8.866])
#
# v3 = Vector([1.5, 9.547, 3.691])
# w3 = Vector([-6.007, 0.124, 5.772])
#
# print v1.cross(w1)
#
# print v2.area_of_parallelogram_with(w2)
#
# print v3.area_of_triangle_with(w3)
