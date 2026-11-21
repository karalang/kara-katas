// LeetCode #2481: Minimum Cuts to Divide a Circle -- bench, Go mirror of
// cuts.kara.
package main

import "fmt"

func numberOfCuts(n int64) int64 {
	if n == 1 {
		return 0
	} else if n%2 == 0 {
		return n / 2
	}
	return n
}

func main() {
	check := int64(0)
	for p := int64(0); p < 500000; p++ {
		start := check % 100
		for i := int64(0); i < 100; i++ {
			n := 1 + (start+i)%100
			check = (check*31 + numberOfCuts(n) + p) % 1000000007
		}
	}
	fmt.Printf("500000 passes over every count from 1 to 100: checksum %d\n", check)
}
