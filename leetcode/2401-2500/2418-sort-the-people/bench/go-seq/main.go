// LeetCode #2418: Sort the People -- the bench, the ★ arm in Go: the
// indexes sorted by height, tallest first, and each index's name read out.
package main

import (
	"fmt"
	"sort"
	"strings"
)

func sortPeople(names []string, heights []int64) []string {
	order := make([]int, len(names))
	for i := range order {
		order[i] = i
	}
	sort.SliceStable(order, func(a, b int) bool { return heights[order[a]] > heights[order[b]] })
	sorted := make([]string, 0, len(names))
	for _, i := range order {
		sorted = append(sorted, strings.Clone(names[i]))
	}
	return sorted
}

var seed int64 = 2418

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	// 10 groups of 1000 people, names of 1 to 20 letters, distinct heights
	// up to 10^5; each pass sorts every group and folds the first letter
	// of every name, plus the pass
	type group struct {
		names   []string
		heights []int64
	}
	var groups []group
	for g := 0; g < 10; g++ {
		var names []string
		for k := 0; k < 1000; k++ {
			n := 1 + nextRandom()%20
			b := make([]byte, n)
			for c := range b {
				b[c] = byte('a' + nextRandom()%26)
			}
			names = append(names, string(b))
		}
		pool := make([]int64, 100000)
		for i := range pool {
			pool[i] = int64(i + 1)
		}
		for i := int64(0); i < 1000; i++ {
			a := nextRandom()
			j := i + (a*32768+nextRandom())%(100000-i)
			pool[i], pool[j] = pool[j], pool[i]
		}
		groups = append(groups, group{names, append([]int64(nil), pool[:1000]...)})
	}
	var check int64
	for p := int64(0); p < 500; p++ {
		for _, g := range groups {
			for _, name := range sortPeople(g.names, g.heights) {
				check = (check*31 + int64(name[0]) + p) % 1000000007
			}
		}
	}
	fmt.Printf("500 passes over 10 groups of 1000 people: checksum %d\n", check)
}
