// Benchmark for #815: Bus Routes -- mirror of the ★ arm (breadth-first
// search over buses), with the same workload as bus_routes.kara.
package main

import "fmt"

type entry struct {
	bus   int
	count int64
}

func numBusesToDestination(routes [][]int64, source, target int64) int64 {
	if source == target {
		return 0
	}
	busesAt := map[int64][]int{}
	for bus, route := range routes {
		for _, stop := range route {
			busesAt[stop] = append(busesAt[stop], bus)
		}
	}
	first, ok := busesAt[source]
	if !ok {
		return -1
	}
	taken := make([]bool, len(routes))
	queue := []entry{}
	for _, bus := range first {
		taken[bus] = true
		queue = append(queue, entry{bus, 1})
	}
	seen := map[int64]bool{}
	for head := 0; head < len(queue); head++ {
		bus, count := queue[head].bus, queue[head].count
		for _, stop := range routes[bus] {
			if stop == target {
				return count
			}
			if seen[stop] {
				continue
			}
			seen[stop] = true
			for _, next := range busesAt[stop] {
				if !taken[next] {
					taken[next] = true
					queue = append(queue, entry{next, count + 1})
				}
			}
		}
	}
	return -1
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	const count = 64
	const rounds int64 = 4000
	seed := int64(815)
	cities := make([][][]int64, 0, count)
	for g := 0; g < count; g++ {
		routes := make([][]int64, 0, 100)
		for b := 0; b < 100; b++ {
			length := 1 + nextRandom(&seed)%200
			on := map[int64]bool{}
			route := []int64{}
			for int64(len(route)) < length {
				stop := nextRandom(&seed) % 20000
				if !on[stop] {
					on[stop] = true
					route = append(route, stop)
				}
			}
			routes = append(routes, route)
		}
		cities = append(cities, routes)
	}
	total, checksum := int64(0), int64(0)
	for round := int64(0); round < rounds; round++ {
		g := round % count
		ends := []int64{}
		for e := 0; e < 2; e++ {
			if nextRandom(&seed)%8 == 0 {
				ends = append(ends, nextRandom(&seed)%20000)
			} else {
				route := cities[g][nextRandom(&seed)%100]
				ends = append(ends, route[nextRandom(&seed)%int64(len(route))])
			}
		}
		answer := numBusesToDestination(cities[g], ends[0], ends[1])
		total += answer
		checksum = (checksum*31 + answer + 2) % 1000000007
	}
	fmt.Printf("%d rounds of 100 routes: total %d, checksum %d\n", rounds, total, checksum)
}
