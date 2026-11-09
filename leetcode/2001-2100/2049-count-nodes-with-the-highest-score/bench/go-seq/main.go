// LeetCode #2049: Count Nodes With the Highest Score -- Go mirror of the ★
// arm's benchmark (highest.kara): the same 50 trees of 100000 nodes, the
// same explicit-stack preorder walked backwards.
package main

import "fmt"

var seed int64 = 2049

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func draw(n int, reach int64) []int64 {
	parents := make([]int64, n)
	kids := make([]int64, n)
	parents[0] = -1
	for i := 1; i < n; i++ {
		span := reach
		if int64(i) < span {
			span = int64(i)
		}
		at := i - int(nextRandom()%span+1)
		for kids[at] == 2 {
			at++
		}
		parents[i] = int64(at)
		kids[at]++
	}
	return parents
}

func countHighestScoreNodes(parents []int64) int64 {
	n := len(parents)
	children := make([][]int, n)
	root := 0
	for v := 0; v < n; v++ {
		if parents[v] == -1 {
			root = v
		} else {
			children[parents[v]] = append(children[parents[v]], v)
		}
	}
	order := []int{}
	stack := []int{root}
	for len(stack) > 0 {
		v := stack[len(stack)-1]
		stack = stack[:len(stack)-1]
		order = append(order, v)
		stack = append(stack, children[v]...)
	}
	size := make([]int64, n)
	for v := range size {
		size[v] = 1
	}
	for k := len(order) - 1; k >= 0; k-- {
		v := order[k]
		if parents[v] != -1 {
			size[parents[v]] += size[v]
		}
	}
	var best, count int64
	for v := 0; v < n; v++ {
		score := int64(n) - size[v]
		if score < 1 {
			score = 1
		}
		for _, c := range children[v] {
			score *= size[c]
		}
		if score > best {
			best, count = score, 1
		} else if score == best {
			count++
		}
	}
	return count
}

func main() {
	var sum, check int64
	for t := int64(0); t < 50; t++ {
		count := countHighestScoreNodes(draw(100000, 1+t*1000))
		sum += count
		check = (check*31 + count) % 1000000007
	}
	fmt.Printf("50 trees: sum %d, checksum %d\n", sum, check)
}
