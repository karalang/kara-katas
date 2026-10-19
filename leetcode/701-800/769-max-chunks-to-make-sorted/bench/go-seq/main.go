// LeetCode 769 — Max Chunks To Make Sorted: benchmark, the ★ arm in Go.
// Sixty-four near-sorted permutations of 2,000, built once; 150,000
// rounds each count the next one's chunks.
package main

import "fmt"

var seed int64 = 769

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func maxChunksToSorted(arr []int64) int64 {
	var chunks, largest int64
	for i, x := range arr {
		if x > largest {
			largest = x
		}
		if largest == int64(i) {
			chunks++
		}
	}
	return chunks
}

func main() {
	const n = 2000
	rounds := 150000
	pool := make([][]int64, 64)
	for p := range pool {
		arr := make([]int64, n)
		for i := range arr {
			arr[i] = int64(i)
		}
		swaps := nextRandom() % n
		for s := int64(0); s < swaps; s++ {
			i := nextRandom() % n
			j := i + 1 + nextRandom()%4
			if j > n-1 {
				j = n - 1
			}
			arr[i], arr[j] = arr[j], arr[i]
		}
		pool[p] = arr
	}
	var total, check int64
	for round := 0; round < rounds; round++ {
		chunks := maxChunksToSorted(pool[round%64])
		total += chunks
		check = (check*31 + chunks) % 1000000007
	}
	fmt.Printf("%d permutations of 2000: %d chunks in all, checksum %d\n", rounds, total, check)
}
