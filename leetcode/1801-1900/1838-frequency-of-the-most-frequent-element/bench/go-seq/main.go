// LeetCode #1838: Frequency of the Most Frequent Element -- the bench in Go: the ★ arm over
// 200 calls on the first 50000 to 99999 of one list of 10^5 numbers from 1
// to 10^5, built once, with `k` from 1 to 10^5, each run's length and `k`
// drawn from the checksum so far. Each call copies its run, and the arm
// sorts a copy of its own.
package main

import (
	"fmt"
	"slices"
)

func maxFrequency(nums []int64, k int64) int64 {
	sorted := slices.Clone(nums)
	slices.Sort(sorted)
	var best, first, sum int64
	for last := int64(0); last < int64(len(sorted)); last++ {
		sum += sorted[last]
		for sorted[last]*(last-first+1)-sum > k {
			sum -= sorted[first]
			first++
		}
		best = max(best, last-first+1)
	}
	return best
}

func main() {
	seed := int64(1838)
	nextRandom := func() int64 {
		seed = (seed*1103515245 + 12345) % 2147483648
		return seed / 65536
	}
	base := make([]int64, 0, 100000)
	for i := 0; i < 100000; i++ {
		hi := nextRandom()
		base = append(base, 1+(hi*32768+nextRandom())%100000)
	}
	var check int64
	for call := int64(0); call < 200; call++ {
		n := 50000 + (check+call)%50000
		k := 1 + (check*7+call)%100000
		run := slices.Clone(base[:n])
		check = (check*31 + maxFrequency(run, k)) % 1000000007
	}
	fmt.Printf("200 calls: checksum %d\n", check)
}
