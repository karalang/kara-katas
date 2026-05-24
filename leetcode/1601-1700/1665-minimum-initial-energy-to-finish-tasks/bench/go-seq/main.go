// LeetCode #1665 — Go seq bench peer for greedy.kara. Same algorithm,
// same workload, same sink as the Kara/Rust/C mirrors.

package main

import (
	"fmt"
	"sort"
)

func minimumEffort(tasks [][2]int64) int64 {
	ordered := make([][2]int64, len(tasks))
	copy(ordered, tasks)
	sort.Slice(ordered, func(i, j int) bool {
		return (ordered[i][1]-ordered[i][0]) > (ordered[j][1]-ordered[j][0])
	})

	var energy, spent int64
	for _, t := range ordered {
		need := spent + t[1]
		if need > energy {
			energy = need
		}
		spent += t[0]
	}
	return energy
}

func main() {
	const n int64 = 50000
	data := make([][2]int64, n)
	for i := int64(0); i < n; i++ {
		actual := (i*7)%100 + 1
		minimum := actual + (i*13)%50
		data[i] = [2]int64{actual, minimum}
	}

	var sum int64
	for k := 0; k < 5; k++ {
		sum += minimumEffort(data)
	}
	fmt.Println(sum)
}
