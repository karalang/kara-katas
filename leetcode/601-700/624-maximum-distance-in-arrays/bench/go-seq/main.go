// LeetCode #624: Maximum Distance in Arrays -- Go mirror of the Kāra
// bench.
//
// The ★ arm's one pass over the same inputs and rounds.
package main

import (
	"fmt"
	"sort"
)

func maxDistance(arrays [][]int64) int64 {
	low := arrays[0][0]
	high := arrays[0][len(arrays[0])-1]
	var best int64
	for _, a := range arrays[1:] {
		first := a[0]
		last := a[len(a)-1]
		if last-low > best {
			best = last - low
		}
		if high-first > best {
			best = high - first
		}
		if first < low {
			low = first
		}
		if last > high {
			high = last
		}
	}
	return best
}

var seed int64 = 624

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomArrays(count, spread int64) [][]int64 {
	arrays := make([][]int64, 0, count)
	for i := int64(0); i < count; i++ {
		n := 1 + nextRandom()%9
		values := make([]int64, 0, n)
		for j := int64(0); j < n; j++ {
			values = append(values, nextRandom()%(2*spread+1)-spread)
		}
		sort.Slice(values, func(a, b int) bool { return values[a] < values[b] })
		arrays = append(arrays, values)
	}
	return arrays
}

func main() {
	const inputs = 20
	const rounds = 2000
	all := make([][][]int64, 0, inputs)
	for i := 0; i < inputs; i++ {
		spread := 1000 + nextRandom()%9001
		all = append(all, randomArrays(20000, spread))
	}
	var sum, checksum int64
	for r := 0; r < rounds; r++ {
		d := maxDistance(all[(r*7)%inputs])
		sum += d
		checksum = (checksum*31 + d) % 1000000007
	}
	fmt.Printf("%d inputs, %d rounds: total %d, checksum %d\n", inputs, rounds, sum, checksum)
}
