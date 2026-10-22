// Benchmark for #853: Car Fleet -- Go twin of the Kāra ★ arm (closest to
// the target first).
package main

import (
	"fmt"
	"slices"
)

type car struct{ p, s int64 }

func carFleet(target int64, position, speed []int64) int64 {
	cars := make([]car, 0, len(position))
	for i := range position {
		cars = append(cars, car{position[i], speed[i]})
	}
	slices.SortFunc(cars, func(a, b car) int {
		if a.p != b.p {
			if a.p < b.p {
				return -1
			}
			return 1
		}
		if a.s < b.s {
			return -1
		}
		if a.s > b.s {
			return 1
		}
		return 0
	})
	var fleets, far int64
	var fast int64 = 1
	for i := len(cars) - 1; i >= 0; i-- {
		p, s := cars[i].p, cars[i].s
		if (target-p)*fast > far*s {
			fleets++
			far = target - p
			fast = s
		}
	}
	return fleets
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	const count, rounds, n = 64, 150, 100000
	const target int64 = 1000000
	var seed int64 = 853
	positions := make([][]int64, 0, count)
	speeds := make([][]int64, 0, count)
	for g := int64(0); g < count; g++ {
		top := 1 + (g%8)*142857
		taken := make([]bool, target)
		position := make([]int64, 0, n)
		for len(position) < n {
			p := (nextRandom(&seed)*32768 + nextRandom(&seed)) % target
			if !taken[p] {
				taken[p] = true
				position = append(position, p)
			}
		}
		speed := make([]int64, 0, n)
		for i := 0; i < n; i++ {
			speed = append(speed, 1+(nextRandom(&seed)*32768+nextRandom(&seed))%top)
		}
		positions = append(positions, position)
		speeds = append(speeds, speed)
	}
	var total, checksum int64
	for round := 0; round < rounds; round++ {
		g := round % count
		f := carFleet(target, positions[g], speeds[g])
		total += f
		checksum = (checksum*31 + f) % 1000000007
	}
	fmt.Printf("%d rounds of %d roads: fleets sum to %d, checksum %d\n", rounds, count, total, checksum)
}
