// LeetCode 285 bench mirror — Go. Same arena, descent and Option-folding sink.
package main

import "fmt"

const N = 300000
const Queries = 2000000

var key, lft, rgt []int64
var cnt int64

func insert(k int64) {
	if cnt == 0 {
		key[0], lft[0], rgt[0], cnt = k, -1, -1, 1
		return
	}
	cur := int64(0)
	for {
		if k < key[cur] {
			if lft[cur] < 0 {
				key[cnt], lft[cnt], rgt[cnt] = k, -1, -1
				lft[cur] = cnt
				cnt++
				return
			}
			cur = lft[cur]
		} else {
			if rgt[cur] < 0 {
				key[cnt], lft[cnt], rgt[cnt] = k, -1, -1
				rgt[cur] = cnt
				cnt++
				return
			}
			cur = rgt[cur]
		}
	}
}

func successor(target int64) (int64, bool) {
	if cnt == 0 {
		return 0, false
	}
	cur := int64(0)
	var best int64
	have := false
	for cur >= 0 {
		if key[cur] > target {
			best, have = key[cur], true
			cur = lft[cur]
		} else {
			cur = rgt[cur]
		}
	}
	return best, have
}

func main() {
	key = make([]int64, N)
	lft = make([]int64, N)
	rgt = make([]int64, N)
	seed := int64(20260825)
	for i := 0; i < N; i++ {
		seed = (seed*1103515245 + 12345) % 2147483648
		insert(seed % 1000000)
	}
	var sink, found int64
	for q := 0; q < Queries; q++ {
		seed = (seed*1103515245 + 12345) % 2147483648
		v, have := successor(seed % 1000000)
		if have {
			found++
		} else {
			v = -1
		}
		sink = (sink*31 + v) % 1000000007
	}
	fmt.Println(sink, found)
}
