// LeetCode #1276 bench, in Go: the ★ arm (by algebra) on 100,000 random
// pairs of tomato and cheese slice counts up to 10^7, a third made from
// burgers and a third near such a count, drawn once; 1000 rounds, every
// answer folded into a checksum.
package main

import "fmt"

func numOfBurgers(t, c int64) []int64 {
	if t%2 != 0 {
		return []int64{}
	}
	jumbo := t/2 - c
	small := 2*c - t/2
	if jumbo < 0 || small < 0 {
		return []int64{}
	}
	return []int64{jumbo, small}
}

var seed int64 = 1276

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	ts := make([]int64, 0, 100000)
	cs := make([]int64, 0, 100000)
	for k := 0; k < 100000; k++ {
		jumbo := nextRandom() % 2500000
		small := nextRandom() % 2500000
		var t, c int64
		if k%3 == 0 {
			t, c = 4*jumbo+2*small, jumbo+small
		} else if k%3 == 1 {
			t = 4*jumbo + 2*small + nextRandom()%5 - 2
			c = jumbo + small + nextRandom()%3 - 1
		} else {
			t = nextRandom() % 10000001
			c = nextRandom() % 5000001
		}
		ts = append(ts, max(t, 0))
		cs = append(cs, max(c, 0))
	}
	var check int64
	for round := int64(0); round < 1000; round++ {
		for k := range ts {
			answer := numOfBurgers(ts[k]+round, cs[k])
			if len(answer) == 2 {
				check = (check*131 + answer[0]*7 + answer[1]) % 1000000007
			} else {
				check = (check*131 + 1) % 1000000007
			}
		}
	}
	fmt.Printf("1000 rounds of 100000 pairs: checksum %d\n", check)
}
