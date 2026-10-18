// LeetCode #736: Parse Lisp Expression -- tokens, recursion and a stack
// of scopes.
// Benchmark mirror of the Kara star arm: split the text into tokens,
// then evaluate by recursion, keeping the assignments of each open let
// in a scope of its own and looking a name up from the innermost.
package main

import (
	"fmt"
	"strconv"
)

func tokenize(expression string) []string {
	var tokens []string
	word := []byte{}
	for i := 0; i < len(expression); i++ {
		c := expression[i]
		if c == '(' || c == ')' || c == ' ' {
			if len(word) > 0 {
				tokens = append(tokens, string(word))
				word = []byte{}
			}
			if c != ' ' {
				tokens = append(tokens, string(c))
			}
		} else {
			word = append(word, c)
		}
	}
	if len(word) > 0 {
		tokens = append(tokens, string(word))
	}
	return tokens
}

func lookup(scopes []map[string]int64, name string) int64 {
	for i := len(scopes) - 1; i >= 0; i-- {
		if v, ok := scopes[i][name]; ok {
			return v
		}
	}
	return 0
}

func eval(tokens []string, pos *int, scopes *[]map[string]int64) int64 {
	t := tokens[*pos]
	*pos++
	if t != "(" {
		if t[0] == '-' || (t[0] >= '0' && t[0] <= '9') {
			n, _ := strconv.ParseInt(t, 10, 64)
			return n
		}
		return lookup(*scopes, t)
	}
	op := tokens[*pos]
	*pos++
	var value int64
	if op == "add" {
		a := eval(tokens, pos, scopes)
		b := eval(tokens, pos, scopes)
		value = a + b
	} else if op == "mult" {
		a := eval(tokens, pos, scopes)
		b := eval(tokens, pos, scopes)
		value = a * b
	} else {
		*scopes = append(*scopes, map[string]int64{})
		for {
			name := tokens[*pos]
			if name != "(" && tokens[*pos+1] != ")" {
				*pos++
				v := eval(tokens, pos, scopes)
				(*scopes)[len(*scopes)-1][name] = v
			} else {
				value = eval(tokens, pos, scopes)
				break
			}
		}
		*scopes = (*scopes)[:len(*scopes)-1]
	}
	*pos++
	return value
}

func evaluate(expression string) int64 {
	tokens := tokenize(expression)
	pos := 0
	var scopes []map[string]int64
	return eval(tokens, &pos, &scopes)
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func randomExpr(seed *int64, depth int64, names []string) string {
	kinds := int64(5)
	if depth == 0 {
		kinds = 2
	}
	kind := nextRandom(seed) % kinds
	if kind == 0 || (kind == 1 && len(names) == 0) {
		return fmt.Sprintf("%d", nextRandom(seed)%21-10)
	}
	if kind == 1 {
		return names[nextRandom(seed)%int64(len(names))]
	}
	if kind == 2 {
		a := randomExpr(seed, depth-1, names)
		b := randomExpr(seed, depth-1, names)
		return fmt.Sprintf("(add %s %s)", a, b)
	}
	if kind == 3 {
		a := randomExpr(seed, depth-1, names)
		return fmt.Sprintf("(mult %s %d)", a, nextRandom(seed)%5-2)
	}
	pool := []string{"x", "y", "z", "a1", "b2"}
	inner := append([]string{}, names...)
	text := "(let"
	count := 1 + nextRandom(seed)%3
	for k := int64(0); k < count; k++ {
		name := pool[nextRandom(seed)%5]
		v := randomExpr(seed, depth-1, inner)
		text = fmt.Sprintf("%s %s %s", text, name, v)
		found := false
		for _, n := range inner {
			if n == name {
				found = true
			}
		}
		if !found {
			inner = append(inner, name)
		}
	}
	body := randomExpr(seed, depth-1, inner)
	return fmt.Sprintf("%s %s)", text, body)
}

func main() {
	seed := int64(736)
	var exprs []string
	chars := 0
	for len(exprs) < 1000 {
		e := randomExpr(&seed, 8, nil)
		if len(e) >= 500 && len(e) <= 2000 {
			chars += len(e)
			exprs = append(exprs, e)
		}
	}
	var sum int64
	for r := 0; r < 40; r++ {
		for _, e := range exprs {
			v := evaluate(e)
			sum = (sum*31 + (v%1000000007+1000000007)%1000000007) % 1000000007
		}
	}
	fmt.Printf("40 rounds of 1000 expressions of %d characters in all: checksum %d\n", chars, sum)
}
