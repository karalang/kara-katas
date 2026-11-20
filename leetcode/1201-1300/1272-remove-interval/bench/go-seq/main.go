// LeetCode #1272 bench, in Go: the ★ arm (one pass; an interval the cut
// misses kept whole, one it meets keeping its parts before and after) on 20
// random lists of 10,000 intervals drawn once, each cut three ways, 40
// rounds; every interval kept folded into a checksum. Each interval is its
// own two-element array, as LeetCode's `int[][]` is.
package main

import "fmt"

func removeInterval(intervals [][]int64, toBeRemoved []int64) [][]int64 {
	lo, hi := toBeRemoved[0], toBeRemoved[1]
	var out [][]int64
	for _, iv := range intervals {
		a, b := iv[0], iv[1]
		if b <= lo || a >= hi {
			out = append(out, []int64{a, b})
			continue
		}
		if a < lo {
			out = append(out, []int64{a, lo})
		}
		if b > hi {
			out = append(out, []int64{hi, b})
		}
	}
	return out
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	seed := int64(1272)
	lists := make([][][]int64, 20)
	for l := range lists {
		at := int64(-1000000)
		for i := 0; i < 10000; i++ {
			a := at + nextRandom(&seed)%50
			b := a + 1 + nextRandom(&seed)%50
			lists[l] = append(lists[l], []int64{a, b})
			at = b
		}
	}
	cuts := [][]int64{{-990000, -800000}, {-700000, -699990}, {-1000000, 1000000}}
	var check int64
	for round := int64(0); round < 40; round++ {
		for _, list := range lists {
			for _, cut := range cuts {
				kept := removeInterval(list, cut)
				check = (check*131 + int64(len(kept)) + round) % 1000000007
				for _, iv := range kept {
					check = (check*131 + iv[0] + iv[1] + 2000000) % 1000000007
				}
			}
		}
	}
	fmt.Printf("40 rounds of 20 lists cut 3 ways: checksum %d\n", check)
}
