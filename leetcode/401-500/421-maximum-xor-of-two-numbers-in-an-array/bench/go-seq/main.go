// Benchmark for #421: mirror of maximum_xor.kara (prefix bits), with a
// Go map as the set.
package main

import (
	"fmt"
	"os"
	"strconv"
)

func findMaximumXor(nums []int64) int64 {
	var answer, mask int64
	for bit := 30; bit >= 0; bit-- {
		mask |= 1 << bit
		prefixes := make(map[int64]struct{})
		for _, x := range nums {
			prefixes[x&mask] = struct{}{}
		}
		candidate := answer | 1<<bit
		for p := range prefixes {
			if _, ok := prefixes[p^candidate]; ok {
				answer = candidate
				break
			}
		}
	}
	return answer
}

func step(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func random31(seed *int64) int64 {
	high := step(seed)
	low := step(seed)
	bit := step(seed) % 2
	return high*65536 + low*2 + bit
}

func main() {
	rounds := int64(100)
	if len(os.Args) > 1 {
		rounds, _ = strconv.ParseInt(os.Args[1], 10, 64)
	}
	n := int64(20000)
	seed := int64(421)
	nums := make([]int64, n)
	for i := range nums {
		nums[i] = random31(&seed)
	}
	var total, checksum int64
	for r := int64(0); r < rounds; r++ {
		nums[r*7919%n] = random31(&seed)
		answer := findMaximumXor(nums)
		total += answer
		checksum = (checksum*31 + answer) % 1000000007
	}
	fmt.Printf("%d rounds on %d numbers: total %d, checksum %d\n", rounds, n, total, checksum)
}
