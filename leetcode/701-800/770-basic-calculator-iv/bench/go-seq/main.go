// LeetCode 770 — Basic Calculator IV: benchmark, the ★ arm in Go.
// Sixty-four random expressions of 40 leaves, built once; 20,000 rounds
// each simplify the next of them.
package main

import (
	"fmt"
	"sort"
	"strconv"
	"strings"
)

type poly map[string]int64

func tokenize(expression string) []string {
	tokens := []string{}
	word := ""
	for _, c := range expression {
		if (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z') || (c >= '0' && c <= '9') {
			word += string(c)
		} else {
			if word != "" {
				tokens = append(tokens, word)
				word = ""
			}
			if c != ' ' {
				tokens = append(tokens, string(c))
			}
		}
	}
	if word != "" {
		tokens = append(tokens, word)
	}
	return tokens
}

func namesOf(key string) []string {
	if key == "" {
		return nil
	}
	return strings.Split(key, "*")
}

func addInto(total poly, p poly, sign int64) {
	for key, coef := range p {
		total[key] += sign * coef
	}
}

func multiply(a, b poly) poly {
	product := poly{}
	for ka, ca := range a {
		for kb, cb := range b {
			names := append(namesOf(ka), namesOf(kb)...)
			sort.Strings(names)
			product[strings.Join(names, "*")] += ca * cb
		}
	}
	return product
}

type reader struct {
	tokens []string
	at     int
	known  map[string]int64
}

func (r *reader) peek() string {
	if r.at < len(r.tokens) {
		return r.tokens[r.at]
	}
	return ""
}

func (r *reader) expression() poly {
	total := r.term()
	for r.peek() == "+" || r.peek() == "-" {
		sign := int64(1)
		if r.peek() == "-" {
			sign = -1
		}
		r.at++
		addInto(total, r.term(), sign)
	}
	return total
}

func (r *reader) term() poly {
	product := r.factor()
	for r.peek() == "*" {
		r.at++
		product = multiply(product, r.factor())
	}
	return product
}

func (r *reader) factor() poly {
	token := r.peek()
	r.at++
	p := poly{}
	if token == "(" {
		p = r.expression()
		r.at++
	} else if token[0] >= '0' && token[0] <= '9' {
		v, _ := strconv.ParseInt(token, 10, 64)
		p[""] = v
	} else if value, ok := r.known[token]; ok {
		p[""] = value
	} else {
		p[token] = 1
	}
	return p
}

type term struct {
	degree int
	key    string
	coef   int64
}

func basicCalculatorIV(expression string, evalvars []string, evalints []int64) []string {
	known := map[string]int64{}
	for i, v := range evalvars {
		known[v] = evalints[i]
	}
	r := &reader{tokens: tokenize(expression), known: known}
	p := r.expression()
	terms := []term{}
	for k, c := range p {
		if c != 0 {
			terms = append(terms, term{-len(namesOf(k)), k, c})
		}
	}
	sort.Slice(terms, func(i, j int) bool {
		if terms[i].degree != terms[j].degree {
			return terms[i].degree < terms[j].degree
		}
		return terms[i].key < terms[j].key
	})
	answer := []string{}
	for _, t := range terms {
		if t.key == "" {
			answer = append(answer, fmt.Sprintf("%d", t.coef))
		} else {
			answer = append(answer, fmt.Sprintf("%d*%s", t.coef, t.key))
		}
	}
	return answer
}

var seed int64 = 770

func nextRandom() int64 {
	seed = (seed*1103515245 + 12345) % 2147483648
	return seed / 65536
}

func randomExpression(size int64) string {
	if size <= 1 {
		pick := nextRandom() % 9
		if pick < 3 {
			return fmt.Sprintf("%d", nextRandom()%10)
		}
		return []string{"a", "b", "c", "d", "x", "y"}[pick-3]
	}
	left := 1 + nextRandom()%(size-1)
	a := randomExpression(left)
	b := randomExpression(size - left)
	op := []string{" + ", " - ", " * "}[nextRandom()%3]
	if nextRandom()%3 == 0 {
		return "(" + a + op + b + ")"
	}
	return a + op + b
}

func main() {
	rounds := 20000
	pool := make([]string, 64)
	longest := 0
	for i := range pool {
		pool[i] = randomExpression(40)
		if len(pool[i]) > longest {
			longest = len(pool[i])
		}
	}
	terms := 0
	var check int64
	for round := 0; round < rounds; round++ {
		answer := basicCalculatorIV(pool[round%64], []string{"x"}, []int64{int64(round%7 - 3)})
		terms += len(answer)
		for _, t := range answer {
			for i := 0; i < len(t); i++ {
				check = (check*31 + int64(t[i])) % 1000000007
			}
		}
	}
	fmt.Printf("%d expressions of up to %d characters: %d terms in all, checksum %d\n", rounds, longest, terms, check)
}
