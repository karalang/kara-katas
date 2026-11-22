// LeetCode #2857: Count Pairs of Points With Distance k -- the bench:
// the ★ arm over 10 cases of 50000 points, LeetCode's most, every
// other one in a 256 x 256 square and the rest up to 10^6, with k up
// to 100, all drawn first, then each answered 3 times.
package main

import "fmt"

func countPairs(coordinates [][]int64, k int64) int64 {
	seen := map[[2]int64]int64{}
	var pairs int64
	for _, p := range coordinates {
		x, y := p[0], p[1]
		for a := int64(0); a <= k; a++ {
			pairs += seen[[2]int64{x ^ a, y ^ (k - a)}]
		}
		seen[[2]int64{x, y}]++
	}
	return pairs
}

var seed int64 = 2857

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wide() int64 {
	a := nextRandom()
	return a*32768 + nextRandom()
}

func main() {
	const count, rounds, n = 10, 3, 50000
	points := make([][][]int64, count)
	ks := make([]int64, count)
	for c := 0; c < count; c++ {
		top := int64(1000001)
		if c%2 == 0 {
			top = 256
		}
		ks[c] = nextRandom() % 101
		points[c] = make([][]int64, n)
		for i := 0; i < n; i++ {
			x := wide() % top
			y := wide() % top
			points[c][i] = []int64{x, y}
		}
	}
	var total, check int64
	for r := int64(0); r < rounds; r++ {
		for c := 0; c < count; c++ {
			pairs := countPairs(points[c], ks[c])
			total += pairs
			check = (check*31 + pairs + r) % 1000000007
		}
	}
	fmt.Printf("%d cases of %d points, %d rounds: %d pairs, checksum %d\n", count, n, rounds, total, check)
}
