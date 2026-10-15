// Benchmark for #661: each cell's 3x3 window, as the Kara ★ arm.
package main

import "fmt"

func imageSmoother(img [][]int64) [][]int64 {
	m, n := len(img), len(img[0])
	out := make([][]int64, m)
	for i := 0; i < m; i++ {
		out[i] = make([]int64, n)
		for j := 0; j < n; j++ {
			var sum, count int64
			for r := max(i-1, 0); r < min(i+2, m); r++ {
				for c := max(j-1, 0); c < min(j+2, n); c++ {
					sum += img[r][c]
					count++
				}
			}
			out[i][j] = sum / count
		}
	}
	return out
}

var seed int64 = 661

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	size, passes := 1000, 20
	img := make([][]int64, size)
	for i := range img {
		img[i] = make([]int64, size)
		for j := range img[i] {
			img[i][j] = nextRandom() % 256
		}
	}
	for p := 0; p < passes; p++ {
		img = imageSmoother(img)
	}
	var checksum int64
	for _, row := range img {
		for _, v := range row {
			checksum = (checksum*31 + v) % 1000000007
		}
	}
	fmt.Printf("%dx%d, %d passes: checksum %d\n", size, size, passes, checksum)
}
