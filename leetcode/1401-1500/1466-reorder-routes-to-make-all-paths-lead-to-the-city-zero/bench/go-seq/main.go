// LeetCode #1466 bench in Go: the ★ arm (a breadth-first search out of
// city 0 over the roads taken both ways) on the same 10 trees of 50000
// cities and 20 passes.
package main

import "fmt"

type road struct{ next, away int32 }

func minReorder(n int32, connections [][]int32) int32 {
	roads := make([][]road, n)
	for _, c := range connections {
		roads[c[0]] = append(roads[c[0]], road{c[1], 1})
		roads[c[1]] = append(roads[c[1]], road{c[0], 0})
	}
	seen := make([]bool, n)
	queue := []int32{0}
	seen[0] = true
	var turned int32
	for len(queue) > 0 {
		city := queue[0]
		queue = queue[1:]
		for _, r := range roads[city] {
			if !seen[r.next] {
				seen[r.next] = true
				turned += r.away
				queue = append(queue, r.next)
			}
		}
	}
	return turned
}

var seed int64 = 1466

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const n = 50000
	trees := make([][][]int32, 10)
	for t := range trees {
		label := make([]int32, n)
		for c := range label {
			label[c] = int32(c)
		}
		for i := int64(n - 1); i >= 1; i-- {
			j := nextRandom() % (i + 1)
			label[i], label[j] = label[j], label[i]
		}
		roads := make([][]int32, 0, n-1)
		for i := int64(1); i < n; i++ {
			p := nextRandom() % i
			if nextRandom()%2 == 0 {
				roads = append(roads, []int32{label[i], label[p]})
			} else {
				roads = append(roads, []int32{label[p], label[i]})
			}
		}
		trees[t] = roads
	}
	var check int64
	for pass := int64(0); pass < 20; pass++ {
		for t := 0; t < 10; t++ {
			k := check % (n - 1)
			r := trees[t][k]
			r[0], r[1] = r[1], r[0]
			got := minReorder(n, trees[t])
			check = (check*31 + int64(got) + pass) % 1000000007
		}
	}
	fmt.Printf("20 passes over 10 trees of 50000 cities: checksum %d\n", check)
}
