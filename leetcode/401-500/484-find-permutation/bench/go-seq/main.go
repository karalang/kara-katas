// Benchmark for #484: Go mirror of the ★ arm (1 to n, each run of Ds
// reversed); see ../find_permutation.kara.
package main

import (
	"fmt"
	"strings"
)

func findPermutation(s string) []int64 {
	letters := []rune(s)
	n := len(letters) + 1
	perm := make([]int64, n)
	for i := range perm {
		perm[i] = int64(i + 1)
	}
	i := 0
	for i < len(letters) {
		if letters[i] == 'D' {
			start := i
			for i < len(letters) && letters[i] == 'D' {
				i++
			}
			for low, high := start, i; low < high; low, high = low+1, high-1 {
				perm[low], perm[high] = perm[high], perm[low]
			}
		} else {
			i++
		}
	}
	return perm
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	patterns := []string{}
	var seed int64 = 484
	for p := int64(0); p < 20; p++ {
		var sb strings.Builder
		for j := 0; j < 100000; j++ {
			if nextRandom(&seed)%20 < p {
				sb.WriteByte('D')
			} else {
				sb.WriteByte('I')
			}
		}
		patterns = append(patterns, sb.String())
	}
	var total, checksum int64
	for r := 0; r < 10; r++ {
		for _, s := range patterns {
			perm := findPermutation(s)
			n := len(perm)
			total += int64(n)
			checksum = (checksum*31 + perm[0] + perm[n/2]*7 + perm[n-1]*13) % 1000000007
		}
	}
	fmt.Printf("200 solves of 100000 letters: %d numbers, checksum %d\n", total, checksum)
}
