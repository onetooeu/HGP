#!/usr/bin/env python3
import math
kB=1.380649e-23; ln2=math.log(2)
for T in [4.2,77,300]:
  E=kB*T*ln2
  print('T',T,'E_bit',E)
