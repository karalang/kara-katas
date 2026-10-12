// Benchmark for #400: mirror of nth_digit.kara (skip whole blocks).
package main

import "fmt"

func findNthDigit(n int64) int64 {
	rest, digits, count, start := n, int64(1), int64(9), int64(1)
	for rest > digits*count {
		rest -= digits * count
		digits++
		count *= 10
		start *= 10
	}
	number := start + (rest-1)/digits
	shift := digits - 1 - (rest-1)%digits
	x := number
	for shift > 0 {
		x = x / 10
		shift--
	}
	return x % 10
}

var seed int64 = 4001

func step() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	calls := 10000000
	var total, checksum int64
	for c := 0; c < calls; c++ {
		hi := step()
		n := 1 + (hi*32768+step())%2147483647
		d := findNthDigit(n)
		total += d
		checksum = (checksum*31 + d) % 1000000007
	}
	fmt.Printf("%d calls: total %d, checksum %d\n", calls, total, checksum)
}
