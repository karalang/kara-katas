package main

import "fmt"

func countCombos(start, k, remaining, dPool int64) int64 {
	if k == 0 {
		if remaining == 0 {
			return 1
		}
		return 0
	}
	var total int64 = 0
	for d := start; d <= dPool; d++ {
		if d > remaining {
			return total
		}
		total += countCombos(d+1, k-1, remaining-d, dPool)
	}
	return total
}

func main() {
	var dPool, kmax, nmax int64 = 36, 6, 150
	var sink int64 = 0
	for k := int64(1); k <= kmax; k++ {
		for n := int64(1); n <= nmax; n++ {
			sink += countCombos(1, k, n, dPool)
		}
	}
	fmt.Println(sink)
}
