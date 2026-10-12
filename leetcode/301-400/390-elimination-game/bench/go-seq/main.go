// Benchmark for #390: mirror of last_remaining.kara (follow the head).
package main

import "fmt"

func lastRemaining(n int64) int64 {
	head, step, left := int64(1), int64(1), n
	fromLeft := true
	for left > 1 {
		if fromLeft || left%2 == 1 {
			head += step
		}
		left /= 2
		step *= 2
		fromLeft = !fromLeft
	}
	return head
}

func next(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	seed, total, checksum := int64(390), int64(0), int64(0)
	for i := 0; i < 10000000; i++ {
		hi := next(&seed)
		n := hi*32768 + next(&seed) + 1
		r := lastRemaining(n)
		total += r
		checksum = (checksum*31 + r) % 1000000007
	}
	fmt.Printf("10000000 values of n, sum %d, checksum %d\n", total, checksum)
}
