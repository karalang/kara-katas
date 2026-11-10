// LeetCode #2103: Rings and Rods -- bench, Go mirror of rings.kara.
package main

import "fmt"

func countPoints(rings string) int64 {
	var masks [10]int64
	for i := 0; i < len(rings); i += 2 {
		var bit int64
		switch rings[i] {
		case 'R':
			bit = 1
		case 'G':
			bit = 2
		default:
			bit = 4
		}
		masks[rings[i+1]-'0'] |= bit
	}
	var full int64
	for _, m := range masks {
		if m == 7 {
			full++
		}
	}
	return full
}

var seed int64 = 2103

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	strings := make([]string, 0, 4096)
	for s := 0; s < 4096; s++ {
		rods := int64(10)
		if s%2 != 0 {
			rods = 3
		}
		b := make([]byte, 200)
		for r := 0; r < 100; r++ {
			b[2*r] = "RGB"[nextRandom()%3]
			b[2*r+1] = byte('0' + nextRandom()%rods)
		}
		strings = append(strings, string(b))
	}
	var total, check int64
	for k := 0; k < 300000; k++ {
		got := countPoints(strings[k*7919%4096])
		total += got
		check = (check*31 + got) % 1000000007
	}
	fmt.Printf("300000 counts: %d rods with all three, checksum %d\n", total, check)
}
