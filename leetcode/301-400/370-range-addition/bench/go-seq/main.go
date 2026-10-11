// Benchmark for #370 -- mirror of range_addition.kara.
package main

import "fmt"

type update struct{ start, end, inc int64 }

func getModifiedArray(length int64, updates []update) []int64 {
	diff := make([]int64, length+1)
	for _, u := range updates {
		diff[u.start] += u.inc
		diff[u.end+1] -= u.inc
	}
	out := make([]int64, length)
	var running int64
	for i := int64(0); i < length; i++ {
		running += diff[i]
		out[i] = running
	}
	return out
}

func main() {
	var seed int64 = 370
	var checksum int64
	for r := 0; r < 50; r++ {
		updates := make([]update, 0, 10000)
		for j := 0; j < 10000; j++ {
			seed = (seed*1103515245 + 12345) % 2147483648
			high := seed / 65536
			seed = (seed*1103515245 + 12345) % 2147483648
			a := (high*32768 + seed/65536) % 100000
			seed = (seed*1103515245 + 12345) % 2147483648
			high2 := seed / 65536
			seed = (seed*1103515245 + 12345) % 2147483648
			b := (high2*32768 + seed/65536) % 100000
			seed = (seed*1103515245 + 12345) % 2147483648
			inc := (seed/65536)%2001 - 1000
			lo, hi := a, b
			if b < a {
				lo, hi = b, a
			}
			updates = append(updates, update{lo, hi, inc})
		}
		out := getModifiedArray(100000, updates)
		for _, v := range out {
			checksum = (checksum*31 + v + 100000000) % 1000000007
		}
	}
	fmt.Printf("checksum %d\n", checksum)
}
