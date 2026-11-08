// LeetCode #1519 bench: the ★ arm (counts returned up a recursive walk),
// as labels.kara.
package main

import "fmt"

func walk(node, parent int64, adjacent [][]int64, labels []byte, answer []int64) []int64 {
	counts := make([]int64, 26)
	for _, next := range adjacent[node] {
		if next != parent {
			below := walk(next, node, adjacent, labels, answer)
			for c := 0; c < 26; c++ {
				counts[c] += below[c]
			}
		}
	}
	mine := int64(labels[node]) - 97
	counts[mine]++
	answer[node] = counts[mine]
	return counts
}

func countSubTrees(n int64, edges [][2]int64, labels string) []int64 {
	adjacent := make([][]int64, n)
	for _, e := range edges {
		adjacent[e[0]] = append(adjacent[e[0]], e[1])
		adjacent[e[1]] = append(adjacent[e[1]], e[0])
	}
	answer := make([]int64, n)
	walk(0, -1, adjacent, []byte(labels), answer)
	return answer
}

var seed int64 = 1519

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const n int64 = 200000
	edges := make([][2]int64, 0, n-1)
	for i := int64(1); i < n; i++ {
		a := nextRandom()
		edges = append(edges, [2]int64{(a*32768 + nextRandom()) % i, i})
	}
	labels := make([]byte, n)
	for i := range labels {
		labels[i] = byte(97 + nextRandom()%26)
	}
	var check int64
	for r := 0; r < 5; r++ {
		for _, x := range countSubTrees(n, edges, string(labels)) {
			check = (check*31 + x + 1) % 1000000007
		}
	}
	fmt.Printf("5 passes over a tree of 200000 nodes: checksum %d\n", check)
}
