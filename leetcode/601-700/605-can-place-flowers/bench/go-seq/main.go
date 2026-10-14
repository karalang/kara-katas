// Benchmark for #605: Go mirror of the ★ arm (plant greedily); see
// ../can_place_flowers.kara. The bed is copied into a fresh slice on
// every call, as the Kāra arm clones it.
package main

import "fmt"

func canPlaceFlowers(flowerbed []int64, n int64) bool {
	bed := append([]int64(nil), flowerbed...)
	var planted int64
	for i := range bed {
		if bed[i] == 0 && (i == 0 || bed[i-1] == 0) && (i == len(bed)-1 || bed[i+1] == 0) {
			bed[i] = 1
			planted++
		}
	}
	return planted >= n
}

func step(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	const count, rounds, size = 100, 50, 20000
	seed := int64(605)
	beds := make([][]int64, 0, count)
	for b := 0; b < count; b++ {
		spread := 2 + step(&seed)%5
		bed := []int64{}
		for i := 0; i < size; i++ {
			if step(&seed)%spread == 0 && (i == 0 || bed[i-1] == 0) {
				bed = append(bed, 1)
			} else {
				bed = append(bed, 0)
			}
		}
		beds = append(beds, bed)
	}
	yes := 0
	var checksum int64
	for round := int64(0); round < rounds; round++ {
		for g := int64(0); g < count; g++ {
			n := (round*397 + g*113) % 8000
			fits := canPlaceFlowers(beds[(round*7+g)%count], n)
			bit := int64(0)
			if fits {
				yes++
				bit = 1
			}
			checksum = (checksum*31 + n*2 + bit) % 1000000007
		}
	}
	fmt.Printf("%d beds, %d rounds: %d fit, checksum %d\n", count, rounds, yes, checksum)
}
