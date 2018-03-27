#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
allFm = open("./都市奇门医生-ALL.txt",'w');
allFm.close();
path = os.listdir(os.getcwd());
path.sort();
# print(path);
for p in path:
  arr = os.path.splitext(p);
  if p.find("-ALL")==-1 and p.find(".DS_Store")==-1 and p.find(".py") == -1:
    itemFm = open(p,"r");
    itemTxt = itemFm.read();
    itemFm.close();
    allFm = open("./都市奇门医生-ALL.txt",'a');
    allFm.write(itemTxt);
    allFm.close();
    pass
  pass