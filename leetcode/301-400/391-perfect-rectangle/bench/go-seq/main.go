// Benchmark for #391: mirror of perfect_rectangle.kara (corners and area).
package main

import "fmt"

type point struct{ x, y int64 }

func isRectangleCover(rects [][4]int64) bool {
	minX, minY, maxX, maxY := rects[0][0], rects[0][1], rects[0][2], rects[0][3]
	var area int64
	corners := map[point]struct{}{}
	for _, r := range rects {
		minX = min(minX, r[0])
		minY = min(minY, r[1])
		maxX = max(maxX, r[2])
		maxY = max(maxY, r[3])
		area += (r[2] - r[0]) * (r[3] - r[1])
		for _, p := range [4]point{{r[0], r[1]}, {r[0], r[3]}, {r[2], r[1]}, {r[2], r[3]}} {
			if _, ok := corners[p]; ok {
				delete(corners, p)
			} else {
				corners[p] = struct{}{}
			}
		}
	}
	has := func(p point) bool { _, ok := corners[p]; return ok }
	return area == (maxX-minX)*(maxY-minY) && len(corners) == 4 &&
		has(point{minX, minY}) && has(point{minX, maxY}) && has(point{maxX, minY}) && has(point{maxX, maxY})
}

var seed int64 = 391

func step() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func big() int64 {
	hi := step()
	return hi*32768 + step()
}

func tile(x1, y1, x2, y2, pieces int64, out *[][4]int64) {
	w, h := x2-x1, y2-y1
	if pieces <= 1 || (w < 2 && h < 2) {
		*out = append(*out, [4]int64{x1, y1, x2, y2})
		return
	}
	left := 1 + step()%(pieces-1)
	var across bool
	if w < 2 {
		across = false
	} else if h < 2 {
		across = true
	} else {
		across = step()%2 == 0
	}
	if across {
		cut := x1 + 1 + big()%(w-1)
		tile(x1, y1, cut, y2, left, out)
		tile(cut, y1, x2, y2, pieces-left, out)
	} else {
		cut := y1 + 1 + big()%(h-1)
		tile(x1, y1, x2, cut, left, out)
		tile(x1, cut, x2, y2, pieces-left, out)
	}
}

func main() {
	tilings := make([][][4]int64, 50)
	for i := range tilings {
		tile(0, 0, 100000, 100000, 20000, &tilings[i])
	}
	perfect := 0
	var checksum int64
	for round := 0; round < 300; round++ {
		t := tilings[round%50]
		at := big() % int64(len(t))
		edit := step() % 3
		if edit == 1 {
			t[at][0]++
			t[at][2]++
		} else if edit == 2 {
			t[at][3]++
		}
		ok := isRectangleCover(t)
		if edit == 1 {
			t[at][0]--
			t[at][2]--
		} else if edit == 2 {
			t[at][3]--
		}
		if ok {
			perfect++
		}
		if ok {
			checksum = (checksum*3 + 1) % 1000000007
		} else {
			checksum = (checksum*3 + 2) % 1000000007
		}
	}
	fmt.Printf("300 rounds over 50 tilings of 20000 pieces: %d perfect, checksum %d\n", perfect, checksum)
}
