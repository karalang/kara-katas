// LeetCode #2127: Maximum Employees to Be Invited to a Meeting -- the
// benchmark, the same algorithm as invitations.kara; the queue is a slice
// with a head index.
package main

import "fmt"

func maximumInvitations(favorite []int64) int64 {
	n := len(favorite)
	indegree := make([]int64, n)
	for _, f := range favorite {
		indegree[f]++
	}
	chain := make([]int64, n)
	queue := make([]int64, 0, n)
	for i := 0; i < n; i++ {
		if indegree[i] == 0 {
			queue = append(queue, int64(i))
		}
	}
	for head := 0; head < len(queue); head++ {
		i := queue[head]
		f := favorite[i]
		if chain[i]+1 > chain[f] {
			chain[f] = chain[i] + 1
		}
		indegree[f]--
		if indegree[f] == 0 {
			queue = append(queue, f)
		}
	}
	var largestCycle, pairs int64
	for i := 0; i < n; i++ {
		if indegree[i] == 0 {
			continue
		}
		var length int64
		j := int64(i)
		for indegree[j] != 0 {
			indegree[j] = 0
			length++
			j = favorite[j]
		}
		if length == 2 {
			pairs += 2 + chain[i] + chain[favorite[i]]
		} else if length > largestCycle {
			largestCycle = length
		}
	}
	if largestCycle > pairs {
		return largestCycle
	}
	return pairs
}

var seed int64 = 2127

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func big() int64 {
	hi := nextRandom()
	return hi*32768 + nextRandom()
}

func main() {
	const n = 100000
	tables := make([][]int64, 20)
	for t := range tables {
		favorite := make([]int64, n)
		for i := int64(0); i < n; i++ {
			if i < n/4 {
				favorite[i] = i ^ 1
			} else {
				favorite[i] = (i + 1 + big()%(n-1)) % n
			}
		}
		tables[t] = favorite
	}
	var total, check int64
	for round := int64(0); round < 10; round++ {
		for t := 0; t < 20; t++ {
			i := n/4 + big()%(n-n/4)
			tables[t][i] = (i + 1 + big()%(n-1)) % n
			invited := maximumInvitations(tables[t])
			total += invited
			check = (check*31 + invited + round) % 1000000007
		}
	}
	fmt.Printf("200 solves: %d invited, checksum %d\n", total, check)
}
