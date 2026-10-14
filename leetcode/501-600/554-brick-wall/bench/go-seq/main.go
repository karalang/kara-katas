// Benchmark for #554: Go mirror of the ★ arm (count the edges at each
// position); see ../brick_wall.kara.
package main

import "fmt"

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func leastBricks(wall [][]int64) int64 {
	edges := map[int64]int64{}
	var most int64
	for _, row := range wall {
		var at int64
		for j := 0; j < len(row)-1; j++ {
			at += row[j]
			count := edges[at] + 1
			edges[at] = count
			if count > most {
				most = count
			}
		}
	}
	return int64(len(wall)) - most
}

func main() {
	count := 20
	seed := int64(554)
	walls := [][][]int64{}
	bricks := 0
	for i := 0; i < count; i++ {
		wall := [][]int64{}
		n := 0
		for n < 19000 {
			row := []int64{}
			left := int64(1000000)
			for left > 0 {
				a := nextRandom(&seed)
				b := nextRandom(&seed)
				w := 1 + (a*32768+b)%10000
				if w > left {
					w = left
				}
				row = append(row, w)
				left -= w
			}
			n += len(row)
			wall = append(wall, row)
		}
		bricks += n
		walls = append(walls, wall)
	}
	var total, checksum int64
	for round := 0; round < 50; round++ {
		for g := 0; g < count; g++ {
			got := leastBricks(walls[(round*7+g)%count])
			total += got
			checksum = (checksum*31 + got) % 1000000007
		}
	}
	fmt.Printf("%d walls, %d bricks, 50 rounds each: total %d, checksum %d\n", count, bricks, total, checksum)
}
