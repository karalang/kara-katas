// LeetCode 808 — Soup Servings: the bench.
//
// Each round works out the answer for a size from 3750 to 4800 ml, 150
// to 192 servings, the largest the table is built for.
package main

import "fmt"

func soupServings(n int64) float64 {
	if n > 4800 {
		return 1.0
	}
	m := (n + 24) / 25
	p := make([][]float64, m+1)
	for a := range p {
		p[a] = make([]float64, m+1)
	}
	pour := [4][2]int64{{4, 0}, {3, 1}, {2, 2}, {1, 3}}
	for a := int64(0); a <= m; a++ {
		for b := int64(0); b <= m; b++ {
			if a == 0 && b == 0 {
				p[a][b] = 0.5
			} else if a == 0 {
				p[a][b] = 1.0
			} else if b == 0 {
				p[a][b] = 0.0
			} else {
				sum := 0.0
				for _, d := range pour {
					sum += p[max(a-d[0], 0)][max(b-d[1], 0)]
				}
				p[a][b] = 0.25 * sum
			}
		}
	}
	return p[m][m]
}

func main() {
	rounds := int64(30000)
	total := 0.0
	sure := 0
	for r := int64(0); r < rounds; r++ {
		n := 3750 + (r*37)%1051
		p := soupServings(n)
		total += p
		if p > 0.99999 {
			sure++
		}
	}
	fmt.Printf("%d rounds of 3750 to 4800 ml: sum %.6f, %d above 0.99999\n", rounds, total, sure)
}
