// LeetCode #1738: Find Kth Largest XOR Coordinate Value -- the bench
// (kth.kara): a prefix XOR table, then a sort.
package main

import (
	"fmt"
	"slices"
)

func kthLargestValue(matrix [][]int32, k int32) int32 {
	m, n := len(matrix), len(matrix[0])
	prefix := make([][]int32, m+1)
	for i := range prefix {
		prefix[i] = make([]int32, n+1)
	}
	values := make([]int32, 0, m*n)
	for i := 0; i < m; i++ {
		for j := 0; j < n; j++ {
			prefix[i+1][j+1] = prefix[i][j+1] ^ prefix[i+1][j] ^ prefix[i][j] ^ matrix[i][j]
			values = append(values, prefix[i+1][j+1])
		}
	}
	slices.Sort(values)
	return values[len(values)-int(k)]
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func wide(seed *int64) int64 {
	hi := nextRandom(seed)
	return hi*32768 + nextRandom(seed)
}

func main() {
	count := 4
	var rounds int64 = 5
	var side int64 = 1000
	var seed int64 = 1738
	matrices := make([][][]int32, 0, count)
	ks := make([]int32, 0, count)
	for p := 0; p < count; p++ {
		matrix := make([][]int32, 0, side)
		for i := int64(0); i < side; i++ {
			row := make([]int32, side)
			for j := range row {
				row[j] = int32(wide(&seed) % 1000001)
			}
			matrix = append(matrix, row)
		}
		matrices = append(matrices, matrix)
		ks = append(ks, int32(wide(&seed)%(side*side)+1))
	}
	var sum, check int64
	for r := int64(0); r < rounds; r++ {
		for p := 0; p < count; p++ {
			answer := int64(kthLargestValue(matrices[p], ks[p]))
			sum += answer
			check = (check*31 + answer + int64(ks[p]) + r) % 1000000007
		}
	}
	fmt.Printf("%d matrices of %d by %d, %d rounds: answers sum to %d, checksum %d\n", count, side, side, rounds, sum, check)
}
