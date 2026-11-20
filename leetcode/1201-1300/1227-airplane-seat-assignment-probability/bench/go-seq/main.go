// LeetCode #1227 bench: the running-sum arm in Go, over the same 1000
// random n up to 10^5 as the Kāra bench.
package main

import "fmt"

func nthPersonGetsNthSeat(n int64) float64 {
	f, sum := 1.0, 0.0
	for m := int64(2); m <= n; m++ {
		f = (1.0 + sum) / float64(m)
		sum += f
	}
	return f
}

func main() {
	seed := int64(1227)
	nextRandom := func() int64 {
		seed = (seed*1103515245 + 12345) % 2147483648
		return seed / 65536
	}
	total := 0.0
	for i := 0; i < 1000; i++ {
		a := nextRandom() % 30000 * 3
		n := a + nextRandom()%10000 + 1
		total += nthPersonGetsNthSeat(n)
	}
	fmt.Printf("1000 random n up to 10^5: total %.5f\n", total)
}
