// Bench for LeetCode #354 -- Go mirror of russian_doll.kara: sort by width
// ascending and height descending, then a patience-sorting LIS over heights.
package main

import (
	"fmt"
	"sort"
)

const rounds = 20
const count = 200000

type env struct{ w, h int64 }

func maxEnvelopes(envelopes []env) int64 {
	order := make([]env, len(envelopes))
	copy(order, envelopes)
	sort.SliceStable(order, func(i, j int) bool {
		if order[i].w != order[j].w {
			return order[i].w < order[j].w
		}
		return order[i].h > order[j].h
	})
	tails := []int64{}
	for _, e := range order {
		lo, hi := 0, len(tails)
		for lo < hi {
			mid := (lo + hi) / 2
			if tails[mid] < e.h {
				lo = mid + 1
			} else {
				hi = mid
			}
		}
		if lo == len(tails) {
			tails = append(tails, e.h)
		} else {
			tails[lo] = e.h
		}
	}
	return int64(len(tails))
}

func main() {
	var sink int64
	for round := int64(0); round < rounds; round++ {
		seed := int64(354) + round
		envelopes := []env{}
		for i := 0; i < count; i++ {
			seed = (seed*1103515245 + 12345) % 2147483648
			w := seed%100000 + 1
			seed = (seed*1103515245 + 12345) % 2147483648
			h := seed%100000 + 1
			envelopes = append(envelopes, env{w, h})
		}
		sink = (sink*31 + maxEnvelopes(envelopes) + round) % 1000000007
	}
	fmt.Println(sink)
}
