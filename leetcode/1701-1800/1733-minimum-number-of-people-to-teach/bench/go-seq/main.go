// LeetCode #1733: Minimum Number of People to Teach -- the bench
// (teach.kara): the stuck users gathered in a set, and the language most
// of them know.
package main

import "fmt"

func minimumTeachings(n int32, languages [][]int32, friendships [][]int32) int32 {
	known := make([]map[int32]struct{}, len(languages))
	for u, l := range languages {
		known[u] = make(map[int32]struct{}, len(l))
		for _, x := range l {
			known[u][x] = struct{}{}
		}
	}
	disjoint := func(a, b map[int32]struct{}) bool {
		for x := range a {
			if _, ok := b[x]; ok {
				return false
			}
		}
		return true
	}
	stuck := map[int]struct{}{}
	for _, f := range friendships {
		u, v := int(f[0])-1, int(f[1])-1
		if disjoint(known[u], known[v]) {
			stuck[u] = struct{}{}
			stuck[v] = struct{}{}
		}
	}
	speakers := make([]int32, n+1)
	for u := range stuck {
		for l := range known[u] {
			speakers[l]++
		}
	}
	best := speakers[0]
	for _, s := range speakers[1:] {
		best = max(best, s)
	}
	return int32(len(stuck)) - best
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func main() {
	count := 50
	var rounds int64 = 200
	var n int64 = 500
	users, pairs := 500, 500
	var seed int64 = 1733
	type problem struct{ languages, friendships [][]int32 }
	problems := make([]problem, 0, count)
	for c := 0; c < count; c++ {
		languages := make([][]int32, 0, users)
		for u := 0; u < users; u++ {
			k := int(nextRandom(&seed)%10 + 1)
			known := []int32{}
			for len(known) < k {
				l := int32(nextRandom(&seed)%n + 1)
				seen := false
				for _, x := range known {
					if x == l {
						seen = true
					}
				}
				if !seen {
					known = append(known, l)
				}
			}
			languages = append(languages, known)
		}
		friends := make([][]bool, users)
		for i := range friends {
			friends[i] = make([]bool, users)
		}
		friendships := [][]int32{}
		for len(friendships) < pairs {
			u := int(nextRandom(&seed) % int64(users))
			v := int(nextRandom(&seed) % int64(users))
			if u != v && !friends[u][v] {
				friends[u][v] = true
				friends[v][u] = true
				friendships = append(friendships, []int32{int32(u + 1), int32(v + 1)})
			}
		}
		problems = append(problems, problem{languages, friendships})
	}
	var sum, check int64
	for r := int64(0); r < rounds; r++ {
		for _, p := range problems {
			answer := int64(minimumTeachings(int32(n), p.languages, p.friendships))
			sum += answer
			check = (check*31 + answer + r) % 1000000007
		}
	}
	fmt.Printf("%d problems of %d users, %d languages and %d friendships, %d rounds: teachings sum to %d, checksum %d\n", count, users, n, pairs, rounds, sum, check)
}
