// Benchmark mirror of LeetCode #318 — build-once + punch.
//
// Same algorithm as bench/max_product.kara: a flat WORDS x LMAX letter grid,
// 26-bit letter masks rebuilt every pass, and a full pair scan that records
// each word's best disjoint partner. One word is rewritten per pass.
package main

import "fmt"

const (
	WORDS   = 6000
	LMAX    = 16
	WINDOW  = 7
	PASSES  = 15
	MASKMOD = 1073741823
)

var (
	letters = make([]int64, WORDS*LMAX)
	lens    = make([]int64, WORDS)
	masks   = make([]int64, WORDS)
	best    = make([]int64, WORDS)
)

func nextRand(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func writeWord(w int64, seed *int64) {
	ln := nextRand(seed)%LMAX + 1
	base := nextRand(seed) % (26 - WINDOW + 1)
	lens[w] = ln
	for k := int64(0); k < ln; k++ {
		letters[w*LMAX+k] = base + nextRand(seed)%WINDOW
	}
}

func buildMasks() {
	for w := 0; w < WORDS; w++ {
		var m int64
		for k := int64(0); k < lens[w]; k++ {
			m |= 1 << letters[int64(w)*LMAX+k]
		}
		masks[w] = m
	}
}

func main() {
	var seed int64 = 318318
	for w := int64(0); w < WORDS; w++ {
		writeWord(w, &seed)
	}

	var sink int64
	for p := int64(0); p < PASSES; p++ {
		writeWord(p*977%WORDS, &seed)
		buildMasks()

		for i := 0; i < WORDS; i++ {
			best[i] = 0
		}
		for i := 0; i < WORDS; i++ {
			mi := masks[i]
			li := lens[i]
			for j := i + 1; j < WORDS; j++ {
				if mi&masks[j] == 0 {
					q := li * lens[j]
					if q > best[i] {
						best[i] = q
					}
					if q > best[j] {
						best[j] = q
					}
				}
			}
		}

		var total, top int64
		for i := 0; i < WORDS; i++ {
			total += best[i]
			if best[i] > top {
				top = best[i]
			}
		}
		sink = (sink*31 + total + top) % MASKMOD
	}

	fmt.Printf("checksum %d\n", sink)
}
