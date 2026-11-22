// LeetCode #2838: Maximum Coins Heroes Can Collect -- the bench, mirrored
// from coins.kara: sorted monsters, prefix sums, a binary search a hero.
package main

import (
	"fmt"
	"sort"
)

type pair struct{ power, coins int64 }

func maximumCoins(heroes, monsters, coins []int64) []int64 {
	pairs := make([]pair, len(monsters))
	for j := range monsters {
		pairs[j] = pair{monsters[j], coins[j]}
	}
	sort.Slice(pairs, func(a, b int) bool {
		if pairs[a].power != pairs[b].power {
			return pairs[a].power < pairs[b].power
		}
		return pairs[a].coins < pairs[b].coins
	})
	prefix := make([]int64, len(pairs)+1)
	for j, p := range pairs {
		prefix[j+1] = prefix[j] + p.coins
	}
	out := make([]int64, len(heroes))
	for i, h := range heroes {
		k := sort.Search(len(pairs), func(j int) bool { return pairs[j].power > h })
		out[i] = prefix[k]
	}
	return out
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func wide(seed *int64) int64 {
	hi := nextRandom(seed)
	return hi*32768 + nextRandom(seed)
}

func draw(n int, seed *int64) []int64 {
	xs := make([]int64, n)
	for i := range xs {
		xs[i] = wide(seed)%1000000000 + 1
	}
	return xs
}

func main() {
	const count, rounds, n = 10, 5, 100000
	seed := int64(2838)
	type battle struct{ heroes, monsters, coins []int64 }
	battles := make([]battle, 0, count)
	for c := 0; c < count; c++ {
		heroes := draw(n, &seed)
		monsters := draw(n, &seed)
		coins := draw(n, &seed)
		battles = append(battles, battle{heroes, monsters, coins})
	}
	var check int64
	for r := int64(0); r < rounds; r++ {
		for _, b := range battles {
			for _, x := range maximumCoins(b.heroes, b.monsters, b.coins) {
				check = (check*31 + x%1000000007 + r) % 1000000007
			}
		}
	}
	fmt.Printf("%d battles of %d, %d rounds: checksum %d\n", count, n, rounds, check)
}
