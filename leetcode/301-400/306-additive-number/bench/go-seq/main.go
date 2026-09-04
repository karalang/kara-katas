// LeetCode 306 - Additive Number.
//
// Mirror of additive.kara: the same O(n^3) scan (two prefix lengths, then
// verification by exact digit-list addition) over the same flat digit array,
// with the same planted positives, the same per-pass perturbation and the same
// masked sink. Kept algorithm-for-algorithm so the benchmark lane is honest.
package main

import "fmt"

const (
	cases  = 220
	width  = 18
	passes = 90
	mask   = 1073741823
)

func addDigits(a, b []int64) []int64 {
	rev := make([]int64, 0, 64)
	i, j := len(a)-1, len(b)-1
	var carry int64
	for i >= 0 || j >= 0 || carry > 0 {
		s := carry
		if i >= 0 { s += a[i]; i-- }
		if j >= 0 { s += b[j]; j-- }
		rev = append(rev, s%10)
		carry = s / 10
	}
	out := make([]int64, len(rev))
	for k := range rev { out[k] = rev[len(rev)-1-k] }
	return out
}

func matchesAt(flat []int64, base, n, pos int, num []int64) bool {
	if pos+len(num) > n { return false }
	for k := range num { if flat[base+pos+k] != num[k] { return false } }
	return true
}

func noLeadZero(flat []int64, base, lo, hi int) bool {
	return hi-lo == 1 || flat[base+lo] != 0
}

func isAdditive(flat []int64, base, n int) bool {
	if n < 3 { return false }
	for len1 := 1; len1 < n-1; len1++ {
		if !noLeadZero(flat, base, 0, len1) { break }
		for len2 := 1; len2 < n-len1; len2++ {
			if !noLeadZero(flat, base, len1, len1+len2) { break }
			a := append([]int64(nil), flat[base:base+len1]...)
			b := append([]int64(nil), flat[base+len1:base+len1+len2]...)
			pos, ok, steps := len1+len2, true, 0
			for pos < n && ok {
				c := addDigits(a, b)
				if matchesAt(flat, base, n, pos, c) {
					pos += len(c)
					a, b = b, c
					steps++
				} else { ok = false }
			}
			if ok && pos == n && steps > 0 { return true }
		}
	}
	return false
}

func main() {
	planted := []string{"022461016264268110", "020204060100160260", "021214263105168273", "022224466110176286", "023234669115184299", "024244872120192312", "025255075125200325", "026265278130208338"}
	flat := make([]int64, 0, cases*width)
	var seed int64 = 7
	for c := 0; c < cases; c++ {
		if c%25 == 0 {
			p := planted[(c/25)%len(planted)]
			for i := 0; i < width; i++ { flat = append(flat, int64(p[i]-'0')) }
		} else {
			for i := 0; i < width; i++ {
				seed = (seed*1103515245 + 12345) % 2147483647
				flat = append(flat, seed%10)
			}
		}
	}

	var checksum int64 = 1
	for pass := int64(0); pass < passes; pass++ {
		site := (checksum*31 + pass*7919) % int64(cases*width)
		flat[site] = (flat[site] + 1) % 10
		var hits int64
		for c := 0; c < cases; c++ {
			if isAdditive(flat, c*width, width) { hits++ }
		}
		checksum = (checksum*131 + hits*7919 + site) & mask
	}
	fmt.Printf("checksum %d\n", checksum)
}
