// Benchmark for #448: mirror of find_disappeared.kara (marking by sign)
// on one random array of 1,000,000 numbers with 300,000 missing, built
// once, copied and searched 20 times over.
package main

import "fmt"

func findDisappearedNumbers(nums []int64) []int64 {
	for i := range nums {
		x := nums[i]
		if x < 0 {
			x = -x
		}
		if nums[x-1] > 0 {
			nums[x-1] = -nums[x-1]
		}
	}
	missing := []int64{}
	for i := range nums {
		if nums[i] > 0 {
			missing = append(missing, int64(i)+1)
		}
	}
	return missing
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func randomIndex(seed *int64, below int64) int64 {
	a := nextRandom(seed)
	return (a*32768 + nextRandom(seed)) % below
}

func main() {
	const n, d, rounds = 1000000, 300000, 20
	seed := int64(448)
	// The first d of a shuffled 1..n twice, the next n - 2d once.
	values := make([]int64, n)
	for x := int64(1); x <= n; x++ {
		values[x-1] = x
	}
	for i := int64(0); i < n; i++ {
		j := i + randomIndex(&seed, n-i)
		values[i], values[j] = values[j], values[i]
	}
	nums := []int64{}
	nums = append(nums, values[:n-d]...)
	nums = append(nums, values[:d]...)
	for i := int64(0); i < n; i++ {
		j := i + randomIndex(&seed, n-i)
		nums[i], nums[j] = nums[j], nums[i]
	}
	found := 0
	checksum := int64(0)
	for round := int64(0); round < rounds; round++ {
		missing := findDisappearedNumbers(append([]int64(nil), nums...))
		found += len(missing)
		for _, x := range missing {
			checksum = (checksum*31 + x + round) % 1000000007
		}
	}
	fmt.Printf("%d rounds on %d numbers: %d missing, checksum %d\n", rounds, n, found, checksum)
}
