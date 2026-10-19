// LeetCode 765 — Couples Holding Hands: benchmark, the ★ arm in Go.
// 1,000,000 random rows of 60 seats.
package main

import "fmt"

func minSwapsCouples(row []int64) int64 {
	seatOf := make([]int64, len(row))
	for i, person := range row {
		seatOf[person] = int64(i)
	}
	var swaps int64
	for i := 0; i < len(row); i += 2 {
		partner := row[i] ^ 1
		if row[i+1] != partner {
			j := seatOf[partner]
			moved := row[i+1]
			row[j] = moved
			seatOf[moved] = j
			row[i+1] = partner
			seatOf[partner] = int64(i + 1)
			swaps++
		}
	}
	return swaps
}

var seed int64 = 765

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	rounds := 1000000
	var total, check int64
	for r := 0; r < rounds; r++ {
		row := make([]int64, 60)
		for p := range row {
			row[p] = int64(p)
		}
		for i := 0; i < 60; i++ {
			j := i + int(nextRandom()%int64(60-i))
			row[i], row[j] = row[j], row[i]
		}
		swaps := minSwapsCouples(row)
		total += swaps
		check = (check*31 + swaps) % 1000000007
	}
	fmt.Printf("%d rows of 60 seats: %d swaps in all, checksum %d\n", rounds, total, check)
}
