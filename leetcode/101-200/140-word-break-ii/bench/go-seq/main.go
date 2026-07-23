package main

import "fmt"

// Exponential-backtracking segmentation COUNT for LeetCode #140 (see
// word_break_ii.kara). Dict SET is a flat stamped base-A table.
const (
	alpha  int64 = 3
	minlen int64 = 1
	maxlen int64 = 3
	slen   int64 = 16
)

var (
	s     []int64
	table []bool
	base  []int64
)

func count(start int64) int64 {
	if start == slen {
		return 1
	}
	var total int64 = 0
	var code int64 = 0
	for end := start + 1; end <= slen && end-start <= maxlen; end++ {
		code = code*alpha + s[end-1]
		ln := end - start
		if ln >= minlen {
			if table[base[ln]+code] {
				total += count(end)
			}
		}
	}
	return total
}

func main() {
	var dwords int64 = 25
	var cases int64 = 80000

	base = []int64{0, 0}
	pwr := alpha
	var acc int64 = 0
	for b := int64(2); b <= maxlen; b++ {
		acc += pwr
		base = append(base, acc)
		pwr *= alpha
	}
	tsize := acc + pwr

	table = make([]bool, tsize)
	s = make([]int64, slen)

	var state int64 = 12345
	var sink int64 = 0

	for c := int64(0); c < cases; c++ {
		for z := int64(0); z < tsize; z++ {
			table[z] = false
		}
		for i := int64(0); i < slen; i++ {
			state = (state*1103515245 + 12345) & 2147483647
			r := state >> 16
			s[i] = r % alpha
		}
		for w := int64(0); w < dwords; w++ {
			state = (state*1103515245 + 12345) & 2147483647
			rl := state >> 16
			span := maxlen - minlen + 1
			wlen := minlen + (rl % span)
			var code int64 = 0
			for k := int64(0); k < wlen; k++ {
				state = (state*1103515245 + 12345) & 2147483647
				rc := state >> 16
				code = code*alpha + (rc % alpha)
			}
			table[base[wlen]+code] = true
		}

		sink += count(0)
	}

	fmt.Println(sink)
}
