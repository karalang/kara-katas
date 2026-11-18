// LeetCode #2306: Naming a Company -- the bench, the ★ arm in Go. Group
// the suffixes by first letter, and for each pair of letters multiply the
// suffixes each group does not share with the other, twice.
package main

import "fmt"

func distinctNames(ideas []string) int64 {
	groups := make([]map[string]struct{}, 26)
	for a := range groups {
		groups[a] = make(map[string]struct{})
	}
	for _, idea := range ideas {
		groups[idea[0]-'a'][idea[1:]] = struct{}{}
	}
	var names int64
	for a := 0; a < 26; a++ {
		for b := a + 1; b < 26; b++ {
			var shared int64
			for suffix := range groups[a] {
				if _, ok := groups[b][suffix]; ok {
					shared++
				}
			}
			names += 2 * (int64(len(groups[a])) - shared) * (int64(len(groups[b])) - shared)
		}
	}
	return names
}

var seed int64 = 2306

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	letters := "abcdefghijklmnopqrstuvwxyz"
	lists := make([][]string, 10)
	for a := range lists {
		seen := make(map[string]struct{})
		ideas := make([]string, 0, 50000)
		for len(ideas) < 50000 {
			idea := []byte{letters[nextRandom()%26]}
			more := nextRandom() % 7
			for m := int64(0); m < more; m++ {
				idea = append(idea, letters[nextRandom()%6])
			}
			s := string(idea)
			if _, ok := seen[s]; !ok {
				seen[s] = struct{}{}
				ideas = append(ideas, s)
			}
		}
		lists[a] = ideas
	}
	var check int64
	for p := 0; p < 4; p++ {
		for _, ideas := range lists {
			check = (check*31 + distinctNames(ideas)) % 1000000007
		}
	}
	fmt.Printf("4 passes over 10 lists of 5 * 10^4 ideas: checksum %d\n", check)
}
