# Word-Hunt-Solver
Solve Word Hunt Puzzles using OCR

## How it works
The algorithm first constructs a Trie for the provided Scrabble CSV dictionary. Users then present the puzzle to their computer camera, where it is located using OpenCV Canny Edge Detection methods. The captured puzzle is binarized via adaptive thresholding and segmented into individual cells, with each containing one letter. An OCR detects these letters and transfers them into a 4x4 array. The algorithm performs a Depth First Seach in union with a Trie query and then displays all valid words.

## YouTube Demo
Link: https://youtu.be/lmZfgbdRcZc 
