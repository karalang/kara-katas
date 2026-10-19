// LeetCode 768 — Max Chunks To Make Sorted II: benchmark, the ★ arm in Go.
// Sixty-four random arrays of 2,000 values, built once; 40,000 rounds
// each count the next one's chunks.
package main

import "fmt"

var seed int64 = 768

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func maxChunksToSorted(arr []int64) int64 {
	maxima := []int64{}
	for _, x := range arr {
		if len(maxima) > 0 && x < maxima[len(maxima)-1] {
			largest := maxima[len(maxima)-1]
			for len(maxima) > 0 && maxima[len(maxima)-1] > x {
				maxima = maxima[:len(maxima)-1]
			}
			maxima = append(maxima, largest)
		} else {
			maxima = append(maxima, x)
		}
	}
	return int64(len(maxima))
}

func main() {
	rounds := 40000
	pool := make([][]int64, 64)
	for p := range pool {
		noise := 1 + nextRandom()%40
		pool[p] = make([]int64, 2000)
		for i := range pool[p] {
			pool[p][i] = int64(i)*50 + nextRandom()%noise*50
		}
	}
	var total, check int64
	for round := 0; round < rounds; round++ {
		chunks := maxChunksToSorted(pool[round%64])
		total += chunks
		check = (check*31 + chunks) % 1000000007
	}
	fmt.Printf("%d arrays of 2000 values: %d chunks in all, checksum %d\n", rounds, total, check)
}
