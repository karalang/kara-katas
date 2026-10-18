// LeetCode #733: Flood Fill -- depth first, with a stack of places.
// Benchmark mirror of the Kara star arm: push the start; pop a place,
// and if it still has the old color, paint it and push its four
// neighbours.
package main

import "fmt"

type place struct{ r, c int64 }

func floodFill(img [][]int64, sr, sc, color int64) [][]int64 {
	old := img[sr][sc]
	if old == color {
		return img
	}
	m, n := int64(len(img)), int64(len(img[0]))
	stack := []place{{sr, sc}}
	for len(stack) > 0 {
		p := stack[len(stack)-1]
		stack = stack[:len(stack)-1]
		r, c := p.r, p.c
		if r < 0 || r >= m || c < 0 || c >= n || img[r][c] != old {
			continue
		}
		img[r][c] = color
		stack = append(stack, place{r + 1, c}, place{r - 1, c}, place{r, c + 1}, place{r, c - 1})
	}
	return img
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	seed := int64(733)
	size := int64(1000)
	img := make([][]int64, size)
	for r := range img {
		img[r] = make([]int64, size)
		for c := range img[r] {
			if nextRandom(&seed)%3 == 0 {
				img[r][c] = 1
			}
		}
	}
	sum := 0
	for round := 0; round < 40; round++ {
		r := (nextRandom(&seed)*32768 + nextRandom(&seed)) % size
		c := (nextRandom(&seed)*32768 + nextRandom(&seed)) % size
		old := img[r][c]
		img = floodFill(img, r, c, 2)
		for _, v := range img[r] {
			if v == 2 {
				sum++
			}
		}
		img = floodFill(img, r, c, old)
	}
	zeros := 0
	for _, row := range img {
		for _, v := range row {
			if v == 0 {
				zeros++
			}
		}
	}
	fmt.Printf("40 rounds on a 1000 x 1000 image: %d painted in their rows, %d 0s after\n", sum, zeros)
}
