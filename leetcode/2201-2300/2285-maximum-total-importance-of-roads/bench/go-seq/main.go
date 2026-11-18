// LeetCode #2285: Maximum Total Importance of Roads -- the bench, the ★
// arm's Go twin. The degrees sorted, the k-th smallest valued k.
package main

import (
	"fmt"
	"slices"
)

func maximumImportance(n int, roads [][2]int) int64 {
	degree := make([]int64, n)
	for _, r := range roads {
		degree[r[0]]++
		degree[r[1]]++
	}
	slices.Sort(degree)
	var total int64
	for i, d := range degree {
		total += d * int64(i+1)
	}
	return total
}

// ---- bench harness ---------------------------------------------------------

var seed int64 = 2285

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	graphs := make([][][2]int, 0, 200)
	for g := 0; g < 200; g++ {
		roads := make([][2]int, 0, 5000)
		for len(roads) < 5000 {
			a := nextRandom() * 32768
			a = (a + nextRandom()) % 5000
			b := nextRandom() * 32768
			b = (b + nextRandom()) % 5000
			if a != b {
				roads = append(roads, [2]int{int(a), int(b)})
			}
		}
		graphs = append(graphs, roads)
	}
	var check int64
	for p := 0; p < 20; p++ {
		for _, roads := range graphs {
			check = (check*31 + maximumImportance(5000, roads)) % 1000000007
		}
	}
	fmt.Printf("20 passes over 200 graphs of 5000 cities: checksum %d\n", check)
}
