// LeetCode #171 bench harness — Go peer (go build, single-thread).
//
// Horner-fold bijective base-26 parse — same canonical algorithm as the Kara
// mirror. A LEN=50000 distinct-title corpus (built once) parsed round-robin.
// Sink sums the parsed column numbers across K_ITERS.
package main

import "fmt"

const (
	length = 50000
	kIters = 100000000
)

const letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

func toTitle(num int64) string {
	var tmp [16]byte
	ln := 0
	for num > 0 {
		num--
		tmp[ln] = letters[num%26]
		ln++
		num /= 26
	}
	out := make([]byte, ln)
	for i := 0; i < ln; i++ {
		out[i] = tmp[ln-1-i]
	}
	return string(out)
}

func toNumber(title string) int64 {
	var n int64
	for i := 0; i < len(title); i++ {
		n = n*26 + int64(title[i]-'A') + 1
	}
	return n
}

func main() {
	corpus := make([]string, length)
	for i := int64(0); i < length; i++ {
		corpus[i] = toTitle(i + 1)
	}
	var sum int64
	for k := int64(0); k < kIters; k++ {
		sum += toNumber(corpus[k%length])
	}
	fmt.Println(sum)
}
