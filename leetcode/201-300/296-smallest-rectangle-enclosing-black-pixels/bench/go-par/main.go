// Par-lane Go mirror for LeetCode #296 — the four edge searches by hand.
//
// Kara's auto-par fans out the four independent searches inside min_area with
// no annotation (`karac query concurrency`: parallel_groups [0,1,2,3]). Here it
// is written out: three goroutines plus the calling goroutine, joined by a
// WaitGroup, over the same immutable image.
//
// Goroutines are the cheapest of the three hand-parallel mirrors to spawn —
// they multiplex onto an existing M:N scheduler rather than creating an OS
// thread per call the way the raw-pthreads C mirror does. That difference is
// part of what the par lane is measuring.
package main

import (
	"fmt"
	"sync"
)

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

func minAreaPar(x, y int64) int64 {
	var top, bottom, left, right int64
	var wg sync.WaitGroup
	wg.Add(3)
	go func() { defer wg.Done(); bottom = firstWhiteRow(x+1, H) }()
	go func() { defer wg.Done(); left = firstBlackCol(0, y+1) }()
	go func() { defer wg.Done(); right = firstWhiteCol(y+1, W) }()
	top = firstBlackRow(0, x+1)
	wg.Wait()
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
		checksum = (checksum*31 + minAreaPar(sx, sy)) % 1000000007
	}
	fmt.Printf("queries %d checksum %d\n", queries, checksum)
}
