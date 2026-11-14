// LeetCode #2125: Number of Laser Beams in a Bank -- the benchmark, the
// same algorithm as beams.kara.
package main

import (
	"fmt"
	"strings"
)

func numberOfBeams(bank []string) int64 {
	var prev, beams int64
	for _, row := range bank {
		devices := int64(strings.Count(row, "1"))
		if devices > 0 {
			beams += prev * devices
			prev = devices
		}
	}
	return beams
}

var seed int64 = 2125

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	banks := make([][]string, 12)
	for b := 0; b < 12; b++ {
		bank := make([]string, 500)
		for r := range bank {
			cells := make([]byte, 500)
			for c := range cells {
				if nextRandom()%4 < int64(b%3+1) {
					cells[c] = '1'
				} else {
					cells[c] = '0'
				}
			}
			bank[r] = string(cells)
		}
		banks[b] = bank
	}
	var total, check int64
	for round := int64(0); round < 500; round++ {
		for b := 0; b < 12; b++ {
			r := nextRandom() % 500
			c := nextRandom() % 500
			cells := []byte(banks[b][r])
			if cells[c] == '1' {
				cells[c] = '0'
			} else {
				cells[c] = '1'
			}
			banks[b][r] = string(cells)
			beams := numberOfBeams(banks[b])
			total += beams
			check = (check*31 + beams + round) % 1000000007
		}
	}
	fmt.Printf("6000 solves: %d beams, checksum %d\n", total, check)
}
