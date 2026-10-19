// LeetCode 799 — Champagne Tower: the bench, in Go. Mirrors
// champagne_tower.kara: one row at a time.
package main

import "fmt"

func champagneTower(poured, queryRow, queryGlass int64) float64 {
	row := []float64{float64(poured)}
	for r := int64(0); r < queryRow; r++ {
		below := make([]float64, r+2)
		for c := int64(0); c < r+1; c++ {
			if row[c] > 1.0 {
				half := (row[c] - 1.0) / 2.0
				below[c] += half
				below[c+1] += half
			}
		}
		row = below
	}
	got := row[queryGlass]
	if got > 1.0 {
		return 1.0
	}
	return got
}

var seed int64 = 799

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	type question struct{ poured, row, glass int64 }
	questions := make([]question, 0, 4096)
	for i := 0; i < 4096; i++ {
		hi := nextRandom()
		poured := (hi*32768 + nextRandom()) % 1000000001
		row := 50 + nextRandom()%50
		glass := nextRandom() % (row + 1)
		questions = append(questions, question{poured, row, glass})
	}
	var rounds int64 = 81920
	total := 0.0
	var check int64
	for r := int64(0); r < rounds; r++ {
		q := questions[r%4096]
		got := champagneTower(q.poured, q.row, q.glass)
		total += got
		check = (check*31 + int64(got*1000000.0)) % 1000000007
	}
	fmt.Printf("%d glasses: %.5f cups in all, checksum %d\n", rounds, total, check)
}
