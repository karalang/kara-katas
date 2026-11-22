// LeetCode #2813: Maximum Elegance of a K-Length Subsequence -- the bench
// in Go: the ★ arm over 10 cases of 10^5 items, profits up to 10^9 and
// categories up to 30000, k from 1 to 10^5, all drawn first, then each
// answered 5 times. The categories taken are a `map[int64]bool`.
package main

import (
	"fmt"
	"cmp"
	"slices"
)

func findMaximumElegance(items [][2]int64, k int) int64 {
	order := append([][2]int64(nil), items...)
	slices.SortStableFunc(order, func(a, b [2]int64) int { return cmp.Compare(b[0], a[0]) })
	seen := map[int64]bool{}
	repeats := []int64{}
	var total int64
	for _, item := range order[:k] {
		total += item[0]
		if seen[item[1]] {
			repeats = append(repeats, item[0])
		} else {
			seen[item[1]] = true
		}
	}
	d := int64(len(seen))
	best := total + d*d
	for _, item := range order[k:] {
		if len(repeats) == 0 {
			break
		}
		if !seen[item[1]] {
			seen[item[1]] = true
			total += item[0] - repeats[len(repeats)-1]
			repeats = repeats[:len(repeats)-1]
			d = int64(len(seen))
			best = max(best, total+d*d)
		}
	}
	return best
}

var seed int64 = 2813

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wide() int64 {
	a := nextRandom()
	return a*32768 + nextRandom()
}

func main() {
	count, rounds := 10, 5
	var n int64 = 100000
	cases := make([][][2]int64, count)
	ks := make([]int, count)
	for c := range cases {
		items := make([][2]int64, n)
		for i := range items {
			items[i][0] = wide()%1000000000 + 1
			items[i][1] = wide()%30000 + 1
		}
		cases[c] = items
		ks[c] = int(wide()%n + 1)
	}
	var total, check int64
	for r := int64(0); r < int64(rounds); r++ {
		for c := range cases {
			a := findMaximumElegance(cases[c], ks[c])
			total += a
			check = (check*31 + a%1000000007 + r) % 1000000007
		}
	}
	fmt.Printf("%d cases of %d, %d rounds: elegance sums to %d, checksum %d\n", count, n, rounds, total, check)
}
