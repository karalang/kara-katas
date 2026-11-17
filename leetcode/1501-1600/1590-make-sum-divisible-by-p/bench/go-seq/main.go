// LeetCode #1590: Make Sum Divisible by P -- the bench in Go, mirroring
// divisible.kara: the latest prefix with each remainder in a map.
package main

import "fmt"

func minSubarray(nums []int32, p32 int32) int32 {
	p := int64(p32)
	var sum int64
	for _, v := range nums {
		sum += int64(v)
	}
	need := sum % p
	if need == 0 {
		return 0
	}
	last := map[int64]int64{0: -1}
	var prefix int64
	n := int64(len(nums))
	best := n
	for j, v := range nums {
		prefix = (prefix + int64(v)) % p
		if i, ok := last[(prefix-need+p)%p]; ok && int64(j)-i < best {
			best = int64(j) - i
		}
		last[prefix] = int64(j)
	}
	if best == n {
		return -1
	}
	return int32(best)
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func wide(seed *int64) int64 {
	a := nextRandom(seed)
	return a*32768 + nextRandom(seed)
}

func main() {
	seed := int64(1590)
	var all [][]int32
	var ps []int32
	for k := 0; k < 40; k++ {
		nums := make([]int32, 100000)
		for i := range nums {
			nums[i] = int32(wide(&seed)%1000000000 + 1)
		}
		all = append(all, nums)
		ps = append(ps, int32(wide(&seed)%100000+1))
	}
	var check, total int64
	for k := range all {
		answer := int64(minSubarray(all[k], ps[k]))
		total += answer
		check = (check*31 + answer + 1) % 1000000007
	}
	fmt.Printf("40 problems of 100000 values: lengths %d, checksum %d\n", total, check)
}
