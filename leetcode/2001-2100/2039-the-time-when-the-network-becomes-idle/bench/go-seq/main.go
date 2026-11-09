// LeetCode #2039: The Time When the Network Becomes Idle -- the ★ arm in
// Go, the same algorithm and workload as network.kara: breadth-first search
// from the master with a slice queue, then each server's last message and
// its reply.
package main

import "fmt"

func networkBecomesIdle(edges [][]int64, patience []int64) int64 {
	n := len(patience)
	adjacent := make([][]int64, n)
	for _, e := range edges {
		adjacent[e[0]] = append(adjacent[e[0]], e[1])
		adjacent[e[1]] = append(adjacent[e[1]], e[0])
	}
	hops := make([]int64, n)
	for i := range hops {
		hops[i] = -1
	}
	hops[0] = 0
	queue := []int64{0}
	for head := 0; head < len(queue); head++ {
		u := queue[head]
		for _, v := range adjacent[u] {
			if hops[v] == -1 {
				hops[v] = hops[u] + 1
				queue = append(queue, v)
			}
		}
	}
	var idle int64
	for i := 1; i < n; i++ {
		roundTrip := 2 * hops[i]
		lastSent := (roundTrip - 1) / patience[i] * patience[i]
		idle = max(idle, lastSent+roundTrip+1)
	}
	return idle
}

var seed int64 = 2039

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

type pair struct{ u, v int64 }

func randomNetwork(n, reach, extra, top int64) ([][]int64, []int64) {
	edges := [][]int64{}
	joined := map[pair]bool{}
	for v := int64(1); v < n; v++ {
		hi := nextRandom()
		lo := nextRandom()
		u := v - 1 - (hi*32768+lo)%min(reach, v)
		edges = append(edges, []int64{u, v})
		joined[pair{u, v}] = true
	}
	tries := int64(0)
	for int64(len(edges)) < n-1+extra && tries < 4*extra {
		tries++
		h1, l1 := nextRandom(), nextRandom()
		a := (h1*32768 + l1) % n
		h2, l2 := nextRandom(), nextRandom()
		b := (h2*32768 + l2) % n
		u, v := min(a, b), max(a, b)
		if u != v && !joined[pair{u, v}] {
			joined[pair{u, v}] = true
			edges = append(edges, []int64{u, v})
		}
	}
	patience := []int64{0}
	for i := int64(1); i < n; i++ {
		patience = append(patience, nextRandom()%top+1)
	}
	return edges, patience
}

func main() {
	tops := []int64{100000, 3, 1000, 1}
	reaches := []int64{100000, 2, 50, 1}
	edges := make([][][]int64, 4)
	patience := make([][]int64, 4)
	for r := 0; r < 4; r++ {
		edges[r], patience[r] = randomNetwork(100000, reaches[r], 1, tops[r])
	}
	var calls, sum, check int64
	for round := int64(0); round < 25; round++ {
		for r := int64(0); r < 4; r++ {
			at := (round*7919+r*104729)%99999 + 1
			patience[r][at] = patience[r][at]%7 + 1
			answer := networkBecomesIdle(edges[r], patience[r])
			calls++
			sum += answer
			check = (check*31 + answer) % 1000000007
		}
	}
	fmt.Printf("%d calls: sum %d, checksum %d\n", calls, sum, check)
}
