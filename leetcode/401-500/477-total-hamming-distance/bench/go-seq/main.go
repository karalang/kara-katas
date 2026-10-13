// Benchmark for #477: Go mirror of the ★ arm (one bit at a time); see
// ../total_hamming_distance.kara.
package main

import "fmt"

func totalHammingDistance(nums []int64) int64 {
	n := int64(len(nums))
	var total int64
	for bit := 0; bit < 30; bit++ {
		var ones int64
		for _, x := range nums {
			ones += (x >> bit) & 1
		}
		total += ones * (n - ones)
	}
	return total
}

var seed int64 = 477

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	n := 10000
	rounds := 5000
	nums := make([]int64, 0, n)
	for i := 0; i < n; i++ {
		a := nextRandom()
		b := nextRandom()
		nums = append(nums, (a*32768+b)%1000000001)
	}
	var total, checksum int64
	for r := 0; r < rounds; r++ {
		a := nextRandom()
		b := nextRandom()
		nums[r%n] = (a*32768 + b) % 1000000001
		got := totalHammingDistance(nums)
		total += got
		checksum = (checksum*31 + got) % 1000000007
	}
	fmt.Printf("%d rounds on %d numbers: distances add up to %d, checksum %d\n", rounds, n, total, checksum)
}
