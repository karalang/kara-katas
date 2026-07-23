package main

import "fmt"

type Building struct {
	left, right, height int64
}

type Point struct {
	x, h int64
}

func merge(left, right []Point) []Point {
	result := make([]Point, 0, len(left)+len(right))
	nl := int64(len(left))
	nr := int64(len(right))
	var i, j, h1, h2 int64 = 0, 0, 0, 0
	for i < nl && j < nr {
		var x int64
		if left[i].x < right[j].x {
			x = left[i].x
			h1 = left[i].h
			i++
		} else if left[i].x > right[j].x {
			x = right[j].x
			h2 = right[j].h
			j++
		} else {
			x = left[i].x
			h1 = left[i].h
			h2 = right[j].h
			i++
			j++
		}
		var maxh int64 = h1
		if h2 > maxh {
			maxh = h2
		}
		if len(result) == 0 || result[len(result)-1].h != maxh {
			result = append(result, Point{x, maxh})
		}
	}
	for i < nl {
		result = append(result, left[i])
		i++
	}
	for j < nr {
		result = append(result, right[j])
		j++
	}
	return result
}

func skyline(bs []Building, lo, hi int64) []Point {
	if hi-lo == 1 {
		b := bs[lo]
		return []Point{{b.left, b.height}, {b.right, 0}}
	}
	mid := lo + (hi-lo)/2
	left := skyline(bs, lo, mid)
	right := skyline(bs, mid, hi)
	return merge(left, right)
}

func main() {
	var n, passes, xr, wr, hr int64 = 24000, 100, 200000, 120, 1000

	bs := make([]Building, 0, n)
	var state int64 = 12345
	for i := int64(0); i < n; i++ {
		state = (state*1103515245 + 12345) & 2147483647
		left := state % xr
		state = (state*1103515245 + 12345) & 2147483647
		width := 1 + state%wr
		state = (state*1103515245 + 12345) & 2147483647
		height := 1 + state%hr
		bs = append(bs, Building{left, left + width, height})
	}

	var sink int64 = 0
	for p := int64(0); p < passes; p++ {
		state = (state*1103515245 + 12345) & 2147483647
		idx := p % n
		bs[idx].height = 1 + state%hr
		sky := skyline(bs, 0, n)
		for _, pt := range sky {
			sink += pt.x + pt.h
		}
	}
	fmt.Println(sink)
}
