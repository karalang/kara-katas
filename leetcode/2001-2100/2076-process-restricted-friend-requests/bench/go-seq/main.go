// LeetCode #2076: Process Restricted Friend Requests -- Go mirror of the ★
// arm's benchmark (friends.kara): 400 problems of 1000 people, 1000
// restrictions and 1000 requests; a union-find of parents in a slice,
// found with path halving, every restriction tried against a request
// between two groups.
package main

import "fmt"

var seed int64 = 2076

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomPairs(n, count int64) [][]int64 {
	pairs := make([][]int64, 0, count)
	for i := int64(0); i < count; i++ {
		a := nextRandom() % n
		b := (a + 1 + nextRandom()%(n-1)) % n
		pairs = append(pairs, []int64{a, b})
	}
	return pairs
}

func find(parent []int64, x int64) int64 {
	for parent[x] != x {
		parent[x] = parent[parent[x]]
		x = parent[x]
	}
	return x
}

func friendRequests(n int64, restrictions, requests [][]int64) []bool {
	parent := make([]int64, n)
	for i := range parent {
		parent[i] = int64(i)
	}
	answers := make([]bool, 0, len(requests))
	for _, request := range requests {
		a := find(parent, request[0])
		b := find(parent, request[1])
		allowed := true
		if a != b {
			for _, r := range restrictions {
				x := find(parent, r[0])
				y := find(parent, r[1])
				if (x == a && y == b) || (x == b && y == a) {
					allowed = false
					break
				}
			}
			if allowed {
				parent[a] = b
			}
		}
		answers = append(answers, allowed)
	}
	return answers
}

func main() {
	var total, check int64
	for t := 0; t < 400; t++ {
		restrictions := randomPairs(1000, 1000)
		requests := randomPairs(1000, 1000)
		for _, a := range friendRequests(1000, restrictions, requests) {
			var bit int64
			if a {
				bit = 1
			}
			total += bit
			check = (check*3 + bit + 1) % 1000000007
		}
	}
	fmt.Printf("400 problems: %d accepted, checksum %d\n", total, check)
}
