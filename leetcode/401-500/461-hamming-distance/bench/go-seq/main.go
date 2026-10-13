// Benchmark for #461: mirror of hamming_distance.kara (the ★ arm, clearing
// the lowest set bit) on the same workload.
package main

import "fmt"

func hammingDistance(x, y int64) int64 {
	z := x ^ y
	count := int64(0)
	for z != 0 {
		z &= z - 1
		count++
	}
	return count
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func random31(seed *int64) int64 {
	a := nextRandom(seed)
	b := nextRandom(seed)
	c := nextRandom(seed)
	return ((a*32768+b)*2 + c%2) % 2147483648
}

func main() {
	const n int64 = 1000000
	const rounds = 20
	seed := int64(461)
	nums := make([]int64, 0, n)
	for i := int64(0); i < n; i++ {
		nums = append(nums, random31(&seed))
	}
	total := int64(0)
	checksum := int64(0)
	for r := 0; r < rounds; r++ {
		hi := nextRandom(&seed)
		lo := nextRandom(&seed)
		k := (hi*65536 + lo) % n
		nums[k] = random31(&seed)
		sum := int64(0)
		for i := int64(1); i < n; i++ {
			sum += hammingDistance(nums[i-1], nums[i])
		}
		total += sum
		checksum = (checksum*31 + sum) % 1000000007
	}
	fmt.Printf("%d rounds on %d numbers: total distance %d, checksum %d\n", rounds, n, total, checksum)
}
