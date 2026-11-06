// LeetCode #1057: Campus Bikes -- the benchmark, mirror of campus_bikes.kara.
package main

import "fmt"

type pair struct{ w, b int64 }

func abs(x int64) int64 {
	if x < 0 {
		return -x
	}
	return x
}

func assignBikes(workers, bikes [][2]int64) []int64 {
	buckets := make([][]pair, 2000)
	for w, wp := range workers {
		for b, bp := range bikes {
			d := abs(wp[0]-bp[0]) + abs(wp[1]-bp[1])
			buckets[d] = append(buckets[d], pair{int64(w), int64(b)})
		}
	}
	bikeOf := make([]int64, len(workers))
	for w := range bikeOf {
		bikeOf[w] = -1
	}
	taken := make([]bool, len(bikes))
	left := len(workers)
	for _, bucket := range buckets {
		for _, p := range bucket {
			if left > 0 && bikeOf[p.w] < 0 && !taken[p.b] {
				bikeOf[p.w] = p.b
				taken[p.b] = true
				left--
			}
		}
	}
	return bikeOf
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func randomPlaces(count int, seed *int64) [][2]int64 {
	places := make([][2]int64, 0, count)
	for i := 0; i < count; i++ {
		x := nextRandom(seed) % 1000
		y := nextRandom(seed) % 1000
		places = append(places, [2]int64{x, y})
	}
	return places
}

func main() {
	count, rounds := 20, 8
	seed := int64(1057)
	workers := make([][][2]int64, count)
	bikes := make([][][2]int64, count)
	for c := 0; c < count; c++ {
		workers[c] = randomPlaces(300, &seed)
		bikes[c] = randomPlaces(400, &seed)
	}
	var ridden, check int64
	for r := 0; r < rounds; r++ {
		for c := 0; c < count; c++ {
			answer := assignBikes(workers[c], bikes[c])
			for w, b := range answer {
				ridden += abs(workers[c][w][0]-bikes[c][b][0]) + abs(workers[c][w][1]-bikes[c][b][1])
				check = (check*131 + b + 1) % 1000000007
			}
		}
	}
	fmt.Printf("%d campuses of 300 workers and 400 bikes, %d rounds: %d ridden, checksum %d\n", count, rounds, ridden, check)
}
