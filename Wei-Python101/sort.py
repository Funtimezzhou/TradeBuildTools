#!/usr/bin/python
# -*- coding: utf-8 -*-

# This script lists several sorting algorithms

# Author: Junqiang Zhou, 2017-06-03


# reference website
# http://python3.codes/popular-sorting-algorithms/

# ---------------------------------------------------------------------------------------#
# --------------------------------- Part1: Simple Sorts -------------------------------- #
# ---------------------------------------------------------------------------------------#
# 1. Bubble Sort
# Bubble sort algorithm starts at the beginning of the data set. It compares the first two elements, and if the first is greater than the second, it swaps them. It continues doing this for each pair of adjacent elements to the end of the data set. It then starts again with the first two elements, repeating until no swaps have occurred on the last pass. 
# This algorithm¡¯s average and worst-case performance is O(n^2), so it is rarely used to sort large, unordered data sets. Bubble sort can be used to sort a small number of items (where its asymptotic inefficiency is not a high penalty). 
def bubble_sort(seq):
    changed = True
    while changed:
        changed = False
        for i in range(len(seq) - 1):
            if seq[i] > seq[i+1]:
                seq[i], seq[i+1] = seq[i+1], seq[i]
                changed = True
    return None

# 2. Insertion Sort
# Insertion sort is an O(n2) sorting algorithm which moves elements one at a time into the correct position. The algorithm consists of inserting one element at a time into the previously sorted part of the array, moving higher ranked elements up as necessary. To start off, the first (or smallest, or any arbitrary) element of the unsorted array is considered to be the sorted part.
# Although insertion sort is an O(n2) algorithm, its simplicity, low overhead, good locality of reference and efficiency make it a good choice in two cases:
# (i) small n,
# (ii) as the final finishing-off algorithm for O(n logn) algorithms such as mergesort and quicksort.
def insertion_sort(seq):
    for i in range(1, len(seq)):
        j = i-1
        key = seq[i]
        while (seq[j] > key) and (j >= 0):
           seq[j+1] = seq[j]
           j -= 1
        seq[j+1] = key
    return None

# speed up insertion sort by using binary search in already sorted part
def insertion_sort_bin(seq):
    for i in range(1, len(seq)):
        key = seq[i]
        # invariant: ``seq[:i]`` is sorted        
        # find the least `low' such that ``seq[low]`` is not less then `key'.
        #   Binary search in sorted sequence ``seq[low:up]``:
        low, up = 0, i
        while up > low:
            middle = (low + up) // 2
            if seq[middle] < key:
                low = middle + 1             
            else:
                up = middle
        # insert key at position ``low``
        seq[:] = seq[:low] + [key] + seq[low:i] + seq[i + 1:]
    return None

# 3. Selection Sort
# Selection sort is an in-place comparison sort. It has O(n2) complexity, making it inefficient on large lists, and generally performs worse than the similar insertion sort. Selection sort is noted for its simplicity, and also has performance advantages over more complicated algorithms in certain situations. First find the smallest element in the array and swap it with the element in the first position, then find the second smallest element and swap it with the element in the second position, and continue in this way until the entire array is sorted. Its asymptotic complexity is O(n2) making it inefficient on large arrays. 
def selection_sort(seq):
    for i, e in enumerate(seq):
        mn = min(range(i,len(seq)), key=seq.__getitem__)
        seq[i], seq[mn] = seq[mn], e
    return seq

# ---------------------------------------------------------------------------------------#
# ------------------------------ Part2: Efficient Sorts -------------------------------- #
# ---------------------------------------------------------------------------------------#
# 1. Merge Sort
# Merge sort takes advantage of the ease of merging already sorted lists into a new sorted list. The basic idea is to split the collection into smaller groups by halving it until the groups only have one element or no elements (which are both entirely sorted groups). Then merge the groups back together so that their elements are in order. This is how the algorithm gets its ¡°divide and conquer¡± description.
# It is notable for having a worst case and average complexity of O(n*log(n)), and a best case complexity of O(n) (for pre-sorted input).
# Of the algorithms described here, this is the first that scales well to very large lists, because its worst-case running time is O(n log n). It is also easily applied to lists, not only arrays, as it only requires sequential access, not random access. However, it has additional O(n) space complexity, and involves a large number of copies in simple implementations.
from heapq import merge

def merge_sort(m):
    if len(m) <= 1:
        return m
  
    middle = len(m) // 2
    left = m[:middle]
    right = m[middle:]
  
    left = merge_sort(left)
    right = merge_sort(right)
    return list(merge(left, right))


# 2. Heap Sort
# Heapsort is an in-place sorting algorithm with worst case and average complexity of O(n?logn).
# The basic idea is to turn the array into a binary heap structure, which has the property that it allows efficient retrieval and removal of the maximal element. We repeatedly ¡°remove¡± the maximal element from the heap, thus building the sorted list from back to front. Heapsort requires random access, so can only be used on an array-like data structure.
# Heapsort is a much more efficient version of selection sort. It also works by determining the largest (or smallest) element of the list, placing that at the end (or beginning) of the list, then continuing with the rest of the list, but accomplishes this task efficiently by using a data structure called a heap, a special type of binary tree. Once the data list has been made into a heap, the root node is guaranteed to be the largest (or smallest) element. When it is removed and placed at the end of the list, the heap is rearranged so the largest element remaining moves to the root. Using the heap, finding the next largest element takes O(log n) time, instead of O(n) for a linear scan as in simple selection sort. This allows Heapsort to run in O(n logn) time, and this is also the worst case complexity.
def swap(i, j):                    
    list[i], list[j] = list[j], list[i] 
 
def heapify(end,i):   
    l=2 * i + 1 
    r=2 * (i + 1)   
    max=i   
    if l < end and list[i] < list[l]:   
        max = l   
    if r < end and list[max] < list[r]:   
        max = r   
    if max != i:   
        swap(i, max)   
        heapify(end, max)   

def heap_sort():     
    end = len(list)   
    start = end // 2 - 1
    for i in range(start, -1, -1):   
        heapify(end, i)   
    for i in range(end-1, 0, -1):   
        swap(i, 0)   
        heapify(i, 0)   


if __name__ == "__main__":
   seq = [0,4,6,15,34,9,3,2]
   print("Before Sort = ", seq)
   
   simplesort = "false"
   if simplesort:
      selection_sort(seq)
      print("After Sort = ", seq)
   else:
      list = seq 
      merge_sort()
      print("After Sort = ", seq)
