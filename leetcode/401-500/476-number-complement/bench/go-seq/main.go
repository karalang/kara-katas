// Benchmark for #476: Go mirror of the ★ arm (a mask of the number's own
// width); see ../number_complement.kara.
package main

import "fmt"

func findComplement(num int64) int64 {
	var mask int64 = 1
	for mask < num {
		mask = (mask << 1) | 1
	}
	return num ^ mask
}

var seed int64 = 476

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	count := 30000000
	var total, checksum int64
	for i := 0; i < count; i++ {
		bits := 1 + nextRandom()%31
		high := int64(1) << (bits - 1)
		a := nextRandom()
		b := nextRandom()
		num := high | ((a*32768 + b) % high)
		got := findComplement(num)
		total += got
		checksum = (checksum*31 + got) % 1000000007
	}
	fmt.Printf("%d numbers: complements add up to %d, checksum %d\n", count, total, checksum)
}
