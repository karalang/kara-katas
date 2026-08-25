// LeetCode 296 benchmark lane — Go mirror of blackpixels.kara.
//
// Same algorithm: 4-way binary search on the row/column projections. Plain
// index loops rather than sort.Search, so the shape matches the other mirrors
// instead of measuring a closure-per-probe indirection.
package main

import "fmt"

var (
	img  []uint8
	W, H int64
)

func rowHasBlack(r int64) bool {
	for c := int64(0); c < W; c++ {
		if img[r*W+c] == 1 {
			return true
		}
	}
	return false
}

func colHasBlack(c int64) bool {
	for r := int64(0); r < H; r++ {
		if img[r*W+c] == 1 {
			return true
		}
	}
	return false
}

func firstBlackRow(lo, hi int64) int64 {
	for lo < hi {
		m := lo + (hi-lo)/2
		if rowHasBlack(m) {
			hi = m
		} else {
			lo = m + 1
		}
	}
	return lo
}

func firstWhiteRow(lo, hi int64) int64 {
	for lo < hi {
		m := lo + (hi-lo)/2
		if rowHasBlack(m) {
			lo = m + 1
		} else {
			hi = m
		}
	}
	return lo
}

func firstBlackCol(lo, hi int64) int64 {
	for lo < hi {
		m := lo + (hi-lo)/2
		if colHasBlack(m) {
			hi = m
		} else {
			lo = m + 1
		}
	}
	return lo
}

func firstWhiteCol(lo, hi int64) int64 {
	for lo < hi {
		m := lo + (hi-lo)/2
		if colHasBlack(m) {
			lo = m + 1
		} else {
			hi = m
		}
	}
	return lo
}

func minArea(x, y int64) int64 {
	top := firstBlackRow(0, x+1)
	bottom := firstWhiteRow(x+1, H)
	left := firstBlackCol(0, y+1)
	right := firstWhiteCol(y+1, W)
	return (bottom - top) * (right - left)
}

func main() {
	const n int64 = 4096
	const queries int64 = 1200
	W, H = n, n
	img = make([]uint8, n*n)

	r0, c0 := n/2, n/2
	for r := int64(0); r < 40; r++ {
		for c := int64(0); c < 40; c++ {
			img[(r0+r)*n+(c0+c)] = 1
		}
	}
	for k := int64(0); k < 25; k++ {
		img[(r0+40+k)*n+(c0+20)] = 1
	}

	var checksum int64
	for q := int64(0); q < queries; q++ {
		sx := r0 + q%40
		sy := c0 + (q*7)%40
		checksum = (checksum*31 + minArea(sx, sy)) % 1000000007
	}
	fmt.Printf("queries %d checksum %d\n", queries, checksum)
}
