// LeetCode #405 bench harness — Go peer (go build, single-thread).
//
// Bitwise mask-and-shift hex render — same canonical algorithm as the Kara
// mirror. Sequential string-building bench: concatenate TOTAL hex renderings
// into one growing buffer, then byte-checksum it. Persisting the output defeats
// render elision. Sink = byte-sum of the concatenated output.
package main

import "fmt"

const total = 4000000

const hex = "0123456789abcdef"

func toHex(num int64) string {
	n := num & 0xffffffff
	if n == 0 {
		return "0"
	}
	var tmp [8]byte
	ln := 0
	for n > 0 {
		tmp[ln] = hex[n&0xf]
		ln++
		n >>= 4
	}
	out := make([]byte, ln)
	for i := 0; i < ln; i++ {
		out[i] = tmp[ln-1-i]
	}
	return string(out)
}

func main() {
	buf := make([]byte, 0, 1<<20)
	for k := int64(0); k < total; k++ {
		v := (k * 2654435761) & 0xffffffff
		buf = append(buf, toHex(v)...)
	}
	var sum int64
	for _, b := range buf {
		sum += int64(b)
	}
	fmt.Println(sum)
}
