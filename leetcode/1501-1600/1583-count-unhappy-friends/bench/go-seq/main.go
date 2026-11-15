// LeetCode #1583 bench: the same table of ranks, in Go.
package main

import "fmt"

func unhappyFriends(n int64, preferences, pairs [][]int64) int64 {
	rank := make([][]int64, n)
	for x := int64(0); x < n; x++ {
		rank[x] = make([]int64, n)
		for r, f := range preferences[x] {
			rank[x][f] = int64(r)
		}
	}
	partner := make([]int64, n)
	for _, p := range pairs {
		partner[p[0]] = p[1]
		partner[p[1]] = p[0]
	}
	var unhappy int64
	for x := int64(0); x < n; x++ {
		y := partner[x]
		for _, u := range preferences[x][:rank[x][y]] {
			if rank[u][x] < rank[u][partner[u]] {
				unhappy++
				break
			}
		}
	}
	return unhappy
}

var seed int64 = 1583

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func mix(check, x int64) int64 { return (check*31 + x + 1) % 1000000007 }

func shuffled(n int64) []int64 {
	v := make([]int64, n)
	for i := range v {
		v[i] = int64(i)
	}
	for i := n - 1; i > 0; i-- {
		j := nextRandom() % (i + 1)
		v[i], v[j] = v[j], v[i]
	}
	return v
}

func main() {
	const n = 500
	type problem struct{ preferences, pairs [][]int64 }
	problems := make([]problem, 0, 40)
	for p := 0; p < 40; p++ {
		preferences := make([][]int64, 0, n)
		for x := int64(0); x < n; x++ {
			order := shuffled(n)
			list := make([]int64, 0)
			for _, f := range order {
				if f != x {
					list = append(list, f)
				}
			}
			preferences = append(preferences, list)
		}
		line := shuffled(n)
		pairs := make([][]int64, 0, n/2)
		for k := 0; k < n/2; k++ {
			pairs = append(pairs, []int64{line[2*k], line[2*k+1]})
		}
		problems = append(problems, problem{preferences, pairs})
	}
	var check, total int64
	for _, pr := range problems {
		unhappy := unhappyFriends(n, pr.preferences, pr.pairs)
		total += unhappy
		check = mix(check, unhappy)
	}
	fmt.Printf("40 problems of 500 friends: unhappy %d, checksum %d\n", total, check)
}
