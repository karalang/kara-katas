// LeetCode #1505: Minimum Possible Integer After at Most K Adjacent Swaps On
// Digits -- the benchmark, the same algorithm as swaps.kara: per-digit
// queues of indices and a Fenwick tree of the digits already taken.
package main

import "fmt"

func takenBefore(tree []int64, i int) int64 {
	var s int64
	for i > 0 {
		s += tree[i]
		i -= i & -i
	}
	return s
}

func take(tree []int64, i int) {
	for at := i + 1; at < len(tree); at += at & -at {
		tree[at]++
	}
}

func minInteger(num []byte, k int64) []byte {
	n := len(num)
	wh := make([][]int, 10)
	for i, c := range num {
		wh[c-'0'] = append(wh[c-'0'], i)
	}
	head := make([]int, 10)
	tree := make([]int64, n+1)
	left := k
	out := make([]byte, 0, n)
	for r := 0; r < n; r++ {
		for d := 0; d < 10; d++ {
			if head[d] < len(wh[d]) {
				i := wh[d][head[d]]
				cost := int64(i) - takenBefore(tree, i)
				if cost <= left {
					left -= cost
					head[d]++
					take(tree, i)
					out = append(out, byte('0'+d))
					break
				}
			}
		}
	}
	return out
}

var seed int64 = 1505

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func mix(check, x int64) int64 { return (check*31 + x + 1) % 1000000007 }

func main() {
	nums := make([][]byte, 60)
	ks := make([]int64, 60)
	for c := 0; c < 60; c++ {
		digits := int64(c%10 + 1)
		nums[c] = make([]byte, 30000)
		for i := range nums[c] {
			nums[c][i] = byte(48 + nextRandom()%digits)
		}
		ks[c] = nextRandom() * int64(c%7+1) * 50
	}
	var check int64
	for c := 0; c < 60; c++ {
		for _, b := range minInteger(nums[c], ks[c]) {
			check = mix(check, int64(b)-48)
		}
	}
	fmt.Printf("60 numbers of 30000 digits: checksum %d\n", check)
}
