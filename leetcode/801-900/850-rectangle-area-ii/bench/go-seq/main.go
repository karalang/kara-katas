// Benchmark for #850: Rectangle Area II -- Go twin of the Kāra segment-tree
// arm (a sweep line over a segment tree).
package main

import (
	"fmt"
	"slices"
)

type event struct{ x, delta, y1, y2 int64 }

type cover struct {
	ys     []int64
	count  []int64
	length []int64
}

func update(t *cover, node, lo, hi, a, b int, delta int64) {
	if b <= lo || hi <= a {
		return
	}
	if a <= lo && hi <= b {
		t.count[node] += delta
	} else {
		mid := (lo + hi) / 2
		update(t, 2*node, lo, mid, a, b, delta)
		update(t, 2*node+1, mid, hi, a, b, delta)
	}
	if t.count[node] > 0 {
		t.length[node] = t.ys[hi] - t.ys[lo]
	} else if hi-lo == 1 {
		t.length[node] = 0
	} else {
		t.length[node] = t.length[2*node] + t.length[2*node+1]
	}
}

func cmp64(a, b int64) int {
	if a < b {
		return -1
	}
	if a > b {
		return 1
	}
	return 0
}

func rectangleArea(rectangles [][4]int64) int64 {
	ys := make([]int64, 0, 2*len(rectangles))
	events := make([]event, 0, 2*len(rectangles))
	for _, r := range rectangles {
		ys = append(ys, r[1], r[3])
		events = append(events, event{r[0], 1, r[1], r[3]}, event{r[2], -1, r[1], r[3]})
	}
	slices.Sort(ys)
	ys = slices.Compact(ys)
	slices.SortFunc(events, func(a, b event) int {
		if c := cmp64(a.x, b.x); c != 0 {
			return c
		}
		if c := cmp64(a.delta, b.delta); c != 0 {
			return c
		}
		if c := cmp64(a.y1, b.y1); c != 0 {
			return c
		}
		return cmp64(a.y2, b.y2)
	})
	segments := len(ys) - 1
	t := cover{slices.Clone(ys), make([]int64, 4*len(ys)), make([]int64, 4*len(ys))}
	var area, prevX int64
	for _, e := range events {
		area += t.length[1] * (e.x - prevX)
		prevX = e.x
		if segments > 0 {
			a, _ := slices.BinarySearch(ys, e.y1)
			b, _ := slices.BinarySearch(ys, e.y2)
			update(&t, 1, 0, segments, a, b, e.delta)
		}
	}
	return area % 1000000007
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	const count, rounds, n = 64, 8000, 200
	const limit int64 = 1000000000
	var seed int64 = 850
	sets := make([][][4]int64, 0, count)
	for g := 0; g < count; g++ {
		size := limit >> (g % 8)
		rectangles := make([][4]int64, 0, n)
		for i := 0; i < n; i++ {
			a := (nextRandom(&seed)*32768 + nextRandom(&seed)) % (size + 1)
			b := (nextRandom(&seed)*32768 + nextRandom(&seed)) % (size + 1)
			c := (nextRandom(&seed)*32768 + nextRandom(&seed)) % (size + 1)
			d := (nextRandom(&seed)*32768 + nextRandom(&seed)) % (size + 1)
			rectangles = append(rectangles, [4]int64{min(a, b), min(c, d), max(a, b), max(c, d)})
		}
		sets = append(sets, rectangles)
	}
	var total, checksum int64
	for round := 0; round < rounds; round++ {
		a := rectangleArea(sets[round%count])
		total += a
		checksum = (checksum*31 + a) % 1000000007
	}
	fmt.Printf("%d rounds of %d sets: areas sum to %d, checksum %d\n", rounds, count, total, checksum)
}
