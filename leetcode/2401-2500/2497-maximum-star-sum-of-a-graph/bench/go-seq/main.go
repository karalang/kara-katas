// LeetCode #2497: Maximum Star Sum of a Graph -- Go mirror of the
// benchmark (star_sum.kara): the same graph, passes and checksum; a slice
// of neighbours' values per node built on every ask, sorted and reversed.
package main

import (
	"fmt"
	"math"
	"slices"
)

var seed int64 = 2497

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wide() int64 {
	hi := nextRandom()
	return hi*32768 + nextRandom()
}

func maxStarSum(vals []int64, edges [][2]int64, k int64) int64 {
	n := len(vals)
	beside := make([][]int64, n)
	for _, e := range edges {
		beside[e[0]] = append(beside[e[0]], vals[e[1]])
		beside[e[1]] = append(beside[e[1]], vals[e[0]])
	}
	best := int64(math.MinInt64)
	for centre := 0; centre < n; centre++ {
		slices.Sort(beside[centre])
		slices.Reverse(beside[centre])
		sum := vals[centre]
		var taken int64
		for _, value := range beside[centre] {
			if taken == k || value <= 0 {
				break
			}
			sum += value
			taken++
		}
		if sum > best {
			best = sum
		}
	}
	return best
}

func main() {
	const n int64 = 100000
	const passes int64 = 125
	vals := make([]int64, n)
	for i := range vals {
		vals[i] = wide()%20001 - 10000
	}
	taken := map[int64]bool{}
	var edges [][2]int64
	for i := int64(0); i < n; i++ {
		a := wide() % n
		b := wide() % n
		key := min(a, b)*n + max(a, b)
		if a != b && !taken[key] {
			taken[key] = true
			edges = append(edges, [2]int64{a, b})
		}
	}
	var check int64
	for p := int64(0); p < passes; p++ {
		at := check % n
		was := vals[at]
		vals[at] = (check/n+p)%20001 - 10000
		k := check % 50
		check = (check*31 + maxStarSum(vals, edges, k) + p) % 1000000007
		vals[at] = was
	}
	fmt.Printf("%d passes over 10^5 nodes and %d edges: checksum %d\n", passes, len(edges), check)
}
