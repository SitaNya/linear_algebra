# coding=utf-8
from Base.Vector import Vector
from Base.linsys import LinearSystem
from Base.plane import Plane

from helper import *

seed = 0

# A = generateMatrix(3,seed,singular=True)
# b = np.ones(shape=(3,1),dtype=int)
# Ab = li.augmentMatrix(A.tolist(),b.tolist()) # 请确保你的增广矩阵已经写好了
# printInMatrixFormat(Ab,padding=3,truncating=0)

p1 = Plane(normal_vector=Vector(['5.862', '1.178', '-10.366']), constant_term='-8.15')
p2 = Plane(normal_vector=Vector(['-2.931', '-0.589', '5.183']), constant_term='-4.075')
s = LinearSystem([p1, p2])

p1 = Plane(normal_vector=Vector(['8.631', '5.112', '-1.816']), constant_term='-5.113')
p2 = Plane(normal_vector=Vector(['4.315', '11.132', '-5.27']), constant_term='-6.775')
p3 = Plane(normal_vector=Vector(['-2.158', '3.01', '-1.727']), constant_term='-0.831')
s2 = LinearSystem([p1, p2, p3])

p1 = Plane(normal_vector=Vector(['5.262', '2.739', '-9.878']), constant_term='-3.441')
p2 = Plane(normal_vector=Vector(['5.111', '6.358', '7.638']), constant_term='-2.152')
p3 = Plane(normal_vector=Vector(['2.016', '-9.924', '-1.367']), constant_term='-9.278')
p4 = Plane(normal_vector=Vector(['2.167', '-13.543', '-18.883']), constant_term='-10.567')
s3 = LinearSystem([p1, p2, p3, p4])
print s3.compute_solution()