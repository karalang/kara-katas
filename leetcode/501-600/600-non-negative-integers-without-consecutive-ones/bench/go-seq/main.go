// Benchmark for #600: Go mirror of the ★ arm (walk the bits with
// Fibonacci counts); see ../find_integers.kara. The counts are a slice
// built on every call, as the Kāra arm builds a `Vec`.
package main

import "fmt"

func findIntegers(n int64) int64 {
	fib := []int64{1, 2}
	for k := 2; k < 32; k++ {
		fib = append(fib, fib[k-1]+fib[k-2])
	}
	var count int64
	previous := false
	for k := 31; k >= 0; k-- {
		if (n>>k)&1 == 1 {
			count += fib[k]
			if previous {
				return count
			}
			previous = true
		} else {
			previous = false
		}
	}
	return count + 1
}

// ---- benchmark --------------------------------------------------------------

func step(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	count := 1000000
	rounds := 20
	seed := int64(600)
	values := make([]int64, 0, count)
	for i := 0; i < count; i++ {
		hi := step(&seed)
		lo := step(&seed)
		values = append(values, 1+(hi*32768+lo)%1000000000)
	}
	var total, checksum int64
	for round := 0; round < rounds; round++ {
		for g := 0; g < count; g++ {
			got := findIntegers(values[(round*7+g)%count])
			total += got
			checksum = (checksum*31 + got) % 1000000007
		}
	}
	fmt.Printf("%d values, %d rounds: total %d, checksum %d\n", count, rounds, total, checksum)
}
