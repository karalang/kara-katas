// Benchmark workload for LeetCode #273 — Integer to English Words.
//
// Algorithm-for-algorithm mirror of ../spell.kara. See that file's header for
// what this lane measures and for the parity decisions — in particular that the
// algorithm PREPENDS, which is preserved here rather than rewritten into a
// strings.Builder that would let this mirror amortize into one growing buffer.
package main

import "fmt"

var small = [20]string{"", "One", "Two", "Three", "Four", "Five", "Six",
	"Seven", "Eight", "Nine", "Ten", "Eleven", "Twelve", "Thirteen", "Fourteen",
	"Fifteen", "Sixteen", "Seventeen", "Eighteen", "Nineteen"}
var tens = [10]string{"", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty",
	"Seventy", "Eighty", "Ninety"}
var scales = [4]string{"", "Thousand", "Million", "Billion"}

func groupName(n int64) string {
	if n == 0 {
		return ""
	}
	if n < 20 {
		return small[n]
	}
	if n < 100 {
		t := tens[n/10]
		r := n % 10
		if r == 0 {
			return t
		}
		return t + " " + small[r]
	}
	h := small[n/100] + " " + "Hundred"
	r := groupName(n % 100)
	if r == "" {
		return h
	}
	return h + " " + r
}

func numberToWords(n int64) string {
	if n == 0 {
		return "Zero"
	}
	out := ""
	rem := n
	var scale int64
	for rem > 0 {
		part := rem % 1000
		if part > 0 {
			piece := groupName(part)
			if scale > 0 {
				piece = piece + " " + scales[scale]
			}
			if out == "" {
				out = piece
			} else {
				out = piece + " " + out
			}
		}
		rem /= 1000
		scale++
	}
	return out
}

func main() {
	const count int64 = 200000
	const rounds int64 = 5

	nums := make([]int64, 0, count)
	var lo int64 = 2147483647
	var hi int64 = 0
	var state int64 = 273273
	for i := int64(0); i < count; i++ {
		state = (state*1103515245 + 12345) & 2147483647
		if state < lo {
			lo = state
		}
		if state > hi {
			hi = state
		}
		nums = append(nums, state)
	}

	var sink int64
	for r := int64(0); r < rounds; r++ {
		for q := int64(0); q < count; q++ {
			w := numberToWords(nums[q])
			for i := 0; i < len(w); i++ {
				sink = (sink*131 + int64(w[i])) % 1000000007
			}
		}
	}

	fmt.Println(sink)
	fmt.Printf("count %d range %d..%d\n", count, lo, hi)
}
