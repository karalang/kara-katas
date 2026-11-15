// benchmark's Go mirror of jumbled.kara (LeetCode #2191, the ★ arm), over
// a slice of the row: (value, place) pairs sorted.
package main

import (
	"fmt"
	"sort"
)

type pair struct {
	value, place int64
}

func mapped(mapping []int64, n int64) int64 {
	if n == 0 {
		return mapping[0]
	}
	var value, place int64 = 0, 1
	for n > 0 {
		value += mapping[n%10] * place
		place *= 10
		n /= 10
	}
	return value
}

func sortJumbled(mapping []int64, nums []int64) []int64 {
	keyed := make([]pair, len(nums))
	for i, x := range nums {
		keyed[i] = pair{mapped(mapping, x), int64(i)}
	}
	sort.Slice(keyed, func(a, b int) bool {
		if keyed[a].value != keyed[b].value {
			return keyed[a].value < keyed[b].value
		}
		return keyed[a].place < keyed[b].place
	})
	out := make([]int64, len(nums))
	for i, k := range keyed {
		out[i] = nums[k.place]
	}
	return out
}

var seed int64 = 2191

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func bigRandom() int64 {
	a := nextRandom()
	b := nextRandom()
	return a*32768 + b
}

func main() {
	row := make([]int64, 1000000)
	for i := range row {
		row[i] = bigRandom() % 1000000000
	}
	var check int64
	for r := 0; r < 200; r++ {
		mapping := make([]int64, 10)
		for d := range mapping {
			mapping[d] = int64(d)
		}
		for i := 9; i >= 1; i-- {
			j := nextRandom() % int64(i+1)
			mapping[i], mapping[j] = mapping[j], mapping[i]
		}
		start := bigRandom() % 970001
		for _, x := range sortJumbled(mapping, row[start:start+30000]) {
			check = (check*31 + x%1000003) % 1000000007
		}
	}
	fmt.Printf("200 solves: checksum %d\n", check)
}
