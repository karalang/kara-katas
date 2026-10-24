// LeetCode #957: Prison Cells After N Days -- Go mirror of the Kara bench
// program (a day per state seen).
package main

import "fmt"

func nextDay(cells []int64) []int64 {
	out := make([]int64, 8)
	for i := 1; i < 7; i++ {
		if cells[i-1] == cells[i+1] {
			out[i] = 1
		}
	}
	return out
}

func code(cells []int64) int64 {
	c := int64(0)
	for _, v := range cells {
		c = c*2 + v
	}
	return c
}

func prisonAfterNDays(cells []int64, n int64) []int64 {
	seen := map[int64]int64{}
	row := cells
	day := int64(0)
	left := n
	for left > 0 {
		if first, ok := seen[code(row)]; ok {
			left %= day - first
			seen = map[int64]int64{}
			if left == 0 {
				break
			}
		}
		seen[code(row)] = day
		row = nextDay(row)
		day++
		left--
	}
	return row
}

func main() {
	rounds := int64(2000)
	rows := make([][]int64, 256)
	for b := int64(0); b < 256; b++ {
		rows[b] = make([]int64, 8)
		for i := int64(0); i < 8; i++ {
			rows[b][i] = (b >> (7 - i)) & 1
		}
	}
	total, check := int64(0), int64(0)
	for r := int64(0); r < rounds; r++ {
		for b := 0; b < 256; b++ {
			cells := make([]int64, 8)
			copy(cells, rows[b])
			c := code(prisonAfterNDays(cells, 1000000000-r))
			total += c
			check = (check*31 + c) % 1000000007
		}
	}
	fmt.Printf("%d rounds over all 256 rows: rows adding to %d, checksum %d\n", rounds, total, check)
}
