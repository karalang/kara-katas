// LeetCode #2045: Second Minimum Time to Reach Destination -- the ★ arm in
// Go, the same algorithm and workload as second.kara: a breadth-first
// search keeping each vertex's two smallest walk lengths, then the lights.
package main

import "fmt"

func travel(steps, time, change int64) int64 {
	var t int64
	for i := int64(0); i < steps; i++ {
		if t/change%2 == 1 {
			t = (t/change + 1) * change
		}
		t += time
	}
	return t
}

func secondMinimum(n int64, edges [][2]int64, time, change int64) int64 {
	adjacent := make([][]int64, n+1)
	for _, e := range edges {
		adjacent[e[0]] = append(adjacent[e[0]], e[1])
		adjacent[e[1]] = append(adjacent[e[1]], e[0])
	}
	first := make([]int64, n+1)
	second := make([]int64, n+1)
	for i := range first {
		first[i], second[i] = -1, -1
	}
	first[1] = 0
	type item struct{ v, d int64 }
	queue := []item{{1, 0}}
	for head := 0; head < len(queue); head++ {
		u, d := queue[head].v, queue[head].d
		for _, v := range adjacent[u] {
			if first[v] == -1 {
				first[v] = d + 1
				queue = append(queue, item{v, d + 1})
			} else if second[v] == -1 && first[v] < d+1 {
				second[v] = d + 1
				queue = append(queue, item{v, d + 1})
			}
		}
	}
	return travel(second[n], time, change)
}

var seed int64 = 2045

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func graph(n, reach, extra int64) [][2]int64 {
	var edges [][2]int64
	seen := map[int64]bool{}
	for v := int64(2); v <= n; v++ {
		lim := reach
		if v-1 < lim {
			lim = v - 1
		}
		u := v - 1 - nextRandom()%lim
		edges = append(edges, [2]int64{u, v})
		seen[u*(n+1)+v] = true
	}
	tries := int64(0)
	for int64(len(edges)) < n-1+extra && tries < 4*extra {
		tries++
		a := nextRandom()%n + 1
		b := nextRandom()%n + 1
		u, v := a, b
		if b < a {
			u, v = b, a
		}
		if u != v && !seen[u*(n+1)+v] {
			seen[u*(n+1)+v] = true
			edges = append(edges, [2]int64{u, v})
		}
	}
	return edges
}

func main() {
	reaches := []int64{10000, 3, 2, 1}
	graphs := make([][][2]int64, 4)
	for r := range graphs {
		graphs[r] = graph(10000, reaches[r], 10001)
	}
	var calls, sum, check int64
	for round := int64(0); round < 250; round++ {
		for r := int64(0); r < 4; r++ {
			time := (round*7+r)%1000 + 1
			change := (round*13+r*5)%1000 + 1
			answer := secondMinimum(10000, graphs[r], time, change)
			calls++
			sum += answer
			check = (check*31 + answer) % 1000000007
		}
	}
	fmt.Printf("%d calls: sum %d, checksum %d\n", calls, sum, check)
}
