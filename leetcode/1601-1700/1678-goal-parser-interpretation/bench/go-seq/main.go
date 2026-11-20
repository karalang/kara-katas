// LeetCode #1678: Goal Parser Interpretation -- the bench's Go mirror: the
// ★ arm on 100000 random commands of up to 100 characters, all drawn
// first, each interpreted 20 times.

package main

import (
	"fmt"
	"strings"
)

func interpret(command string) string {
	var out strings.Builder
	out.Grow(len(command))
	i := 0
	for i < len(command) {
		if command[i] == 'G' {
			out.WriteByte('G')
			i++
		} else if command[i+1] == ')' {
			out.WriteByte('o')
			i += 2
		} else {
			out.WriteString("al")
			i += 4
		}
	}
	return out.String()
}

// ---- the harness ----------------------------------------------------------

var seed int64 = 1678

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func main() {
	const count = 100000
	const rounds = 20
	tokens := []string{"G", "()", "(al)"}
	commands := make([]string, 0, count)
	for c := 0; c < count; c++ {
		var command strings.Builder
		length := int(nextRandom()%100 + 1)
		for {
			token := tokens[nextRandom()%3]
			if command.Len()+len(token) > length {
				break
			}
			command.WriteString(token)
		}
		if command.Len() == 0 {
			command.WriteByte('G')
		}
		commands = append(commands, command.String())
	}
	var total, check int64
	for r := int64(0); r < rounds; r++ {
		for _, command := range commands {
			answer := interpret(command)
			n := int64(len(answer))
			total += n
			check = (check*31 + n + int64(answer[len(answer)-1]) + r) % 1000000007
		}
	}
	fmt.Printf("%d commands, %d rounds: %d letters, checksum %d\n", count, rounds, total, check)
}
