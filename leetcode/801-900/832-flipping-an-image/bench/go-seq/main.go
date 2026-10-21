// Benchmark for #832: Flipping an Image -- the ★ arm (two pointers in place).
//
// Mirrors flip_and_invert_image.kara: each row is flipped and inverted in
// one walk from both ends, the middle cell of an odd row only inverted.
// The image is changed in place.
package main

import "fmt"

func flipAndInvertImage(img [][]int64) [][]int64 {
	n := len(img)
	for r := 0; r < n; r++ {
		i, j := 0, n-1
		for i < j {
			left := img[r][i]
			img[r][i] = 1 - img[r][j]
			img[r][j] = 1 - left
			i++
			j--
		}
		if i == j {
			img[r][i] = 1 - img[r][i]
		}
	}
	return img
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	const count, rounds = int64(64), int64(4000000)
	seed := int64(832)
	images := make([][][]int64, 0, count)
	for g := int64(0); g < count; g++ {
		n := 17 + g%4
		image := make([][]int64, 0, n)
		for r := int64(0); r < n; r++ {
			row := make([]int64, 0, n)
			for c := int64(0); c < n; c++ {
				row = append(row, nextRandom(&seed)%2)
			}
			image = append(image, row)
		}
		images = append(images, image)
	}
	var total, checksum int64
	for round := int64(0); round < rounds; round++ {
		k := round % count
		images[k] = flipAndInvertImage(images[k])
		row := images[k][round/count%int64(len(images[k]))]
		for _, x := range row {
			total += x
			checksum = (checksum*3 + x) % 1000000007
		}
	}
	fmt.Printf("%d rounds of %d images: %d ones, checksum %d\n", rounds, count, total, checksum)
}
