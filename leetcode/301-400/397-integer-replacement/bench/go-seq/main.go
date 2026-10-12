// Benchmark for #397: mirror of integer_replacement.kara (greedy on the last two bits).
package main

import "fmt"

func integerReplacement(n int64) int64 {
	v := n
	var ops int64
	for v != 1 {
		if v%2 == 0 {
			v = v / 2
		} else if v == 3 || v%4 == 1 {
			v -= 1
		} else {
			v += 1
		}
		ops++
	}
	return ops
}

var seed int64 = 397

func step() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	calls := 5000000
	var total, checksum int64
	for c := 0; c < calls; c++ {
		hi := step()
		n := 1 + (hi*32768+step())%2147483647
		r := integerReplacement(n)
		total += r
		checksum = (checksum*31 + r) % 1000000007
	}
	fmt.Printf("%d calls: total %d, checksum %d\n", calls, total, checksum)
}
