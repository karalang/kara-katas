// LeetCode #954: Array of Doubled Pairs -- Go mirror of the Kara bench
// program (counts, smallest first).
package main

import (
	"fmt"
	"sort"
)

func abs(x int64) int64 {
	if x < 0 {
		return -x
	}
	return x
}

func canReorderDoubled(arr []int64) bool {
	count := map[int64]int64{}
	for _, x := range arr {
		count[x]++
	}
	values := make([]int64, 0, len(count))
	for x := range count {
		values = append(values, x)
	}
	sort.Slice(values, func(i, j int) bool { return abs(values[i]) < abs(values[j]) })
	for _, x := range values {
		c := count[x]
		if c == 0 {
			continue
		}
		if x == 0 {
			if c%2 != 0 {
				return false
			}
			continue
		}
		d := count[2*x]
		if d < c {
			return false
		}
		count[2*x] = d - c
	}
	return true
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	rounds, count, n := 10, 20, 30000
	seed := int64(954)
	sets := [][]int64{}
	for s := 0; s < count; s++ {
		arr := make([]int64, 0, n)
		for i := 0; i < n/2; i++ {
			a := nextRandom(&seed)
			x := (a*32768+nextRandom(&seed))%100001 - 50000
			arr = append(arr, x, 2*x)
		}
		for i := 0; i < n; i++ {
			a := nextRandom(&seed)
			j := i + int((a*32768+nextRandom(&seed))%int64(n-i))
			arr[i], arr[j] = arr[j], arr[i]
		}
		if s%4 == 3 {
			arr[s*1000] = 2*(arr[s*1000]/2) + 1
		}
		sets = append(sets, arr)
	}
	yes, check := int64(0), int64(0)
	for r := 0; r < rounds; r++ {
		for i := 0; i < count; i++ {
			k := (r + i) % count
			ok := canReorderDoubled(sets[k])
			if ok {
				yes++
			}
			v := int64(2)
			if ok {
				v = 1
			}
			check = (check*31 + v) % 1000000007
		}
	}
	fmt.Printf("%d rounds over %d sets of %d values: %d can be paired, checksum %d\n", rounds, count, n, yes, check)
}
