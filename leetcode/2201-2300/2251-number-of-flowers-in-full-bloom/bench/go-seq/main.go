// LeetCode #2251: Number of Flowers in Full Bloom -- the benchmark's Go
// mirror of flowers.kara: the starts and the ends sorted once, and each
// person the starts of at most t less the ends before t, by two
// sort.Search calls.
package main

import (
	"fmt"
	"slices"
	"sort"
)

func fullBloomFlowers(flowers [][2]int64, people []int64) []int64 {
	starts := make([]int64, len(flowers))
	ends := make([]int64, len(flowers))
	for i, f := range flowers {
		starts[i] = f[0]
		ends[i] = f[1]
	}
	slices.Sort(starts)
	slices.Sort(ends)
	counts := make([]int64, len(people))
	for i, t := range people {
		began := sort.Search(len(starts), func(k int) bool { return starts[k] > t })
		over := sort.Search(len(ends), func(k int) bool { return ends[k] >= t })
		counts[i] = int64(began - over)
	}
	return counts
}

var seed int64 = 2251

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wideRandom() int64 {
	high := nextRandom()
	return high*32768 + nextRandom()
}

func main() {
	var check int64
	for t := 0; t < 20; t++ {
		flowers := make([][2]int64, 50000)
		for i := range flowers {
			a := wideRandom()%1000000000 + 1
			b := wideRandom()%1000000000 + 1
			flowers[i] = [2]int64{min(a, b), max(a, b)}
		}
		people := make([]int64, 50000)
		for i := range people {
			people[i] = wideRandom()%1000000000 + 1
		}
		for _, c := range fullBloomFlowers(flowers, people) {
			check = (check*31 + c) % 1000000007
		}
	}
	fmt.Printf("20 cases of 5 * 10^4 flowers and people: checksum %d\n", check)
}
