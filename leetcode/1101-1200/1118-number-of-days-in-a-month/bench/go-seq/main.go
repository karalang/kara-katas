// LeetCode #1118: Number of Days in a Month -- the bench in Go, the ★
// arm's `switch` over the same 10^6 months and 40 rounds.
package main

import "fmt"

func isLeap(year int32) bool {
	return year%4 == 0 && year%100 != 0 || year%400 == 0
}

func numberOfDays(year, month int32) int32 {
	switch month {
	case 2:
		if isLeap(year) {
			return 29
		}
		return 28
	case 4, 6, 9, 11:
		return 30
	default:
		return 31
	}
}

var seed int64 = 1118

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	years := make([]int32, 0, 1000000)
	months := make([]int32, 0, 1000000)
	for i := 0; i < 1000000; i++ {
		years = append(years, int32(1583+nextRandom()%517))
		months = append(months, int32(1+nextRandom()%12))
	}
	var total, check int64
	var last int32
	for round := 0; round < 40; round++ {
		for i := range years {
			d := numberOfDays(years[i]+(last&1), months[i])
			total += int64(d)
			if i%64 == 0 {
				check = (check*31 + int64(d)) % 1000000007
			}
			last = d
		}
	}
	fmt.Printf("40 rounds over 10^6 months: %d days, checksum %d\n", total, check)
}
