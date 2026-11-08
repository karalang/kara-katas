// LeetCode #1072: Flip Columns For Maximum Number of Equal Rows -- the
// benchmark's Go mirror of equal_rows.kara: the same count of row patterns
// in a map keyed by string over 200 matrices built once, each answered 30
// times.
package main

import "fmt"

func maxEqualRows(matrix [][]int64) int64 {
	counts := map[string]int64{}
	var best int64
	for _, row := range matrix {
		key := make([]byte, 0, len(row))
		for _, c := range row {
			if c != row[0] {
				key = append(key, '1')
			} else {
				key = append(key, '0')
			}
		}
		k := string(key)
		seen := counts[k] + 1
		counts[k] = seen
		if seen > best {
			best = seen
		}
	}
	return best
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func randomBits(n int64, seed *int64) []int64 {
	bits := make([]int64, 0, n)
	for i := int64(0); i < n; i++ {
		bits = append(bits, nextRandom(seed)%2)
	}
	return bits
}

func randomMatrix(rows, cols int64, seed *int64) [][]int64 {
	m := nextRandom(seed)%rows + 1
	n := nextRandom(seed)%cols + 1
	var patterns [][]int64
	count := nextRandom(seed)%3 + 1
	for p := int64(0); p < count; p++ {
		patterns = append(patterns, randomBits(n, seed))
	}
	var matrix [][]int64
	for i := int64(0); i < m; i++ {
		roll := nextRandom(seed) % 8
		if roll < 2 {
			matrix = append(matrix, randomBits(n, seed))
		} else {
			p := patterns[nextRandom(seed)%int64(len(patterns))]
			row := make([]int64, n)
			for j := range p {
				if roll < 5 {
					row[j] = 1 - p[j]
				} else {
					row[j] = p[j]
				}
			}
			matrix = append(matrix, row)
		}
	}
	return matrix
}

func main() {
	seed := int64(1072)
	matrices := make([][][]int64, 0, 200)
	for i := 0; i < 200; i++ {
		matrices = append(matrices, randomMatrix(300, 300, &seed))
	}
	var total, check int64
	for r := 0; r < 30; r++ {
		for _, matrix := range matrices {
			x := maxEqualRows(matrix)
			total += x
			check = (check*31 + x) % 1000000007
		}
	}
	fmt.Printf("6000 calls: answers sum %d, checksum %d\n", total, check)
}
