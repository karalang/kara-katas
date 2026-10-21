// Benchmark for #835: Image Overlap -- the ★ arm (shifts counted over pairs of ones).
//
// Mirrors largest_overlap.kara: every pair of a one in the first image and
// a one in the second votes for the shift that lays the first on the
// second, and the shift with the most votes is the answer.
package main

import "fmt"

type cell struct{ r, c int64 }

func largestOverlap(img1, img2 [][]int64) int64 {
	n := int64(len(img1))
	ones1 := make([]cell, 0)
	ones2 := make([]cell, 0)
	for r := int64(0); r < n; r++ {
		for c := int64(0); c < n; c++ {
			if img1[r][c] == 1 {
				ones1 = append(ones1, cell{r, c})
			}
			if img2[r][c] == 1 {
				ones2 = append(ones2, cell{r, c})
			}
		}
	}
	width := 2*n - 1
	votes := make([]int64, width*width)
	best := int64(0)
	for _, a := range ones1 {
		for _, b := range ones2 {
			k := (b.r-a.r+n-1)*width + (b.c - a.c + n - 1)
			votes[k]++
			if votes[k] > best {
				best = votes[k]
			}
		}
	}
	return best
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	// 64 pairs of images drawn once, each of LeetCode's largest size, 30
	// by 30, the share of ones running from 2% to 98% over the pairs, the
	// two images of pair k at 2k and 2k + 1 in one list. Each round solves
	// the next pair.
	count := int64(64)
	rounds := int64(4000)
	n := int64(30)
	seed := int64(835)
	images := make([][][]int64, 0)
	for g := int64(0); g < count; g++ {
		percent := 2 + g*96/(count-1)
		for i := 0; i < 2; i++ {
			img := make([][]int64, 0)
			for r := int64(0); r < n; r++ {
				row := make([]int64, 0)
				for c := int64(0); c < n; c++ {
					if nextRandom(&seed)%100 < percent {
						row = append(row, 1)
					} else {
						row = append(row, 0)
					}
				}
				img = append(img, row)
			}
			images = append(images, img)
		}
	}
	total := int64(0)
	checksum := int64(0)
	for round := int64(0); round < rounds; round++ {
		k := round % count
		x := largestOverlap(images[2*k], images[2*k+1])
		total += x
		checksum = (checksum*131 + x) % 1000000007
	}
	fmt.Printf("%d rounds of %d pairs: overlaps total %d, checksum %d\n", rounds, count, total, checksum)
}
