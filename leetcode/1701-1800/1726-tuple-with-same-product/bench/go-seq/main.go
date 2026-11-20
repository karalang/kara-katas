// LeetCode #1726: Tuple with Same Product -- the bench (products.kara):
// every pair's product counted in a hash map, each new pair meeting the
// earlier pairs of its product, 8 tuples each.
package main

import "fmt"

func tupleSameProduct(nums []int32) int32 {
	counts := map[int32]int32{}
	var tuples int32
	for i := range nums {
		for j := i + 1; j < len(nums); j++ {
			p := nums[i] * nums[j]
			seen := counts[p]
			tuples += 8 * seen
			counts[p] = seen + 1
		}
	}
	return tuples
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	count := 20
	var rounds int64 = 3
	n := 1000
	top := 10000
	var seed int64 = 1726
	problems := make([][]int32, count)
	for c := range problems {
		pool := make([]int32, top)
		for i := range pool {
			pool[i] = int32(i + 1)
		}
		for i := 0; i < n; i++ {
			j := i + int(nextRandom(&seed)%int64(top-i))
			pool[i], pool[j] = pool[j], pool[i]
		}
		problems[c] = append([]int32(nil), pool[:n]...)
	}
	var sum, check int64
	for r := int64(0); r < rounds; r++ {
		for _, nums := range problems {
			answer := int64(tupleSameProduct(nums))
			sum += answer
			check = (check*31 + answer + r) % 1000000007
		}
	}
	fmt.Printf("%d problems of %d values up to %d, %d rounds: answers sum to %d, checksum %d\n", count, n, top, rounds, sum, check)
}
