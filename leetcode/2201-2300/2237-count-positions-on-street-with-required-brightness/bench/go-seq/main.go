// LeetCode #2237: Count Positions on Street With Required Brightness --
// the benchmark's Go mirror of brightness.kara: a difference array, a
// running sum, and the positions meeting their requirement counted.
package main

import "fmt"

func meetRequirement(n int64, lights [][2]int64, requirement []int64) int64 {
	change := make([]int64, n+1)
	for _, light := range lights {
		from := light[0] - light[1]
		if from < 0 {
			from = 0
		}
		to := light[0] + light[1]
		if to > n-1 {
			to = n - 1
		}
		change[from]++
		change[to+1]--
	}
	brightness, count := int64(0), int64(0)
	for i := int64(0); i < n; i++ {
		brightness += change[i]
		if brightness >= requirement[i] {
			count++
		}
	}
	return count
}

var seed int64 = 2237

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wideRandom() int64 {
	high := nextRandom()
	return high*32768 + nextRandom()
}

func main() {
	n := int64(100000)
	lights := make([][2]int64, 100000)
	for k := range lights {
		position := wideRandom() % n
		lights[k] = [2]int64{position, wideRandom() % 1001}
	}
	requirement := make([]int64, n)
	for i := range requirement {
		requirement[i] = wideRandom() % 2001
	}
	check := int64(0)
	for pass := 0; pass < 100; pass++ {
		// punch: one light and one requirement drawn again before each pass
		at := wideRandom() % 100000
		position := wideRandom() % n
		lights[at] = [2]int64{position, wideRandom() % 1001}
		place := wideRandom() % n
		requirement[place] = wideRandom() % 2001
		check = (check*31 + meetRequirement(n, lights, requirement)) % 1000000007
	}
	fmt.Printf("100 passes over 10^5 positions and lights: checksum %d\n", check)
}
