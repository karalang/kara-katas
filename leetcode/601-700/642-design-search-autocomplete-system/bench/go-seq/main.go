// Benchmark for #642: mirror of autocomplete.kara (the ★ arm: a trie
// searched below the prefix) on the same workload.
package main

import (
	"fmt"
	"sort"
	"strings"
)

type Node struct {
	children [27]int64
	count    int64
}

type Found struct {
	count int64
	text  string
}

type AutocompleteSystem struct {
	nodes []Node
	typed string
	at    int64
}

func branch(c byte) int64 {
	if c == ' ' {
		return 26
	}
	return int64(c - 'a')
}

func letter(b int64) string {
	if b == 26 {
		return " "
	}
	return string(rune('a' + b))
}

func newNode() Node {
	var n Node
	for b := range n.children {
		n.children[b] = -1
	}
	return n
}

func gather(nodes []Node, node int64, path string, found *[]Found) {
	if nodes[node].count > 0 {
		*found = append(*found, Found{nodes[node].count, strings.Clone(path)})
	}
	for b := int64(0); b < 27; b++ {
		child := nodes[node].children[b]
		if child != -1 {
			gather(nodes, child, path+letter(b), found)
		}
	}
}

func newSystem(sentences []string, times []int64) *AutocompleteSystem {
	s := &AutocompleteSystem{nodes: []Node{newNode()}}
	for i := range sentences {
		s.add(sentences[i], times[i])
	}
	return s
}

func (s *AutocompleteSystem) add(sentence string, times int64) {
	node := int64(0)
	for i := 0; i < len(sentence); i++ {
		b := branch(sentence[i])
		if s.nodes[node].children[b] == -1 {
			s.nodes = append(s.nodes, newNode())
			s.nodes[node].children[b] = int64(len(s.nodes) - 1)
		}
		node = s.nodes[node].children[b]
	}
	s.nodes[node].count += times
}

func (s *AutocompleteSystem) input(c byte) []string {
	if c == '#' {
		s.add(s.typed, 1)
		s.typed = ""
		s.at = 0
		return nil
	}
	s.typed += string(c)
	if s.at != -1 {
		s.at = s.nodes[s.at].children[branch(c)]
	}
	if s.at == -1 {
		return nil
	}
	found := []Found{}
	gather(s.nodes, s.at, s.typed, &found)
	sort.Slice(found, func(i, j int) bool {
		if found[i].count != found[j].count {
			return found[i].count > found[j].count
		}
		return found[i].text < found[j].text
	})
	top := []string{}
	for i := 0; i < len(found) && i < 3; i++ {
		top = append(top, found[i].text)
	}
	return top
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func randomSentence(most int64, seed *int64) string {
	length := 1 + nextRandom(seed)%most
	var b strings.Builder
	for i := int64(0); i < length; i++ {
		b.WriteByte("abc "[nextRandom(seed)%4])
	}
	return b.String()
}

type History struct {
	sentences []string
	times     []int64
	typing    string
}

func main() {
	seed := int64(642)
	histories := []History{}
	for h := 0; h < 10; h++ {
		sentences := []string{}
		times := []int64{}
		for len(sentences) < 100 {
			s := randomSentence(100, &seed)
			seen := false
			for _, t := range sentences {
				if t == s {
					seen = true
				}
			}
			if !seen {
				sentences = append(sentences, s)
				times = append(times, 1+nextRandom(&seed)%100)
			}
		}
		var typing strings.Builder
		for typing.Len() < 5000 {
			if nextRandom(&seed)%2 == 0 {
				typing.WriteString(sentences[nextRandom(&seed)%100])
			} else {
				typing.WriteString(randomSentence(100, &seed))
			}
			typing.WriteByte('#')
		}
		histories = append(histories, History{sentences, times, typing.String()[:5000]})
	}
	rounds := 40
	names := 0
	checksum := int64(0)
	for r := 0; r < rounds; r++ {
		h := histories[r%10]
		s := newSystem(h.sentences, h.times)
		for i := 0; i < len(h.typing); i++ {
			for _, name := range s.input(h.typing[i]) {
				checksum = (checksum*31 + int64(len(name))*65536 + int64(name[0])*256 + int64(name[len(name)-1])) % 1000000007
				names++
			}
			checksum = (checksum*31 + 1) % 1000000007
		}
	}
	fmt.Printf("%d rounds of 5000 calls: %d names, checksum %d\n", rounds, names, checksum)
}
