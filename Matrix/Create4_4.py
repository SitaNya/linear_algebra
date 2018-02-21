# coding=utf-8
import sys

sys.path.append('../')
from Base.Vector import Vector
from Base.matrix import matrix

v1 = Vector([0.9353123, 1.76123123, -9.3655345, -9.16285467])
v2 = Vector([5.73456236, 6.7345635, 7.623452525, 8.6234551565])
v3 = Vector([9.1356461654, 10.161348971, 11.19713641894, 12.198874131])
v4 = Vector([13.1961231341, 14.164789131, 15.189671684, 16.18731687])
m = matrix([v1, v2, v3, v4])
print m

# 返回4*4单位矩阵


print m.shape()
# 返回行列

m.matxRound()
print "\n四舍五入后： " + str(m)
