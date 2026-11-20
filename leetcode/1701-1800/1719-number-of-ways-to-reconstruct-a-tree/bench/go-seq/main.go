// LeetCode #1719: Number Of Ways To Reconstruct A Tree -- the bench
// (ways.kara): the nodes by degree, most first, each hung under the last
// earlier neighbour, which must hold every other neighbour of it.
package main

import (
	"fmt"
	"sort"
)

func checkWays(pairs [][2]int32) int32 {
	const size = 501
	linked := make([][]bool, size)
	for i := range linked {
		linked[i] = make([]bool, size)
	}
	degree := make([]int64, size)
	for _, p := range pairs {
		x, y := p[0], p[1]
		linked[x][y] = true
		linked[y][x] = true
		degree[x]++
		degree[y]++
	}
	nodes := []int{}
	for v := 0; v < size; v++ {
		if degree[v] > 0 {
			nodes = append(nodes, v)
		}
	}
	n := int64(len(nodes))
	sort.SliceStable(nodes, func(a, b int) bool { return degree[nodes[a]] > degree[nodes[b]] })
	if degree[nodes[0]] != n-1 {
		return 0
	}
	var ways int32 = 1
	for i := 1; i < len(nodes); i++ {
		v := nodes[i]
		parent := -1
		for j := i - 1; j >= 0; j-- {
			if linked[v][nodes[j]] {
				parent = nodes[j]
				break
			}
		}
		if parent < 0 {
			return 0
		}
		for _, u := range nodes {
			if u != parent && linked[v][u] && !linked[parent][u] {
				return 0
			}
		}
		if degree[parent] == degree[v] {
			ways = 2
		}
	}
	return ways
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func draw(seed *int64) [][2]int32 {
	const k = 500
	labels := make([]int32, 500)
	for i := range labels {
		labels[i] = int32(i + 1)
	}
	for i := 0; i < k; i++ {
		j := i + int(nextRandom(seed)%int64(500-i))
		labels[i], labels[j] = labels[j], labels[i]
	}
	have := make([][]bool, k)
	for i := range have {
		have[i] = make([]bool, k)
	}
	parent := make([]int64, k)
	parent[0] = -1
	for i := int64(1); i < k; i++ {
		if nextRandom(seed)%2 == 0 {
			parent[i] = nextRandom(seed) % i
		} else {
			parent[i] = i - 1 - nextRandom(seed)%min(i, 4)
		}
	}
	for i := 1; i < k; i++ {
		a := parent[i]
		for a >= 0 {
			have[i][a] = true
			have[a][i] = true
			a = parent[a]
		}
	}
	mode := nextRandom(seed) % 3
	i := nextRandom(seed) % k
	j := nextRandom(seed) % k
	if i != j && mode > 0 {
		have[i][j] = mode == 2
		have[j][i] = mode == 2
	}
	pairs := [][2]int32{}
	for i := 0; i < k; i++ {
		for j := i + 1; j < k; j++ {
			if have[i][j] {
				pairs = append(pairs, [2]int32{min(labels[i], labels[j]), max(labels[i], labels[j])})
			}
		}
	}
	return pairs
}

func main() {
	count := 50
	var rounds int64 = 50
	var seed int64 = 1719
	problems := make([][][2]int32, count)
	pairs := 0
	for c := range problems {
		problems[c] = draw(&seed)
		pairs += len(problems[c])
	}
	var sum, check int64
	for r := int64(0); r < rounds; r++ {
		for _, p := range problems {
			answer := int64(checkWays(p))
			sum += answer
			check = (check*31 + answer + r) % 1000000007
		}
	}
	fmt.Printf("%d problems of 500 nodes, %d pairs, %d rounds: answers sum to %d, checksum %d\n", count, pairs, rounds, sum, check)
}
