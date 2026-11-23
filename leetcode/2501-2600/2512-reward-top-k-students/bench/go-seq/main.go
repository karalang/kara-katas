// LeetCode #2512: Reward Top K Students -- Go mirror of the benchmark
// (reward.kara): the same cases, passes and checksum, the words in two
// maps and each report's words looked up as they are split.
package main

import (
	"fmt"
	"sort"
	"strings"
)

type ranked struct{ score, id int64 }

func topStudents(positive, negative, report []string, studentID []int64, k int64) []int64 {
	good := make(map[string]struct{}, len(positive))
	for _, w := range positive {
		good[w] = struct{}{}
	}
	bad := make(map[string]struct{}, len(negative))
	for _, w := range negative {
		bad[w] = struct{}{}
	}
	all := make([]ranked, 0, len(report))
	for i, r := range report {
		var score int64
		for _, w := range strings.Split(r, " ") {
			if _, ok := good[w]; ok {
				score += 3
			} else if _, ok := bad[w]; ok {
				score--
			}
		}
		all = append(all, ranked{-score, studentID[i]})
	}
	sort.Slice(all, func(a, b int) bool {
		if all[a].score != all[b].score {
			return all[a].score < all[b].score
		}
		return all[a].id < all[b].id
	})
	out := make([]int64, 0, k)
	for _, x := range all[:k] {
		out = append(out, x.id)
	}
	return out
}

var seed int64 = 2512

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func word(w int64) string {
	var digits []byte
	for v := w + 5; v > 0; v /= 5 {
		digits = append(digits, byte('a'+v%5))
	}
	for i, j := 0, len(digits)-1; i < j; i, j = i+1, j-1 {
		digits[i], digits[j] = digits[j], digits[i]
	}
	return string(digits)
}

type kase struct {
	positive, negative, report []string
	ids                        []int64
	k                          int64
}

func main() {
	cases := make([]kase, 0, 100)
	for c := int64(0); c < 100; c++ {
		p := nextRandom()%200 + 1
		q := nextRandom()%200 + 1
		var x kase
		for w := int64(0); w < p; w++ {
			x.positive = append(x.positive, word(w))
		}
		for w := p; w < p+q; w++ {
			x.negative = append(x.negative, word(w))
		}
		for r := 0; r < 1000; r++ {
			length := nextRandom()%20 + 1
			words := make([]string, 0, length)
			for i := int64(0); i < length; i++ {
				words = append(words, word(nextRandom()%600))
			}
			x.report = append(x.report, strings.Join(words, " "))
		}
		for r := int64(0); r < 1000; r++ {
			x.ids = append(x.ids, (r*7919+c)%1000003+1)
		}
		x.k = c*10 + 1
		cases = append(cases, x)
	}
	const passes = 50
	var check int64
	for p := int64(0); p < passes; p++ {
		for i := range cases {
			x := &cases[i]
			at := check % 1000
			kept := x.report[at]
			x.report[at] = x.report[(check/1000+p)%1000]
			for _, id := range topStudents(x.positive, x.negative, x.report, x.ids, x.k) {
				check = (check*31 + id + p) % 1000000007
			}
			x.report[at] = kept
		}
	}
	fmt.Printf("%d passes over 100 cases of 1000 reports: checksum %d\n", passes, check)
}
