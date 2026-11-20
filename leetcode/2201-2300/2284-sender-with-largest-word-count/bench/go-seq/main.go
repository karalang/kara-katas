// LeetCode #2284: Sender With Largest Word Count -- the bench, the ★
// arm's Go twin. A map of totals, then the largest by total and name.
package main

import (
	"fmt"
	"strings"
)

func largestWordCount(messages, senders []string) string {
	totals := map[string]int64{}
	for i, message := range messages {
		totals[senders[i]] += int64(len(strings.Split(message, " ")))
	}
	best := ""
	var most int64
	for sender, total := range totals {
		if total > most || (total == most && sender > best) {
			best = sender
			most = total
		}
	}
	return best
}

// ---- bench harness ---------------------------------------------------------

var seed int64 = 2284

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func word(n int64) string {
	b := make([]byte, n)
	for i := range b {
		b[i] = byte('a' + nextRandom()%26)
	}
	return string(b)
}

func main() {
	pool := make([]string, 0, 40)
	for i := 0; i < 40; i++ {
		n := nextRandom()%10 + 1
		pool = append(pool, word(n))
	}
	type kase struct{ messages, senders []string }
	cases := make([]kase, 0, 1000)
	for c := 0; c < 1000; c++ {
		first := nextRandom() % 20
		messages := make([]string, 0, 100)
		senders := make([]string, 0, 100)
		for m := 0; m < 100; m++ {
			senders = append(senders, pool[first+nextRandom()%20])
			w := nextRandom()%8 + 1
			var sb strings.Builder
			for j := int64(0); j < w; j++ {
				if j > 0 {
					sb.WriteByte(' ')
				}
				n := nextRandom()%5 + 1
				sb.WriteString(word(n))
			}
			messages = append(messages, sb.String())
		}
		cases = append(cases, kase{messages, senders})
	}
	var check int64
	for p := 0; p < 20; p++ {
		for _, k := range cases {
			best := largestWordCount(k.messages, k.senders)
			var sum int64
			for i := 0; i < len(best); i++ {
				sum += int64(best[i])
			}
			check = (check*31 + sum) % 1000000007
		}
	}
	fmt.Printf("20 passes over 1000 cases of 100 messages: checksum %d\n", check)
}
