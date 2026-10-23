// LeetCode #929: Unique Email Addresses -- bench: one walk per address and
// a set. Mirrors num_unique_emails.kara.
package main

import "fmt"

func numUniqueEmails(emails []string) int64 {
	seen := make(map[string]struct{})
	for _, e := range emails {
		out := make([]byte, 0, len(e))
		domain, tagged := false, false
		for i := 0; i < len(e); i++ {
			c := e[i]
			if domain {
				out = append(out, c)
			} else if c == '@' {
				domain = true
				out = append(out, c)
			} else if c == '+' {
				tagged = true
			} else if c != '.' && !tagged {
				out = append(out, c)
			}
		}
		seen[string(out)] = struct{}{}
	}
	return int64(len(seen))
}

var seed int64 = 929

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const rounds, count = 300, 100
	domains := []string{"@leetcode.com", "@lee.tcode.com", "@example.com", "@mail.example.com", "@a+b.com", "@ab.com", "@kara.dev.com", "@x.com"}
	// count lists of 100 addresses, built once: a local name of 2 to 7
	// letters from "ab" with a dot before about one in four, a tag after a
	// '+' on half of them, and one of eight domains
	lists := make([][]string, count)
	for g := range lists {
		emails := make([]string, 100)
		for t := range emails {
			b := []byte{}
			letters := 2 + nextRandom()%6
			for i := int64(0); i < letters; i++ {
				if nextRandom()%4 == 0 {
					b = append(b, '.')
				}
				b = append(b, byte('a'+nextRandom()%2))
			}
			if nextRandom()%2 == 0 {
				b = append(b, '+')
				tag := nextRandom() % 10
				for i := int64(0); i < tag; i++ {
					b = append(b, byte('a'+nextRandom()%26))
				}
			}
			emails[t] = string(b) + domains[nextRandom()%8]
		}
		lists[g] = emails
	}
	var total, check int64
	for r := 0; r < rounds; r++ {
		// each round visits every list, starting from a different one
		for i := 0; i < count; i++ {
			a := numUniqueEmails(lists[(r+i)%count])
			total += a
			check = (check*1000003 + a) % 1000000007
		}
	}
	fmt.Printf("%d rounds over %d lists of 100 addresses: answers summing to %d, checksum %d\n", rounds, count, total, check)
}
