import cv2
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image
from imutils.perspective import four_point_transform
from imutils import contours
import imutils
import time
import sys
import warnings

import camera
import parseFrame

def getInputs():
    puzzle = None

    while(puzzle is None):
        puzzle = camera.scanPuzzle()
        puzzle = parseFrame.getCells(puzzle)

        if puzzle is not None:
            print(puzzle)

    return puzzle

class TrieNode:
    def __init__ (self):
        self.children = [None for _ in range(26)]
        self.endOfWord = False
        self.prefix = ""
    
class Trie:
    def __init__(self):
        self.root = self.newNode()
    
    def newNode(self):
        return TrieNode()
    
    def charConv(self, ch):
        return ord(ch) - ord('A')
    
    def insert(self, key):
        node = self.root
        length = len(key)
        for level in range(length):
            index = self.charConv(key[level])

            if node.children[index] is None:
                node.children[index] = self.newNode()
                node.children[index].prefix = node.prefix + key[level]
            node = node.children[index]

        node.endOfWord = True

    # For debugging purposes
    def search(self, key):
        node = self.root
        length = len(key)
        for level in range(length):
            index = self.charConv(key[level])

            if node.children[index] is None:
                return False
            node = node.children[index]
        return node.endOfWord

def buildTrie():
    df = pd.read_csv("word-hunt/scrable-words.csv", na_filter=False)
    words = df.values.tolist()

    words = [word[0] for word in words if len(word[0]) >= 3]

    trie = Trie()

    for word in words:
        trie.insert(word)

    return trie

solutions = []
offSet = [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]

def solve(puzzle, node, visited, i, j):
    if node.endOfWord:
        global solutions
        solutions.append(node.prefix)
    
    visited[i][j] = True

    global offSet

    for offset in offSet:
        new_i = i + offset[0]
        new_j = j + offset[1]
        if new_i < 0 or new_i >=4 or new_j < 0 or new_j >=4: continue
        index = trie.charConv(puzzle[new_i][new_j])
        if node.children[index] is not None and not visited[new_i][new_j]:
            solve(puzzle, node.children[index], visited, new_i, new_j)
            visited[new_i][new_j] = False
    return
    

if __name__ == "__main__":
    warnings.filterwarnings('ignore')
    sys.setrecursionlimit(10000)

    trie = buildTrie()

    puzzle = getInputs()

    root = trie.root

    for i in range(4):
        for j in range(4):     
            index = trie.charConv(puzzle[i][j])
            if root.children[index] is not None:
                visited = np.full((4,4), False)
                solve(puzzle, root.children[index], visited, i, j)

    solutions = list(set(solutions))
    solutions.sort(reverse=True, key=len)
    print("\n{} words found: ".format(len(solutions)))
    print(solutions)



    
    