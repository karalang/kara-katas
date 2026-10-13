// Benchmark for #526: Go mirror of the ★ arm (place positions from the
// front); see ../count_arrangement.kara.
package main

import "fmt"

func place(n, pos int64, used []bool) int64 {
	if pos > n {
		return 1
	}
	count := int64(0)
	for x := int64(1); x <= n; x++ {
		if !used[x] && (x%pos == 0 || pos%x == 0) {
			used[x] = true
			count += place(n, pos+1, used)
			used[x] = false
		}
	}
	return count
}

func countArrangement(n int64) int64 {
	return place(n, 1, make([]bool, n+1))
}

func main() {
	total, checksum := int64(0), int64(0)
	for round := int64(0); round < 20; round++ {
		for n := int64(1); n <= 15; n++ {
			count := countArrangement(n)
			total += count
			checksum = (checksum*31 + count + round) % 1000000007
		}
	}
	fmt.Printf("n from 1 to 15, 20 rounds: total %d, checksum %d\n", total, checksum)
}
