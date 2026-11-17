// benchmark's Go mirror of archery.kara (LeetCode #2212, the ★ arm): all
// 2^12 sets of sections tried as bit masks, Bob paying alice[k] + 1 arrows
// for each, the best he can afford kept, and the arrows left over put in
// section 0.
package main

import "fmt"

func maximumBobPoints(numArrows int64, alice []int64) []int64 {
	bestMask, bestPoints := int64(0), int64(-1)
	for mask := int64(0); mask < 4096; mask++ {
		var cost, points int64
		for k := 0; k < 12; k++ {
			if mask>>k&1 == 1 {
				cost += alice[k] + 1
				points += int64(k)
			}
		}
		if cost <= numArrows && points > bestPoints {
			bestPoints = points
			bestMask = mask
		}
	}
	bob := make([]int64, 12)
	left := numArrows
	for k := 0; k < 12; k++ {
		if bestMask>>k&1 == 1 {
			bob[k] = alice[k] + 1
			left -= bob[k]
		}
	}
	bob[0] += left
	return bob
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	seed := int64(2212)
	ns := []int64{}
	alices := [][]int64{}
	for c := 0; c < 3000; c++ {
		// up to 10^5 arrows, Alice's shot into 12 sections in random shares
		n := nextRandom(&seed)*4%100000 + 1
		alice := make([]int64, 12)
		left := n
		for k := 0; k < 11; k++ {
			take := nextRandom(&seed) % (left/4 + 1)
			alice[k] = take
			left -= take
		}
		alice[11] = left
		ns = append(ns, n)
		alices = append(alices, alice)
	}
	check := int64(0)
	for c := range ns {
		bob := maximumBobPoints(ns[c], alices[c])
		for k := 0; k < 12; k++ {
			check = (check*31 + bob[k]) % 1000000007
		}
	}
	fmt.Printf("3000 contests: checksum %d\n", check)
}
