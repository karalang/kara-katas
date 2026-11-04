// LeetCode #1043: Partition Array for Maximum Sum -- bench, Go mirror of
// partition_max.kara (the bottom-up table).
package main

import "fmt"

func maxSumAfterPartitioning(arr []int64, k int64) int64 {
	n := int64(len(arr))
	best := make([]int64, n+1)
	for i := int64(1); i <= n; i++ {
		largest := int64(0)
		for j := int64(1); j <= k && j <= i; j++ {
			if arr[i-j] > largest {
				largest = arr[i-j]
			}
			if offer := best[i-j] + largest*j; offer > best[i] {
				best[i] = offer
			}
		}
	}
	return best[n]
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	const count, n, rounds = 400, 500, 40
	seed := int64(1043)
	arrays := make([][]int64, 0, count)
	ks := make([]int64, 0, count)
	for a := 0; a < count; a++ {
		arr := make([]int64, 0, n)
		for i := 0; i < n; i++ {
			hi := nextRandom(&seed)
			lo := nextRandom(&seed)
			arr = append(arr, (hi*32768+lo)%1000000001)
		}
		arrays = append(arrays, arr)
		ks = append(ks, nextRandom(&seed)%50+1)
	}
	var total, check int64
	for r := 0; r < rounds; r++ {
		for a := 0; a < count; a++ {
			answer := maxSumAfterPartitioning(arrays[a], ks[a])
			total += answer
			check = (check*131 + answer%1000000007) % 1000000007
		}
	}
	fmt.Printf("%d arrays of %d values, %d rounds: total %d, checksum %d\n", count, n, rounds, total, check)
}
