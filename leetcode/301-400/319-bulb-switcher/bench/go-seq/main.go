// Benchmark mirror of LeetCode #319 — the round simulation.
//
// Same algorithm as bench/bulb_switcher.kara: PASSES passes, each simulating
// n rounds over an n-bulb byte array and folding the count of lit bulbs
// together with the sum of their indices.
package main

import "fmt"

const (
	BULBS   = 6000000
	PASSES  = 10
	STRIDE  = 90011
	MASKMOD = 1073741823
)

func main() {
	on := make([]byte, BULBS+1)

	var sink int64
	for p := int64(0); p < PASSES; p++ {
		n := int64(BULBS) - p*STRIDE

		for b := int64(0); b <= n; b++ {
			on[b] = 0
		}

		for step := int64(1); step <= n; step++ {
			for b := step; b <= n; b += step {
				on[b] ^= 1
			}
		}

		var count, idxSum int64
		for b := int64(1); b <= n; b++ {
			if on[b] == 1 {
				count++
				idxSum = (idxSum + b) % MASKMOD
			}
		}
		sink = (sink*31 + count*7919 + idxSum) % MASKMOD
	}

	fmt.Printf("checksum %d\n", sink)
}
