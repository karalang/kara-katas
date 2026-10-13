// Benchmark for #492: Go mirror of the ★ arm (down from the square root);
// see ../construct_the_rectangle.kara.
package main

import (
	"fmt"
	"math"
)

func constructRectangle(area int64) []int64 {
	width := int64(math.Sqrt(float64(area)))
	for width*width > area {
		width--
	}
	for (width+1)*(width+1) <= area {
		width++
	}
	for area%width != 0 {
		width--
	}
	return []int64{area / width, width}
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	// 200,000 random areas from 1 to ten million, built once, then each
	// solved once.
	areas := make([]int64, 0, 200000)
	var seed int64 = 492
	for i := 0; i < 200000; i++ {
		high := nextRandom(&seed)
		areas = append(areas, 1+(high*32768+nextRandom(&seed))%10000000)
	}
	squares, thin := 0, 0
	var checksum int64
	for _, area := range areas {
		sides := constructRectangle(area)
		if sides[0] == sides[1] {
			squares++
		}
		if sides[1] == 1 {
			thin++
		}
		checksum = (checksum*31 + sides[0] - sides[1]) % 1000000007
	}
	fmt.Printf("200000 areas: %d squares, %d of width 1, checksum %d\n", squares, thin, checksum)
}
