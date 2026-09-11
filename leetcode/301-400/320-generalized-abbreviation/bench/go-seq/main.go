// Benchmark mirror of LeetCode #320 — same mask walk as
// bench/generalized_abbreviation.kara.
package main

import "fmt"

const (
	wordLen = 20
	passes  = 8
	modulus = 1073741789
)

func main() {
	var sink int64
	var totalChars int64

	for p := int64(0); p < passes; p++ {
		var bs [wordLen]byte
		for i := int64(0); i < wordLen; i++ {
			bs[i] = byte((i*7+p*11)%26) + 'a'
		}

		var buf [wordLen + 8]byte
		limit := int64(1) << wordLen
		var acc int64
		var chars int64

		for mask := int64(0); mask < limit; mask++ {
			length := 0
			run := int64(0)
			for i := int64(0); i < wordLen; i++ {
				if mask&(int64(1)<<uint(i)) != 0 {
					run++
				} else {
					if run > 0 {
						if run >= 10 {
							buf[length] = byte(run/10) + '0'
							length++
						}
						buf[length] = byte(run%10) + '0'
						length++
						run = 0
					}
					buf[length] = bs[i]
					length++
				}
			}
			if run > 0 {
				if run >= 10 {
					buf[length] = byte(run/10) + '0'
					length++
				}
				buf[length] = byte(run%10) + '0'
				length++
			}

			for j := 0; j < length; j++ {
				acc = (acc*131 + int64(buf[j])) % modulus
			}
			acc = (acc*131 + 7) % modulus
			chars += int64(length)
		}

		sink = (sink*1000003 + acc) % modulus
		totalChars += chars
	}

	fmt.Printf("sink %d chars %d\n", sink, totalChars)
}
