package main

import "fmt"

// Build-once + punch word-break; dictionary is a SET realized as a flat stamped
// bool table keyed by a per-length base-A word encoding (see word_break.kara).
func main() {
	var alpha int64 = 5
	var maxlen int64 = 4
	var n int64 = 5000
	var dwords int64 = 120
	var win int64 = 24
	var windows int64 = 2200000

	base := []int64{0, 0}
	pwr := alpha
	var acc int64 = 0
	for b := int64(2); b <= maxlen; b++ {
		acc += pwr
		base = append(base, acc)
		pwr *= alpha
	}
	tsize := acc + pwr

	table := make([]bool, tsize)

	var state int64 = 12345

	s := make([]int64, n)
	for i := int64(0); i < n; i++ {
		state = (state*1103515245 + 12345) & 2147483647
		r := state >> 16
		s[i] = r % alpha
	}

	for w := int64(0); w < dwords; w++ {
		state = (state*1103515245 + 12345) & 2147483647
		rl := state >> 16
		wlen := 2 + (rl % (maxlen - 1))
		var code int64 = 0
		for k := int64(0); k < wlen; k++ {
			state = (state*1103515245 + 12345) & 2147483647
			rc := state >> 16
			code = code*alpha + (rc % alpha)
		}
		table[base[wlen]+code] = true
	}

	dp := make([]bool, win+1)

	var sink int64 = 0
	for wnd := int64(0); wnd < windows; wnd++ {
		state = (state*1103515245 + 12345) & 2147483647
		ro := state >> 16
		off := ro % (n - win)

		for z := int64(0); z <= win; z++ {
			dp[z] = false
		}
		dp[0] = true

		for ii := int64(1); ii <= win; ii++ {
			var low int64 = 0
			if ii > maxlen {
				low = ii - maxlen
			}
			var code int64 = 0
			var pw int64 = 1
			var ln int64 = 0
			for j := ii - 1; j >= low; j-- {
				ch := s[off+j]
				code = ch*pw + code
				pw *= alpha
				ln++
				if dp[j] {
					if table[base[ln]+code] {
						dp[ii] = true
						break
					}
				}
			}
		}

		if dp[win] {
			sink += off + 1
		}
	}

	fmt.Println(sink)
}
