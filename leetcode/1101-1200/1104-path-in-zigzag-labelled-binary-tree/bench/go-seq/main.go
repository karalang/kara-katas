// LeetCode #1104: Path In Zigzag Labelled Binary Tree -- the bench in Go:
// the ★ arm (walking up, each parent half the label's mirror in its row)
// over every label from 1 to 10^6 in a different order each of 8 rounds.
package main

import "fmt"

func pathInZigZagTree(label int64) []int64 {
	depth := int64(1)
	for (int64(1) << depth) <= label {
		depth++
	}
	path := []int64{}
	node := label
	for depth > 0 {
		path = append(path, node)
		start, end := int64(1)<<(depth-1), (int64(1)<<depth)-1
		node = (start + end - node) / 2
		depth--
	}
	for i, j := 0, len(path)-1; i < j; i, j = i+1, j-1 {
		path[i], path[j] = path[j], path[i]
	}
	return path
}

func main() {
	var nodes, check int64
	for round := int64(0); round < 8; round++ {
		for i := int64(0); i < 1000000; i++ {
			label := (i*7919+round*104729)%1000000 + 1
			path := pathInZigZagTree(label)
			nodes += int64(len(path))
			check = (check*31 + path[len(path)/2]) % 1000000007
		}
	}
	fmt.Printf("8 rounds over the labels 1 to 10^6: %d nodes on their paths, checksum %d\n", nodes, check)
}
