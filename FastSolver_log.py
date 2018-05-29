#!/usr/bin/env python

from __future__ import division
import argparse
import random
import queue
import math
import numpy as np



def solve(P, M, N, C, items, constraints):
  """


  Return: a list of strings, corresponding to item names.
  """
  maxer={}
  exp = 0.65
  

  itemProfit = 0
  itemWeight = 0
  itemCost = 0
  itemlist = []
  priorityQ = queue.PriorityQueue()
  random.shuffle(items)
  allconstraints = []
  restrictSet = set()

  # Counts the number of connections to other classes
  connections = np.ones(N)

  
  for constraint in constraints:
    for c in constraint:
      connections[c] += len(constraint) - 1


  for i in items:
    # If this item restricts many other items if picked, decrease priority by division
    #exp = 0.4
    #
    # 0.65 for problem10, 0.75 for problem11, 0 for problem 12, 0.7 for problem13
    # 0 for problem14, 0.2 for problem15, 0.5 for problem16, 1 for problem17 and 18
    # 0 for problem19, 0.5 for problem20
    if i[4] - i[3] > 0:
      heuristic = (i[3]-i[4])/(connections[i[1]]**exp)
      priorityQ.put((heuristic,i))
    
  for i in range(N):
    #if(i%1000==0):
    print(i)
    maxItem = priorityQ.get()[1] 
    cond, temp = checkCons(maxItem[1], restrictSet, constraints)
    if cond:
      if itemWeight + maxItem[2] <= P and itemCost + maxItem[3] <= M:
        restrictSet = temp
        itemlist.append(maxItem[0])
        itemWeight += maxItem[2]
        itemCost += maxItem[3]
        itemProfit += maxItem[4]-maxItem[3]
  
  
  print ("Total Profit: ", itemProfit)
  
  
  return itemlist

def checkCons(lastItemAdded, restrictSet, constraints):
  if lastItemAdded in restrictSet:
    return (False, restrictSet)
  for constraint in constraints:
    if lastItemAdded in constraint:
      for item in constraint:
        if item != lastItemAdded:
          restrictSet.add(item)
  return (True, restrictSet)
      #check set to see if clash



def read_input(filename):
  """
  P: float
  M: float
  N: integer
  C: integer
  items: list of tuples
  constraints: list of sets
  """
  with open(filename) as f:
    P = float(f.readline())
    M = float(f.readline())
    N = int(f.readline())
    C = int(f.readline())
    items = []
    constraints = []
    for i in range(N):
      name, cls, weight, cost, val = f.readline().split(";")
      # if(float(cost) > float(val) or float(val) < 0):
      #   continue
      items.append((name, int(cls), float(weight), float(cost), float(val)))
    for i in range(C):
      constraint = set(eval(f.readline()))
      constraints.append(constraint)
  return P, M, N, C, items, constraints

def write_output(filename, items_chosen):
  with open(filename, "w") as f:
    for i in items_chosen:
      f.write("{0}\n".format(i))

if __name__ == "__main__":

  parser = argparse.ArgumentParser(description="PickItems solver.")
  parser.add_argument("input_file", type=str, help="____.in")
  parser.add_argument("output_file", type=str, help="____.out")
  args = parser.parse_args()

  P, M, N, C, items, constraints = read_input(args.input_file)
  items_chosen = solve(P, M, N, C, items, constraints)
  write_output(args.output_file, items_chosen)