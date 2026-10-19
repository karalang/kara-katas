// Benchmark for #775: Global and Local Inversions -- the ★ arm (every
// value at most one place from its index), as the Kāra program does it.
package main

import "fmt"

func isIdealPermutation(nums []int64) bool {
	for i := range nums {
		d := nums[i] - int64(i)
		if d > 1 || d < -1 {
			return false
		}
	}
	return true
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	const count = 64
	const n = 100000
	seed := int64(775)
	perms := make([][]int64, 0, count)
	for g := 0; g < count; g++ {
		nums := make([]int64, n)
		for v := range nums {
			nums[v] = int64(v)
		}
		i := 0
		for i+1 < n {
			if nextRandom(&seed)%2 == 0 {
				nums[i], nums[i+1] = nums[i+1], nums[i]
				i += 2
			} else {
				i++
			}
		}
		if g%4 == 1 {
			at := n - 4 - int(nextRandom(&seed)%1000)
			nums[at], nums[at+3] = nums[at+3], nums[at]
		} else if g%4 == 2 {
			at := int(nextRandom(&seed) % (n - 3))
			nums[at], nums[at+3] = nums[at+3], nums[at]
		}
		perms = append(perms, nums)
	}
	ideals := 0
	checksum := int64(0)
	for round := 0; round < 12000; round++ {
		g := (round * 7) % count
		if isIdealPermutation(perms[g]) {
			ideals++
			checksum = (checksum*31 + int64(g) + 1) % 1000000007
		} else {
			checksum = (checksum*31 + 7) % 1000000007
		}
	}
	fmt.Printf("12000 rounds of %d values: %d ideal, checksum %d\n", n, ideals, checksum)
}
