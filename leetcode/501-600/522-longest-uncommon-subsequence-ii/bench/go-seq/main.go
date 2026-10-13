// Benchmark for #522: Go mirror of the ★ arm (longest first); see
// ../find_lus_length.kara.
package main

import (
	"fmt"
	"sort"
	"strings"
)

func isSubsequence(small, big string) bool {
	s := []rune(small)
	i := 0
	for _, c := range big {
		if i < len(s) && s[i] == c {
			i++
		}
	}
	return i == len(s)
}

func findLUSLength(strs []string) int64 {
	order := make([]int, len(strs))
	for i := range order {
		order[i] = i
	}
	sort.SliceStable(order, func(a, b int) bool { return len(strs[order[a]]) > len(strs[order[b]]) })
	for _, i := range order {
		uncommon := true
		for j := range strs {
			if j != i && isSubsequence(strs[i], strs[j]) {
				uncommon = false
				break
			}
		}
		if uncommon {
			return int64(len(strs[i]))
		}
	}
	return -1
}

var seed int64 = 522

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomWord(n, letters int64) string {
	var b strings.Builder
	for i := int64(0); i < n; i++ {
		b.WriteByte(byte(97 + nextRandom()%letters))
	}
	return b.String()
}

func main() {
	// 2,000 random lists of 50 words of 1 to 10 letters from 1 to 3
	// letters, one word in three a copy of an earlier one, made once;
	// then every list solved in each of 100 rounds.
	lists := make([][]string, 0, 2000)
	for l := 0; l < 2000; l++ {
		letters := 1 + nextRandom()%3
		strs := make([]string, 0, 50)
		for k := int64(0); k < 50; k++ {
			if k > 0 && nextRandom()%3 == 0 {
				strs = append(strs, strings.Clone(strs[nextRandom()%k]))
			} else {
				strs = append(strs, randomWord(1+nextRandom()%10, letters))
			}
		}
		lists = append(lists, strs)
	}
	var total, checksum int64
	for round := int64(0); round < 100; round++ {
		for l, strs := range lists {
			answer := findLUSLength(strs)
			total += answer
			checksum = (checksum + (round+1)*(int64(l)+1)*(answer+2)) % 1000000007
		}
	}
	fmt.Printf("2000 lists of 50 words, 100 rounds: total %d, checksum %d\n", total, checksum)
}
