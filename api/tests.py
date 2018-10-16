from django.test import TestCase

# Create your tests here.
# import itertools
#
# c = list(itertools.chain([{"A":1}],[{"A":2}]))
# print(list(c))


l1 = [1,2,3,4,5,6]
try:
    l1[10]
except:
    l1.append(7)
print(l1)