// Benchmark for #468: mirror of validate_ip.kara (the ★ arm: split on the
// separator) on the same workload. strings.SplitSeq yields the parts
// lazily, as the Kāra arm's split does.
package main

import (
	"fmt"
	"strings"
)

func isDigit(c rune) bool {
	return c >= '0' && c <= '9'
}

func isHex(c rune) bool {
	return isDigit(c) || (c >= 'a' && c <= 'f') || (c >= 'A' && c <= 'F')
}

func ipv4Part(part string) bool {
	if len(part) == 0 || len(part) > 3 {
		return false
	}
	value := 0
	for _, c := range part {
		if !isDigit(c) {
			return false
		}
		value = value*10 + int(c-48)
	}
	if len(part) > 1 && strings.HasPrefix(part, "0") {
		return false
	}
	return value <= 255
}

func ipv6Group(group string) bool {
	if len(group) == 0 || len(group) > 4 {
		return false
	}
	for _, c := range group {
		if !isHex(c) {
			return false
		}
	}
	return true
}

func validIPAddress(queryIP string) string {
	if strings.Contains(queryIP, ".") {
		parts := 0
		for part := range strings.SplitSeq(queryIP, ".") {
			if !ipv4Part(part) {
				return "Neither"
			}
			parts++
		}
		if parts == 4 {
			return "IPv4"
		}
	} else if strings.Contains(queryIP, ":") {
		groups := 0
		for group := range strings.SplitSeq(queryIP, ":") {
			if !ipv6Group(group) {
				return "Neither"
			}
			groups++
		}
		if groups == 8 {
			return "IPv6"
		}
	}
	return "Neither"
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func pick(alphabet string, seed *int64) byte {
	return alphabet[nextRandom(seed)%int64(len(alphabet))]
}

func randomQuery(seed *int64) string {
	kind := nextRandom(seed) % 5
	fault := nextRandom(seed) % 8
	var s strings.Builder
	if kind < 2 {
		parts := int64(4)
		if fault == 4 {
			parts = []int64{3, 5}[nextRandom(seed)%2]
		}
		at := nextRandom(seed) % parts
		for p := int64(0); p < parts; p++ {
			if p > 0 {
				s.WriteByte('.')
			}
			value := nextRandom(seed) % 256
			if p == at && fault == 5 {
				s.WriteByte('0')
			}
			if p == at && fault == 6 {
				value = 256 + nextRandom(seed)%744
			}
			if p == at && fault == 7 {
				if nextRandom(seed)%2 == 0 {
					s.WriteByte(pick("aeFx", seed))
				}
				continue
			}
			fmt.Fprintf(&s, "%d", value)
		}
	} else if kind < 4 {
		groups := int64(8)
		if fault == 4 {
			groups = []int64{7, 9}[nextRandom(seed)%2]
		}
		at := nextRandom(seed) % groups
		for g := int64(0); g < groups; g++ {
			if g > 0 {
				s.WriteByte(':')
			}
			if g == at && fault == 6 {
				continue
			}
			var length int64
			if g == at && fault == 5 {
				length = 5
			} else {
				length = 1 + nextRandom(seed)%4
			}
			bad := int64(-1)
			if g == at && fault == 7 {
				bad = nextRandom(seed) % length
			}
			for i := int64(0); i < length; i++ {
				if i == bad {
					s.WriteByte(pick("gGxz", seed))
				} else {
					s.WriteByte(pick("0123456789abcdefABCDEF", seed))
				}
			}
		}
	} else {
		length := 1 + nextRandom(seed)%15
		for i := int64(0); i < length; i++ {
			s.WriteByte(pick("0123456789aF.:g", seed))
		}
	}
	return s.String()
}

func main() {
	const count = 100000
	const rounds = 20
	seed := int64(468)
	queries := make([]string, 0, count)
	for i := 0; i < count; i++ {
		queries = append(queries, randomQuery(&seed))
	}
	var ipv4, ipv6, checksum int64
	for r := 0; r < rounds; r++ {
		for i := 0; i < count; i++ {
			answer := validIPAddress(queries[i])
			var code int64
			if answer == "IPv4" {
				ipv4++
				code = 1
			} else if answer == "IPv6" {
				ipv6++
				code = 2
			} else {
				code = 3
			}
			checksum = (checksum*7 + code + int64(i)) % 1000000007
		}
	}
	fmt.Printf("%d rounds of %d queries: %d IPv4, %d IPv6, checksum %d\n", rounds, count, ipv4, ipv6, checksum)
}
