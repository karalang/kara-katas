// LeetCode #2152: Minimum Number of Lines to Cover Points -- the
// benchmark's Go mirror of lines.kara.
package main

import "fmt"

func minimumLines(points [][2]int64) int64 {
	n := len(points)
	full := (1 << n) - 1
	fewest := make([]int64, 1<<n)
	for m := range fewest {
		fewest[m] = int64(n) + 1
	}
	fewest[0] = 0
	for mask := 0; mask < full; mask++ {
		if fewest[mask] > int64(n) {
			continue
		}
		i := 0
		for (mask>>i)&1 == 1 {
			i++
		}
		alone := mask | (1 << i)
		if fewest[mask]+1 < fewest[alone] {
			fewest[alone] = fewest[mask] + 1
		}
		for j := i + 1; j < n; j++ {
			line := 0
			for k := 0; k < n; k++ {
				cross := (points[j][0]-points[i][0])*(points[k][1]-points[i][1]) - (points[j][1]-points[i][1])*(points[k][0]-points[i][0])
				if cross == 0 {
					line |= 1 << k
				}
			}
			if fewest[mask]+1 < fewest[mask|line] {
				fewest[mask|line] = fewest[mask] + 1
			}
		}
	}
	return fewest[full]
}

var seed int64 = 2152

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func freePlace(points [][2]int64) [2]int64 {
	for {
		x := nextRandom()%7 - 3
		y := nextRandom()%7 - 3
		taken := false
		for _, p := range points {
			if p[0] == x && p[1] == y {
				taken = true
			}
		}
		if !taken {
			return [2]int64{x, y}
		}
	}
}

func main() {
	sets := make([][][2]int64, 4)
	for s := range sets {
		for len(sets[s]) < 10 {
			sets[s] = append(sets[s], freePlace(sets[s]))
		}
	}
	var total, check int64
	for round := int64(0); round < 2500; round++ {
		for s := 0; s < 4; s++ {
			at := nextRandom() % 10
			sets[s][at] = freePlace(sets[s])
			lines := minimumLines(sets[s])
			total += lines
			check = (check*31 + lines + round) % 1000000007
		}
	}
	fmt.Printf("10000 solves: %d lines in all, checksum %d\n", total, check)
}
