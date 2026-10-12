// Benchmark for #454: mirror of four_sum.kara (the ★ arm, pair sums of
// the first two arrays counted in a map) on the same workload.
package main

import "fmt"

func fourSumCount(nums1, nums2, nums3, nums4 []int64) int64 {
	sums := make(map[int64]int64)
	for _, a := range nums1 {
		for _, b := range nums2 {
			sums[a+b]++
		}
	}
	var count int64
	for _, c := range nums3 {
		for _, d := range nums4 {
			count += sums[-(c + d)]
		}
	}
	return count
}

// ---- benchmark --------------------------------------------------------

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func randomValue(seed *int64) int64 {
	hi := nextRandom(seed)
	lo := nextRandom(seed)
	return (hi*65536+lo)%100001 - 50000
}

func main() {
	const n = 1000
	const rounds = 10
	var seed int64 = 454
	arrays := make([][]int64, 0, 4)
	for a := 0; a < 4; a++ {
		nums := make([]int64, 0)
		for i := 0; i < n; i++ {
			nums = append(nums, randomValue(&seed))
		}
		arrays = append(arrays, nums)
	}
	var total, checksum int64
	for r := 0; r < rounds; r++ {
		for a := 0; a < 4; a++ {
			at := nextRandom(&seed) % n
			arrays[a][at] = randomValue(&seed)
		}
		tuples := fourSumCount(arrays[0], arrays[1], arrays[2], arrays[3])
		total += tuples
		checksum = (checksum*31 + tuples) % 1000000007
	}
	fmt.Printf("%d rounds on 4 arrays of %d: %d tuples, checksum %d\n", rounds, n, total, checksum)
}
