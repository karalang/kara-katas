// LeetCode #2511: Maximum Enemy Forts That Can Be Captured -- Go mirror of
// the benchmark (forts.kara): the same lines, passes and checksum.
package main

import "fmt"

func captureForts(forts []int64) int64 {
	best, last := int64(0), int64(-1)
	for i := int64(0); i < int64(len(forts)); i++ {
		if forts[i] != 0 {
			if last >= 0 && forts[last] == -forts[i] && i-last-1 > best {
				best = i - last - 1
			}
			last = i
		}
	}
	return best
}

var seed int64 = 2511

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	lines := make([][]int64, 2000)
	for k := int64(0); k < 2000; k++ {
		zeros := k%50 + 1
		line := make([]int64, 1000)
		for i := range line {
			r := nextRandom() % (zeros + 2)
			switch {
			case r < zeros:
				line[i] = 0
			case r == zeros:
				line[i] = 1
			default:
				line[i] = -1
			}
		}
		lines[k] = line
	}
	const passes = 115
	var check int64
	for p := int64(0); p < passes; p++ {
		for _, line := range lines {
			at := check % 1000
			kept := line[at]
			line[at] = (check+p)%3 - 1
			check = (check*31 + captureForts(line) + p) % 1000000007
			line[at] = kept
		}
	}
	fmt.Printf("%d passes over 2000 lines of 1000 forts: checksum %d\n", passes, check)
}
