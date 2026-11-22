// LeetCode #2773: Height of Special Binary Tree -- the bench in Go: the ★
// arm over 20 random trees of 10^4 nodes, all drawn first, then each
// answered 200 times.
package main

import "fmt"

func depth(u int64, left, right []int64) int64 {
	var best int64
	l := left[u]
	if l >= 0 && right[l] != u {
		best = max(best, depth(l, left, right)+1)
	}
	r := right[u]
	if r >= 0 && left[r] != u {
		best = max(best, depth(r, left, right)+1)
	}
	return best
}

var seed int64 = 2773

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func joined(left, right []int64, root int64) ([]int64, []int64) {
	leaves := []int64{}
	stack := []int64{root}
	for len(stack) > 0 {
		u := stack[len(stack)-1]
		stack = stack[:len(stack)-1]
		if left[u] < 0 && right[u] < 0 {
			leaves = append(leaves, u)
		}
		if right[u] >= 0 {
			stack = append(stack, right[u])
		}
		if left[u] >= 0 {
			stack = append(stack, left[u])
		}
	}
	l := append([]int64{}, left...)
	r := append([]int64{}, right...)
	k := len(leaves)
	for i := 0; i < k; i++ {
		r[leaves[i]] = leaves[(i+1)%k]
		l[leaves[i]] = leaves[(i+k-1)%k]
	}
	return l, r
}

func grown(n, reach int64) ([]int64, []int64) {
	left := make([]int64, n)
	right := make([]int64, n)
	for i := range left {
		left[i] = -1
		right[i] = -1
	}
	for k := int64(1); k < n; k++ {
		p := k - 1 - nextRandom()%min(reach, k)
		for left[p] >= 0 && right[p] >= 0 {
			p = nextRandom() % k
		}
		var goLeft bool
		if left[p] >= 0 {
			goLeft = false
		} else if right[p] >= 0 {
			goLeft = true
		} else {
			goLeft = nextRandom()%2 == 0
		}
		if goLeft {
			left[p] = k
		} else {
			right[p] = k
		}
	}
	return joined(left, right, 0)
}

func main() {
	count := 20
	rounds := 200
	lefts := make([][]int64, count)
	rights := make([][]int64, count)
	for c := 0; c < count; c++ {
		reach := nextRandom()%50 + 1
		lefts[c], rights[c] = grown(10000, reach)
	}
	var total, check int64
	for r := int64(0); r < int64(rounds); r++ {
		for c := 0; c < count; c++ {
			h := depth(0, lefts[c], rights[c])
			total += h
			check = (check*31 + h + r) % 1000000007
		}
	}
	fmt.Printf("%d trees of 10^4, %d rounds: heights sum to %d, checksum %d\n", count, rounds, total, check)
}
