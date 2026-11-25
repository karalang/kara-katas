// LeetCode #1361 bench -- Go: every node's parents counted, one root and
// no node with two, then a search from the root that must reach all n.
package main

import "fmt"

func validateBinaryTreeNodes(n int32, leftChild, rightChild []int32) bool {
	parents := make([]int64, n)
	for i := int32(0); i < n; i++ {
		for _, child := range [2]int32{leftChild[i], rightChild[i]} {
			if child != -1 {
				parents[child]++
			}
		}
	}
	root := int64(-1)
	for i := int64(0); i < int64(n); i++ {
		if parents[i] > 1 {
			return false
		}
		if parents[i] == 0 {
			if root != -1 {
				return false
			}
			root = i
		}
	}
	if root == -1 {
		return false
	}
	seen := make([]bool, n)
	queue := []int64{root}
	head := 0
	for head < len(queue) {
		node := queue[head]
		head++
		if seen[node] {
			return false
		}
		seen[node] = true
		for _, child := range [2]int32{leftChild[node], rightChild[node]} {
			if child != -1 {
				queue = append(queue, int64(child))
			}
		}
	}
	return head == int(n)
}

var seed int64 = 1361

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

// n nodes made into one binary tree, each node after the first hung on a
// free side of a node already placed; then, one time in two, broken or not
func randomCase(n int64) ([]int32, []int32) {
	left := make([]int32, n)
	right := make([]int32, n)
	order := make([]int64, n)
	for i := range left {
		left[i] = -1
		right[i] = -1
		order[i] = int64(i)
	}
	for i := int64(1); i < n; i++ {
		j := nextRandom() % (i + 1)
		order[i], order[j] = order[j], order[i]
	}
	for i := int64(1); i < n; i++ {
		for {
			parent := order[nextRandom()%i]
			if nextRandom()%2 == 0 {
				if left[parent] == -1 {
					left[parent] = int32(order[i])
					break
				}
			} else if right[parent] == -1 {
				right[parent] = int32(order[i])
				break
			}
		}
	}
	node := nextRandom() % n
	other := int32(nextRandom() % n)
	switch nextRandom() % 6 {
	case 0:
		if left[node] == -1 {
			left[node] = other
		} else if right[node] == -1 {
			right[node] = other
		}
	case 1:
		left[node] = -1
	case 2:
		if right[node] != -1 {
			right[node] = other
		}
	}
	return left, right
}

func main() {
	// 20 sets of 5000 nodes made once; then 5000 questions, each set drawn
	// from the checksum so far, every answer folded into it
	lefts := make([][]int32, 20)
	rights := make([][]int32, 20)
	for s := range lefts {
		lefts[s], rights[s] = randomCase(5000)
	}
	var check int64
	for r := int64(0); r < 5000; r++ {
		s := check % 20
		got := int64(0)
		if validateBinaryTreeNodes(5000, lefts[s], rights[s]) {
			got = 1
		}
		check = (check*31 + got + r) % 1000000007
	}
	fmt.Printf("5000 questions: checksum %d\n", check)
}
