// Benchmark for #547: Go mirror of the ★ arm (depth-first search); see
// ../number_of_provinces.kara.
package main

import "fmt"

func visit(m [][]int64, city int, seen []bool) {
	seen[city] = true
	for other := 0; other < len(m); other++ {
		if m[city][other] == 1 && !seen[other] {
			visit(m, other, seen)
		}
	}
}

func findCircleNum(m [][]int64) int64 {
	n := len(m)
	seen := make([]bool, n)
	var provinces int64
	for city := 0; city < n; city++ {
		if !seen[city] {
			provinces++
			visit(m, city, seen)
		}
	}
	return provinces
}

var seed int64 = 547

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	count, n := 30, 200
	all := make([][][]int64, count)
	for g := 0; g < count; g++ {
		m := make([][]int64, n)
		for i := range m {
			m[i] = make([]int64, n)
			m[i][i] = 1
		}
		for i := 0; i < n; i++ {
			for j := i + 1; j < n; j++ {
				if nextRandom()%1000 < int64(1+g%10) {
					m[i][j] = 1
					m[j][i] = 1
				}
			}
		}
		all[g] = m
	}
	var total, checksum int64
	for round := 0; round < 200; round++ {
		for g := 0; g < count; g++ {
			a, b := (round*13+g)%n, (round*29+g*3+1)%n
			if a != b {
				flip := 1 - all[g][a][b]
				all[g][a][b] = flip
				all[g][b][a] = flip
			}
			p := findCircleNum(all[g])
			total += p
			checksum = (checksum*31 + p) % 1000000007
		}
	}
	fmt.Printf("%d matrices, 200 rounds each: %d provinces, checksum %d\n", count, total, checksum)
}
