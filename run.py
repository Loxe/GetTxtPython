#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os

path = os.listdir(os.getcwd());
for p in path:
  arr = os.path.splitext(p);
  if arr[-1] == ".py" and p.find("run")==-1:
    cwd = os.path.join(os.getcwd(),p);
    os.system('{} {}'.format('python3', cwd));
    pass
  pass

