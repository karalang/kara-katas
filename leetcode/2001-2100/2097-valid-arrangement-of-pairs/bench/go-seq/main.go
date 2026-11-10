// LeetCode #2097: Valid Arrangement of Pairs -- Go mirror of the ★ arm's
// benchmark (arrangement.kara): the same 100 random walks of 100000 pairs,
// each arranged by Hierholzer's walk on an explicit stack, with Go's map.
package main

import "fmt"

type pair struct{ a, b int64 }

func validArrangement(pairs []pair) []pair {
	next := map[int64][]int64{}
	balance := map[int64]int64{}
	for _, p := range pairs {
		next[p.a] = append(next[p.a], p.b)
		if _, ok := next[p.b]; !ok {
			next[p.b] = nil
		}
		balance[p.a]++
		balance[p.b]--
	}
	start := pairs[0].a
	for v, d := range balance {
		if d == 1 {
			start = v
		}
	}
	stack := []int64{start}
	path := []int64{}
	for len(stack) > 0 {
		top := stack[len(stack)-1]
		outs := next[top]
		if len(outs) > 0 {
			v := outs[len(outs)-1]
			next[top] = outs[:len(outs)-1]
			stack = append(stack, v)
		} else {
			path = append(path, top)
			stack = stack[:len(stack)-1]
		}
	}
	out := make([]pair, 0, len(path))
	for i := len(path) - 1; i > 0; i-- {
		out = append(out, pair{path[i], path[i-1]})
	}
	return out
}

var seed int64 = 2097

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func wideRandom() int64 {
	hi := nextRandom()
	return hi*32768 + nextRandom()
}

func step(at int64, values []int64, used map[pair]bool) (int64, bool) {
	k := int64(len(values))
	from := nextRandom() % k
	for j := int64(0); j < k; j++ {
		v := values[(from+j)%k]
		if v != at && !used[pair{at, v}] {
			return v, true
		}
	}
	return 0, false
}

func randomPairs(m, k int64, closed bool) []pair {
	values := make([]int64, k)
	for i := range values {
		values[i] = wideRandom() % 1000000001
	}
	first := values[nextRandom()%k]
	walk := []int64{first}
	used := map[pair]bool{}
	at := first
	for int64(len(walk)) <= m+50 {
		if closed && int64(len(walk)) >= m && at != first && !used[pair{at, first}] {
			walk = append(walk, first)
			break
		}
		if !closed && int64(len(walk)) > m {
			break
		}
		v, ok := step(at, values, used)
		if !ok {
			break
		}
		used[pair{at, v}] = true
		walk = append(walk, v)
		at = v
	}
	pairs := make([]pair, 0, len(walk))
	for i := 1; i < len(walk); i++ {
		pairs = append(pairs, pair{walk[i-1], walk[i]})
	}
	for i := len(pairs) - 1; i > 0; i-- {
		j := wideRandom() % int64(i+1)
		pairs[i], pairs[j] = pairs[j], pairs[i]
	}
	return pairs
}

func main() {
	total := 0
	var check int64
	for round := 0; round < 100; round++ {
		pairs := randomPairs(100000, 1000, round%2 == 0)
		got := validArrangement(pairs)
		total += len(got)
		for _, p := range got {
			check = (check*31 + p.a) % 1000000007
		}
		check = (check*31 + got[len(got)-1].b) % 1000000007
	}
	fmt.Printf("100 rounds: %d pairs, checksum %d\n", total, check)
}
