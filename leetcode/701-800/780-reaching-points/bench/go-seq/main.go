// Benchmark for #780: Reaching Points -- mirror of the ★ arm (backwards
// by remainders), with the same workload as the Kāra program.
package main

import "fmt"

func reachingPoints(sx, sy, tx, ty int64) bool {
	x, y := tx, ty
	for x > sx && y > sy && x != y {
		if x > y {
			x %= y
		} else {
			y %= x
		}
	}
	if x == sx && y == sy {
		return true
	}
	if x == sx && y > sy {
		return (y-sy)%x == 0
	}
	if y == sy && x > sx {
		return (x-sx)%y == 0
	}
	return false
}

var seed int64 = 780

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const count = 1024
	var queries [count][4]int64
	for q := int64(0); q < count; q++ {
		sx := 1 + nextRandom()%1000
		sy := 1 + nextRandom()%1000
		a, b := sx, sy
		if q%4 == 3 {
			a = sx + 1
		}
		for a <= 500000000 && b <= 500000000 {
			if nextRandom()%2 == 0 {
				a += b
			} else {
				b += a
			}
		}
		if q%4 == 2 {
			b--
		}
		queries[q] = [4]int64{sx, sy, a, b}
	}
	var yes, checksum int64
	for round := int64(0); round < 15000; round++ {
		for i := int64(0); i < count; i++ {
			q := queries[i]
			if reachingPoints(q[0], q[1], q[2], q[3]) {
				yes++
				checksum = (checksum*31 + i + round) % 1000000007
			}
		}
	}
	fmt.Printf("15000 rounds of 1024 queries: %d reachable, checksum %d\n", yes, checksum)
}
