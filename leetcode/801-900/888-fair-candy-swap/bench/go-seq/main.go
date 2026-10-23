// LeetCode #888 bench: Go mirror of fair_candy_swap.kara (the ★ arm, a set
// of Bob's boxes) on the same 2000 cases.
package main

import "fmt"

func fairCandySwap(aliceSizes, bobSizes []int64) []int64 {
	var aliceTotal, bobTotal int64
	for _, x := range aliceSizes {
		aliceTotal += x
	}
	bob := map[int64]struct{}{}
	for _, y := range bobSizes {
		bobTotal += y
		bob[y] = struct{}{}
	}
	d := (bobTotal - aliceTotal) / 2
	var best int64 = -1
	for _, x := range aliceSizes {
		if _, ok := bob[x+d]; ok && (best < 0 || x < best) {
			best = x
		}
	}
	return []int64{best, best + d}
}

var seed int64 = 888

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func below(limit int64) int64 {
	hi := nextRandom()
	return (hi*32768 + nextRandom()) % limit
}

// as in the Kāra bench: Alice's n boxes and Bob's m with a swap that
// evens the totals
func caseBoxes(n, m, most int64) ([]int64, []int64) {
	for {
		alice := []int64{}
		var aliceTotal int64
		for k := int64(0); k < n; k++ {
			x := 1 + below(most)
			alice = append(alice, x)
			aliceTotal += x
		}
		bob := []int64{}
		for k := int64(0); k < m; k++ {
			bob = append(bob, 1+below(most))
		}
		i := below(n)
		j := below(m)
		y := 1 + below(most)
		bob[j] = y
		var bobTotal int64
		for _, v := range bob {
			bobTotal += v
		}
		short := aliceTotal + 2*(y-alice[i]) - bobTotal
		for k := int64(0); k < m; k++ {
			if k != j && short != 0 {
				step := min(max(short, 1-bob[k]), most-bob[k])
				bob[k] += step
				short -= step
			}
		}
		for k := int64(0); k < n; k++ {
			if k != i && short != 0 {
				step := min(max(-short, 1-alice[k]), most-alice[k])
				alice[k] += step
				short += step
			}
		}
		if short == 0 && y != alice[i] {
			return alice, bob
		}
	}
}

func main() {
	var gives, takes, check int64
	for c := 0; c < 2000; c++ {
		n := 5000 + below(5001)
		m := 5000 + below(5001)
		alice, bob := caseBoxes(n, m, 100000)
		swap := fairCandySwap(alice, bob)
		gives += swap[0]
		takes += swap[1]
		check = (check*131 + swap[0]*7 + swap[1]) % 1000000007
	}
	fmt.Printf("2000 cases of 5000 to 10000 boxes: Alice gives %d candies, Bob %d, checksum %d\n", gives, takes, check)
}
