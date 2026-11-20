// LeetCode #1215 bench, in Go: the ★ arm (a breadth-first search from the
// digits 1 to 9, each number followed by itself with one more digit,
// stopping at the first number past `high`) on 2000 random ranges inside
// 0 to 2 * 10^9, drawn once; then 20 rounds over the ranges, each
// answer's length and last number folded into a checksum.
package main

import "fmt"

var seed int64 = 1215

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func countSteppingNumbers(low, high int64) []int64 {
	out := []int64{}
	if low == 0 {
		out = append(out, 0)
	}
	queue := []int64{}
	for d := int64(1); d < 10; d++ {
		queue = append(queue, d)
	}
	for head := 0; head < len(queue); head++ {
		n := queue[head]
		if n > high {
			break
		}
		if n >= low {
			out = append(out, n)
		}
		last := n % 10
		if last > 0 {
			queue = append(queue, n*10+last-1)
		}
		if last < 9 {
			queue = append(queue, n*10+last+1)
		}
	}
	return out
}

func main() {
	lows := make([]int64, 2000)
	highs := make([]int64, 2000)
	for i := range lows {
		a := nextRandom()
		b := nextRandom()
		lows[i] = (a*32768 + b) % 2000000001
		c := nextRandom()
		d := nextRandom()
		highs[i] = lows[i] + (c*32768+d)%(2000000001-lows[i])
	}
	var check int64
	for round := int64(0); round < 20; round++ {
		for i := range lows {
			answer := countSteppingNumbers(lows[i], highs[i])
			var last int64 = -1
			if len(answer) > 0 {
				last = answer[len(answer)-1]
			}
			check = (check*131 + int64(len(answer)) + last%1000003 + round) % 1000000007
		}
	}
	fmt.Printf("20 rounds over 2000 ranges: checksum %d\n", check)
}
