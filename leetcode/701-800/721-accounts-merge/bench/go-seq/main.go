// LeetCode #721: Accounts Merge -- union-find over the emails.
// Benchmark mirror of the Kara star arm: every email numbered the first
// time it is seen, each account's emails joined in a union-find, then the
// emails gathered by their root, each group sorted under its name.
package main

import (
	"fmt"
	"sort"
)

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func find(parent []int, x int) int {
	root := x
	for parent[root] != root {
		root = parent[root]
	}
	at := x
	for parent[at] != root {
		up := parent[at]
		parent[at] = root
		at = up
	}
	return root
}

func accountsMerge(accounts [][]string) [][]string {
	id := map[string]int{}
	var emails, owner []string
	var parent []int
	for _, account := range accounts {
		first := -1
		for _, email := range account[1:] {
			if _, ok := id[email]; !ok {
				id[email] = len(emails)
				parent = append(parent, len(emails))
				emails = append(emails, email)
				owner = append(owner, account[0])
			}
			e := id[email]
			if first < 0 {
				first = e
			} else {
				a, b := find(parent, first), find(parent, e)
				if a != b {
					parent[b] = a
				}
			}
		}
	}
	groups := map[int][]string{}
	for e := range emails {
		root := find(parent, e)
		groups[root] = append(groups[root], emails[e])
	}
	var merged [][]string
	for root, group := range groups {
		sorted := append([]string(nil), group...)
		sort.Strings(sorted)
		merged = append(merged, append([]string{owner[root]}, sorted...))
	}
	return merged
}

func main() {
	names := []string{"Ada", "Bo", "Cy", "Di"}
	seed := int64(721)
	var lists [][][]string
	for l := 0; l < 20; l++ {
		var accounts [][]string
		for a := 0; a < 1000; a++ {
			who := nextRandom(&seed) % 4
			account := []string{names[who]}
			n := 1 + nextRandom(&seed)%4
			for k := int64(0); k < n; k++ {
				e := 4*(nextRandom(&seed)%2000) + who
				account = append(account, fmt.Sprintf("u%d@m.co", e))
			}
			accounts = append(accounts, account)
		}
		lists = append(lists, accounts)
	}
	sum := 0
	for round := 0; round < 50; round++ {
		for d := 0; d < 20; d++ {
			i := (round*7919 + d*104729) % 1000
			j := (i + 1) % 1000
			for lists[d][j][0] != lists[d][i][0] {
				j = (j + 1) % 1000
			}
			last := len(lists[d][i]) - 1
			lists[d][i][last] = lists[d][j][1]
			merged := accountsMerge(lists[d])
			sum += len(merged)
			for _, person := range merged {
				sum += len(person[1])
			}
		}
	}
	fmt.Printf("50 rounds of 20 lists of 1000 accounts: sum %d\n", sum)
}
