// LeetCode #1529: Minimum Suffix Flips -- bench: the ★ arm over 200
// random strings of 1 to 100000 bits, built once and answered 50 times.
package main

import "fmt"

func minFlips(target string) int64 {
	var flips int64
	prev := byte('0')
	for i := 0; i < len(target); i++ {
		if target[i] != prev {
			flips++
			prev = target[i]
		}
	}
	return flips
}

var seed int64 = 1529

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func mix(check, x int64) int64 {
	return (check*31 + x + 1) % 1000000007
}

func main() {
	targets := make([]string, 0, 200)
	for c := 0; c < 200; c++ {
		hi := nextRandom()
		n := (hi*32768+nextRandom())%100000 + 1
		ones := nextRandom()%9 + 1
		b := make([]byte, n)
		for i := int64(0); i < n; i++ {
			if nextRandom()%10 < ones {
				b[i] = '1'
			} else {
				b[i] = '0'
			}
		}
		targets = append(targets, string(b))
	}
	var check int64
	for pass := 0; pass < 50; pass++ {
		for _, t := range targets {
			check = mix(check, minFlips(t))
		}
	}
	fmt.Printf("50 passes over 200 strings of up to 100000 bits: checksum %d\n", check)
}
