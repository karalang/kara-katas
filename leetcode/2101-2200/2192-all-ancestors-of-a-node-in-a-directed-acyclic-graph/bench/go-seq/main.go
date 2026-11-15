// benchmark's Go mirror of ancestors.kara (LeetCode #2192, the ★ arm): a
// walk down from every node by a stack.
package main

import "fmt"

func getAncestors(n int, edges [][2]int) [][]int {
	children := make([][]int, n)
	for _, e := range edges {
		children[e[0]] = append(children[e[0]], e[1])
	}
	ancestors := make([][]int, n)
	for start := 0; start < n; start++ {
		seen := make([]bool, n)
		seen[start] = true
		stack := []int{start}
		for len(stack) > 0 {
			u := stack[len(stack)-1]
			stack = stack[:len(stack)-1]
			for _, v := range children[u] {
				if !seen[v] {
					seen[v] = true
					ancestors[v] = append(ancestors[v], start)
					stack = append(stack, v)
				}
			}
		}
	}
	return ancestors
}

var seed int64 = 2192

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomDag() [][2]int {
	order := make([]int, 1000)
	for i := range order {
		order[i] = i
	}
	for i := 999; i >= 1; i-- {
		j := int(nextRandom() % int64(i+1))
		order[i], order[j] = order[j], order[i]
	}
	edges := make([][2]int, 0, 2000)
	for len(edges) < 2000 {
		a := int(nextRandom() % 1000)
		b := int(nextRandom() % 1000)
		if a < b {
			edges = append(edges, [2]int{order[a], order[b]})
		} else if b < a {
			edges = append(edges, [2]int{order[b], order[a]})
		}
	}
	return edges
}

func main() {
	dags := make([][][2]int, 20)
	for d := range dags {
		dags[d] = randomDag()
	}
	var check int64
	for r := 0; r < 2000; r++ {
		for _, list := range getAncestors(1000, dags[r%20]) {
			check = (check*31 + int64(len(list))) % 1000000007
			for _, a := range list {
				check = (check*31 + int64(a) + 1) % 1000000007
			}
		}
	}
	fmt.Printf("2000 solves: checksum %d\n", check)
}
