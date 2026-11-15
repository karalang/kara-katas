// LeetCode #2164: Sort Even and Odd Indices Independently -- the
// benchmark's Go mirror of parity.kara.
package main

import (
	"fmt"
	"sort"
)

func sortEvenOdd(nums []int64) []int64 {
	var even, odd []int64
	for i, x := range nums {
		if i%2 == 0 {
			even = append(even, x)
		} else {
			odd = append(odd, x)
		}
	}
	sort.Slice(even, func(i, j int) bool { return even[i] < even[j] })
	sort.Slice(odd, func(i, j int) bool { return odd[i] > odd[j] })
	out := make([]int64, 0, len(nums))
	for i := range nums {
		if i%2 == 0 {
			out = append(out, even[i/2])
		} else {
			out = append(out, odd[i/2])
		}
	}
	return out
}

var seed int64 = 2164

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	lists := make([][]int64, 1000)
	for k := range lists {
		lists[k] = make([]int64, 100)
		for i := range lists[k] {
			lists[k][i] = nextRandom()%100 + 1
		}
	}
	var check int64
	for round := int64(0); round < 200; round++ {
		for k := int64(0); k < 1000; k++ {
			at := nextRandom() % 100
			lists[k][at] = nextRandom()%100 + 1
			cp := append([]int64(nil), lists[k]...)
			out := sortEvenOdd(cp)
			check = (check*31 + out[round%100] + out[(k*7)%100]) % 1000000007
		}
	}
	fmt.Printf("200000 solves: checksum %d\n", check)
}
