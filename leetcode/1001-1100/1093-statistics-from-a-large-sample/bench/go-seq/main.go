// Benchmark: LeetCode #1093 Statistics from a Large Sample -- the ★ arm, two
// walks over the counts. Mirrors ../sample_stats.kara.
package main

import "fmt"

func sampleStats(count []int64) []float64 {
	var low, high, sum, total, mode int64 = -1, 0, 0, 0, 0
	for k := int64(0); k < int64(len(count)); k++ {
		c := count[k]
		if c == 0 {
			continue
		}
		if low < 0 {
			low = k
		}
		high = k
		sum += k * c
		total += c
		if c > count[mode] {
			mode = k
		}
	}
	left, right := (total-1)/2, total/2
	var seen, medianLow, medianHigh int64 = 0, -1, -1
	for k := int64(0); k < int64(len(count)); k++ {
		seen += count[k]
		if medianLow < 0 && seen > left {
			medianLow = k
		}
		if seen > right {
			medianHigh = k
			break
		}
	}
	return []float64{float64(low), float64(high), float64(sum) / float64(total), float64(medianLow+medianHigh) / 2.0, float64(mode)}
}

var seed int64 = 1093

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	samples := make([][]int64, 0, 64)
	for k := 0; k < 64; k++ {
		c := make([]int64, 256)
		for i := 0; i < 4+k*4; i++ {
			p := nextRandom() % 256
			c[p] = nextRandom()*91%3000000 + 1
		}
		samples = append(samples, c)
	}
	var modes, check int64
	for round := 0; round < 10000; round++ {
		for j := 0; j < len(samples); j++ {
			samples[j][(round*7+j*13)%256]++
			s := sampleStats(samples[j])
			modes += int64(s[4])
			for _, x := range s {
				check = (check*31 + int64(x*1000000.0)) % 1000000007
			}
		}
	}
	fmt.Printf("10000 rounds over 64 samples: modes sum to %d, checksum %d\n", modes, check)
}
