// LeetCode 811 -- Subdomain Visit Count: the bench, with the ★ arm's map
// from domain to visits.
package main

import (
	"fmt"
	"strconv"
	"strings"
)

var seed int64 = 811

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func subdomainVisits(cpdomains []string) []string {
	counts := map[string]int64{}
	for _, entry := range cpdomains {
		space := strings.IndexByte(entry, ' ')
		n, _ := strconv.ParseInt(entry[:space], 10, 64)
		domain := entry[space+1:]
		for {
			counts[domain] += n
			dot := strings.IndexByte(domain, '.')
			if dot < 0 {
				break
			}
			domain = domain[dot+1:]
		}
	}
	out := make([]string, 0, len(counts))
	for domain, total := range counts {
		out = append(out, fmt.Sprintf("%d %s", total, domain))
	}
	return out
}

var tops = []string{"com", "org", "net", "io"}
var middles = []string{"leetcode", "google", "yahoo", "wiki", "kara"}
var lefts = []string{"mail", "discuss", "www", "api", "m", "docs"}

// A domain of 2 or 3 parts: a left part one time in three, then a middle
// part and a top part.
func randomDomain() string {
	top := tops[nextRandom()%4]
	middle := middles[nextRandom()%5]
	if nextRandom()%3 == 0 {
		return middle + "." + top
	}
	return lefts[nextRandom()%6] + "." + middle + "." + top
}

// 64 lists of 100 entries are made once. Each round writes a new count
// into one entry of the next list and counts that list's visits; the
// answer's lines, in whatever order they come, are folded into a sum.
func main() {
	lists := make([][]string, 64)
	domains := make([][]string, 64)
	for k := 0; k < 64; k++ {
		for j := 0; j < 100; j++ {
			d := randomDomain()
			lists[k] = append(lists[k], fmt.Sprintf("%d %s", 1+nextRandom()%10000, d))
			domains[k] = append(domains[k], d)
		}
	}
	var rounds int64 = 100000
	var lines, check int64
	for r := int64(0); r < rounds; r++ {
		k := r % 64
		i := r / 64 % 100
		lists[k][i] = fmt.Sprintf("%d %s", 1+nextRandom()%10000, domains[k][i])
		out := subdomainVisits(lists[k])
		var sum int64
		for _, line := range out {
			space := strings.IndexByte(line, ' ')
			n, _ := strconv.ParseInt(line[:space], 10, 64)
			sum += n*7 + int64(len(line))
		}
		lines += int64(len(out))
		check = (check*131 + sum) % 1000000007
	}
	fmt.Printf("%d rounds of 100 entries: %d lines, checksum %d\n", rounds, lines, check)
}
