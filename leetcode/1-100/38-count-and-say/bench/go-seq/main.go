// LeetCode #38 bench — Go (mirror of count_and_say.kara).
//
// Streaming run-length "say" over a growing byte buffer. Workload: TOTAL times seed with
// the decimal digits of k+1, apply STEPS say-steps, fold a position-weighted digit
// signature of the final term into a checksum (single goroutine — seq).
package main

import (
	"fmt"
	"strconv"
)

// Run lengths stay <= 9 in this workload (verified max 5), so the count is a single
// decimal digit appended in place — fair, allocation-free across the language mirrors.
func say(s []byte) []byte {
	out := make([]byte, 0, len(s)*2)
	var runDigit byte = '0'
	var runLen int64 = 0
	for _, c := range s {
		if runLen != 0 && c == runDigit {
			runLen++
		} else {
			if runLen != 0 {
				out = append(out, byte('0'+runLen))
				out = append(out, runDigit)
			}
			runDigit = c
			runLen = 1
		}
	}
	if runLen != 0 {
		out = append(out, byte('0'+runLen))
		out = append(out, runDigit)
	}
	return out
}

func main() {
	const total int64 = 12000
	const steps int64 = 14
	const modulus int64 = 1000000007

	var acc int64 = 0
	for k := int64(0); k < total; k++ {
		cur := []byte(strconv.FormatInt(k+1, 10))
		for step := int64(0); step < steps; step++ {
			cur = say(cur)
		}

		var sig int64 = 0
		for i, c := range cur {
			dv := int64(c - '0')
			sig += dv * (int64(i) + 1)
		}
		acc = (acc*31 + sig) % modulus
	}

	fmt.Println(acc)
}
