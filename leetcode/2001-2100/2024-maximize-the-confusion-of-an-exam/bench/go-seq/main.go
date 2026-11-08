// LeetCode #2024: Maximize the Confusion of an Exam -- the ★ arm in Go, the
// same algorithm and workload as confuse.kara: a sliding window for each
// answer, the longer of the two.
package main

import "fmt"

func longestRun(key string, c byte, k int64) int64 {
	var best, other int64
	left := 0
	for right := 0; right < len(key); right++ {
		if key[right] != c {
			other++
		}
		for other > k {
			if key[left] != c {
				other--
			}
			left++
		}
		if int64(right-left+1) > best {
			best = int64(right - left + 1)
		}
	}
	return best
}

func maxConsecutiveAnswers(key string, k int64) int64 {
	t, f := longestRun(key, 'T', k), longestRun(key, 'F', k)
	if t > f {
		return t
	}
	return f
}

var seed int64 = 2024

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	pcts := []int64{50, 70, 90, 97, 99}
	kvals := []int64{1, 10, 100, 1000, 10000}
	keys := make([]string, 0, 20)
	ks := make([]int64, 0, 20)
	for a := 0; a < 20; a++ {
		pct := pcts[a%5]
		buf := make([]byte, 100000)
		for i := range buf {
			if nextRandom()%100 < pct {
				buf[i] = 'T'
			} else {
				buf[i] = 'F'
			}
		}
		keys = append(keys, string(buf))
		ks = append(ks, kvals[a/4])
	}
	var calls, total, check int64
	for r := 0; r < 5; r++ {
		for a := 0; a < 20; a++ {
			best := maxConsecutiveAnswers(keys[a], ks[a])
			calls++
			total += best
			check = (check*31 + best) % 1000000007
		}
	}
	fmt.Printf("%d calls: total %d, checksum %d\n", calls, total, check)
}
