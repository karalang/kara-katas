// LeetCode #1387 bench -- Go: the ★ arm: each value walked only until it
// meets one whose power is known, in a map that every walk fills on its
// way back; the (power, value) pairs sorted and the k-th read off.
package main

import (
	"fmt"
	"sort"
)

func getKth(lo, hi, k int32) int32 {
	known := map[int64]int32{1: 0}
	keyed := make([][2]int32, 0, hi-lo+1)
	for x := lo; x <= hi; x++ {
		path := []int64{}
		v := int64(x)
		for {
			if _, ok := known[v]; ok {
				break
			}
			path = append(path, v)
			if v%2 == 0 {
				v /= 2
			} else {
				v = 3*v + 1
			}
		}
		steps := known[v]
		for len(path) > 0 {
			p := path[len(path)-1]
			path = path[:len(path)-1]
			steps++
			known[p] = steps
		}
		keyed = append(keyed, [2]int32{known[int64(x)], x})
	}
	sort.Slice(keyed, func(a, b int) bool {
		if keyed[a][0] != keyed[b][0] {
			return keyed[a][0] < keyed[b][0]
		}
		return keyed[a][1] < keyed[b][1]
	})
	return keyed[k-1][1]
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	seed := int64(1387)
	check := int64(0)
	for q := 0; q < 4000; q++ {
		seed = (seed + check) % 2147483648
		lo := 1 + nextRandom(&seed)%200
		hi := 800 + nextRandom(&seed)%201
		k := 1 + nextRandom(&seed)%(hi-lo+1)
		check = (check*131 + int64(getKth(int32(lo), int32(hi), int32(k)))) % 1000000007
	}
	fmt.Printf("4000 queries over ranges up to 1 to 1000: checksum %d\n", check)
}
