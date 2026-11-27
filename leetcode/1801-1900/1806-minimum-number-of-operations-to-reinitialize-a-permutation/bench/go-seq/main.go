// LeetCode #1806: Minimum Number of Operations to Reinitialize a
// Permutation -- the bench in Go: the ★ arm over 3000 calls, each n an even
// number to 1000 drawn from the checksum so far.
package main

import (
	"fmt"
	"slices"
)

func reinitializePermutation(n int32) int32 {
	size := int64(n)
	start := make([]int64, size)
	for i := range start {
		start[i] = int64(i)
	}
	perm := slices.Clone(start)
	var ops int32
	for {
		arr := make([]int64, size)
		for i := int64(0); i < size; i++ {
			if i%2 == 0 {
				arr[i] = perm[i/2]
			} else {
				arr[i] = perm[size/2+(i-1)/2]
			}
		}
		perm = arr
		ops++
		if slices.Equal(perm, start) {
			return ops
		}
	}
}

func main() {
	var check int64
	for call := int64(0); call < 3000; call++ {
		n := 2 * (1 + (check+call)%500)
		check = (check*31 + int64(reinitializePermutation(int32(n)))) % 1000000007
	}
	fmt.Printf("3000 calls of even n to 1000: checksum %d\n", check)
}
