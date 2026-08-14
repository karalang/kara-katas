// Benchmark workload for LeetCode #271 — Encode and Decode Strings.
//
// Algorithm-for-algorithm mirror of ../codec.kara. See that file's header for
// what this lane measures and for the two parity decisions (hand-rolled decimal
// in every language; every buffer hoisted out of the punch loop).
package main

import "fmt"

func main() {
	const count int64 = 50000
	const rounds int64 = 250

	// ---- build once: a flat corpus --------------------------------------
	src := make([]byte, 0, count*25)
	off := make([]int64, 0, count)
	length := make([]int64, 0, count)
	var state int64 = 271271
	for i := int64(0); i < count; i++ {
		state = (state*1103515245 + 12345) & 2147483647
		n := (state / 65536) % 25
		off = append(off, int64(len(src)))
		length = append(length, n)
		for p := int64(0); p < n; p++ {
			state = (state*1103515245 + 12345) & 2147483647
			src = append(src, byte(97+(state/65536)%26))
		}
	}

	// ---- hoisted working buffers ----------------------------------------
	enc := make([]byte, int64(len(src))+count*3)
	dout := make([]byte, len(src))

	// ---- punch -----------------------------------------------------------
	var sink int64 = 0
	for r := int64(0); r < rounds; r++ {
		var w int64 = 0
		for k := int64(0); k < count; k++ {
			n := length[k]
			if n >= 10 {
				enc[w] = byte(48 + n/10)
				w++
			}
			enc[w] = byte(48 + n%10)
			w++
			enc[w] = 35 // '#'
			w++
			base := off[k]
			for p := int64(0); p < n; p++ {
				enc[w+p] = src[base+p]
			}
			w += n
		}
		encodedLen := w

		var rp, dp, items, check int64
		for rp < encodedLen {
			var n int64 = 0
			for enc[rp] != 35 {
				n = n*10 + (int64(enc[rp]) - 48)
				rp++
			}
			rp++
			for p := int64(0); p < n; p++ {
				dout[dp+p] = enc[rp+p]
			}
			check = (check*31 + n) % 1000000007
			rp += n
			dp += n
			items++
		}
		sink = (sink*131 + check + items) % 1000000007
	}

	fmt.Println(sink)
}
