// LeetCode #2101: Detonate the Maximum Bombs -- Go mirror of the ★ arm's
// benchmark (detonate.kara): the same 2000 fields of 100 bombs, adjacency
// lists and a breadth-first search from each bomb with a slice as the
// queue.
package main

import "fmt"

func maximumDetonation(bombs [][3]int64) int64 {
	n := len(bombs)
	reach := make([][]int, n)
	for i := 0; i < n; i++ {
		for j := 0; j < n; j++ {
			dx := bombs[i][0] - bombs[j][0]
			dy := bombs[i][1] - bombs[j][1]
			if i != j && dx*dx+dy*dy <= bombs[i][2]*bombs[i][2] {
				reach[i] = append(reach[i], j)
			}
		}
	}
	var best int64
	for start := 0; start < n; start++ {
		seen := make([]bool, n)
		seen[start] = true
		queue := []int{start}
		var count int64
		for len(queue) > 0 {
			i := queue[0]
			queue = queue[1:]
			count++
			for _, j := range reach[i] {
				if !seen[j] {
					seen[j] = true
					queue = append(queue, j)
				}
			}
		}
		if count > best {
			best = count
		}
	}
	return best
}

var seed int64 = 2101

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	var total, check int64
	for f := 0; f < 2000; f++ {
		bombs := make([][3]int64, 100)
		for i := range bombs {
			x := nextRandom()%1000 + 1
			y := nextRandom()%1000 + 1
			r := nextRandom()%150 + 1
			bombs[i] = [3]int64{x, y, r}
		}
		got := maximumDetonation(bombs)
		total += got
		check = (check*31 + got) % 1000000007
	}
	fmt.Printf("2000 fields: %d bombs in all, checksum %d\n", total, check)
}
