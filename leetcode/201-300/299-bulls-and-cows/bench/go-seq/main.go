// Benchmark mirror of bullscore.kara — LeetCode #299, Bulls and Cows.
// Same algorithm: build boards once, then 12 scoring passes over a flat digit
// array. See ../../README.md § Benchmarks.
package main

import "fmt"

const (
	nPairs   = 400000
	passes   = 12
	width    = 4
	alphabet = 4
)

func lcg(state int64) int64 {
	return (state*1103515245 + 12345) & 0x7fffffff
}

func main() {
	total := nPairs * width
	secrets := make([]int64, total)
	guesses := make([]int64, total)

	var state int64 = 20299
	for i := 0; i < total; i++ {
		state = lcg(state)
		secrets[i] = (state / 65536) % alphabet
		state = lcg(state)
		guesses[i] = (state / 65536) % alphabet
	}

	var checksum int64
	for pass := 0; pass < passes; pass++ {
		for p := 0; p < nPairs; p++ {
			base := p * width
			var sLeft [alphabet]int64
			var gLeft [alphabet]int64
			var bulls, cows int64

			for k := 0; k < width; k++ {
				sd := secrets[base+k]
				gd := guesses[base+k]
				if sd == gd {
					bulls++
				} else {
					sLeft[sd]++
					gLeft[gd]++
				}
			}
			for d := 0; d < alphabet; d++ {
				if sLeft[d] < gLeft[d] {
					cows += sLeft[d]
				} else {
					cows += gLeft[d]
				}
			}

			checksum = (checksum*31 + bulls*7 + cows) % 1000000007
		}
	}

	fmt.Printf("pairs %d passes %d checksum %d\n", nPairs, passes, checksum)
}
