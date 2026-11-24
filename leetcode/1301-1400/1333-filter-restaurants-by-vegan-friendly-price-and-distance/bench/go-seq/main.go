// LeetCode #1333 bench, Go mirror of the Kāra bench: the ★ arm on 20 lists
// of 10^4 restaurants built once, then 100 passes, each setting one rating
// of every list from the checksum so far and drawing the filters from it
// too, answering every list.
package main

import (
	"cmp"
	"fmt"
	"slices"
)

type pair struct {
	rating int32
	id     int32
}

func filterRestaurants(restaurants [][]int32, veganFriendly, maxPrice, maxDistance int32) []int32 {
	kept := []pair{}
	for _, r := range restaurants {
		if (veganFriendly == 0 || r[2] == 1) && r[3] <= maxPrice && r[4] <= maxDistance {
			kept = append(kept, pair{r[1], r[0]})
		}
	}
	slices.SortFunc(kept, func(a, b pair) int {
		if c := cmp.Compare(b.rating, a.rating); c != 0 {
			return c
		}
		return cmp.Compare(b.id, a.id)
	})
	ids := make([]int32, len(kept))
	for i, p := range kept {
		ids[i] = p.id
	}
	return ids
}

var seed int64 = 1333

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const n = 10000
	lists := make([][][]int32, 20)
	for t := range lists {
		list := make([][]int32, n)
		for i := int64(0); i < n; i++ {
			id := int32(i*10 + 1 + nextRandom()%10)
			rating := int32(1 + nextRandom()%100000)
			vegan := int32(nextRandom() % 2)
			price := int32(1 + nextRandom()%100000)
			distance := int32(1 + nextRandom()%100000)
			list[i] = []int32{id, rating, vegan, price, distance}
		}
		lists[t] = list
	}
	var check int64
	for pass := int64(0); pass < 100; pass++ {
		vegan := int32(pass % 2)
		maxPrice := int32(50000 + check%50001)
		maxDistance := int32(50000 + check/7%50001)
		for t := 0; t < 20; t++ {
			at := check % n
			lists[t][at][1] = int32(1 + check/3%100000)
			ids := filterRestaurants(lists[t], vegan, maxPrice, maxDistance)
			k := len(ids)
			check = (check*31 + int64(k) + int64(ids[0]) + int64(ids[k/2]) + pass) % 1000000007
		}
	}
	fmt.Printf("100 passes over 20 lists of 10^4: checksum %d\n", check)
}
