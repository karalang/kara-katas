// LeetCode #2424: Longest Uploaded Prefix -- the bench, the ★ arm: a flag
// for each video and the prefix so far, moved on by `longest` past every
// flag set beyond it.
package main

import "fmt"

type LuPrefix struct {
	uploaded []bool
	prefix   int64
}

func newLuPrefix(n int64) *LuPrefix {
	return &LuPrefix{uploaded: make([]bool, n+2)}
}

func (s *LuPrefix) upload(video int64) { s.uploaded[video] = true }

func (s *LuPrefix) longest() int64 {
	for s.uploaded[s.prefix+1] {
		s.prefix++
	}
	return s.prefix
}

var seed int64 = 2424

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const n int64 = 100000
	scripts := make([][]int64, 0, 10)
	for s := 0; s < 10; s++ {
		width := int64(1) << (s + 3)
		order := make([]int64, n)
		for i := int64(0); i < n; i++ {
			order[i] = i + 1
		}
		for start := int64(0); start < n; {
			end := start + width
			if end > n {
				end = n
			}
			for i := end - 1; i > start; i-- {
				a := nextRandom()
				r := a*32768 + nextRandom()
				j := start + r%(i-start+1)
				order[i], order[j] = order[j], order[i]
			}
			start = end
		}
		scripts = append(scripts, order)
	}
	var check int64
	for p := int64(0); p < 50; p++ {
		for _, order := range scripts {
			server := newLuPrefix(n)
			for _, v := range order {
				server.upload(v)
				check = (check*31 + server.longest() + p) % 1000000007
			}
		}
	}
	fmt.Printf("50 passes over 10 scripts of 10^5 uploads: checksum %d\n", check)
}
