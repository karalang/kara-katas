// Benchmark for #849: Maximize Distance to Closest Person -- Go twin of the
// Kāra ★ arm (one pass, remembering the last person).
package main

import "fmt"

func maxDistToClosest(seats []int64) int64 {
	n := int64(len(seats))
	var last int64 = -1
	var best int64
	for i := int64(0); i < n; i++ {
		if seats[i] == 1 {
			if last < 0 {
				best = i
			} else if (i-last)/2 > best {
				best = (i - last) / 2
			}
			last = i
		}
	}
	if n-1-last > best {
		return n - 1 - last
	}
	return best
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	const count, rounds, n = 64, 20000, 20000
	var seed int64 = 849
	rows := make([][]int64, 0, count)
	for g := 0; g < count; g++ {
		odds := int64(2) << (g % 8)
		seats := make([]int64, n)
		for i := range seats {
			if nextRandom(&seed)%odds == 0 {
				seats[i] = 1
			}
		}
		taken := nextRandom(&seed) % n
		empty := (taken + 1 + nextRandom(&seed)%(n-1)) % n
		seats[taken] = 1
		seats[empty] = 0
		rows = append(rows, seats)
	}
	var total, checksum int64
	for round := 0; round < rounds; round++ {
		d := maxDistToClosest(rows[round%count])
		total += d
		checksum = (checksum*31 + d) % 1000000007
	}
	fmt.Printf("%d rounds of %d rows: distances sum to %d, checksum %d\n", rounds, count, total, checksum)
}
