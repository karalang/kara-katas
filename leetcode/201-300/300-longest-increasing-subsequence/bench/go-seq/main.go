// Benchmark mirror of lisscan.kara — LeetCode #300, Longest Increasing
// Subsequence. Same patience sorting, same hand-written binary search, same
// reused tails buffer. See ../../README.md § Benchmarks.
package main

import "fmt"

const (
	nArrays = 3000
	length  = 512
	passes  = 24
	spread  = 4096
)

func lcg(state int64) int64 {
	return (state*1103515245 + 12345) & 0x7fffffff
}

func main() {
	total := nArrays * length
	data := make([]int64, total)

	var state int64 = 20300
	for i := 0; i < total; i++ {
		state = lcg(state)
		data[i] = (state / 65536) % spread
	}

	var tails [length]int64
	var checksum int64

	for pass := 0; pass < passes; pass++ {
		for a := 0; a < nArrays; a++ {
			base := a * length
			nTails := 0

			for k := 0; k < length; k++ {
				x := data[base+k]

				lo, hi := 0, nTails
				for lo < hi {
					mid := lo + (hi-lo)/2
					if tails[mid] < x {
						lo = mid + 1
					} else {
						hi = mid
					}
				}

				if lo == nTails {
					tails[nTails] = x
					nTails++
				} else {
					tails[lo] = x
				}
			}

			checksum = (checksum*31 + int64(nTails)) % 1000000007
		}
	}

	fmt.Printf("arrays %d len %d passes %d checksum %d\n", nArrays, length, passes, checksum)
}
