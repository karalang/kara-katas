// Benchmark for #428: mirror of codec.kara (preorder with child
// counts).
package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)

type Node struct {
	val      int64
	children []*Node
}

func write(node *Node, out *strings.Builder) {
	if out.Len() > 0 {
		out.WriteByte(' ')
	}
	out.WriteString(strconv.FormatInt(node.val, 10))
	out.WriteByte(' ')
	out.WriteString(strconv.Itoa(len(node.children)))
	for _, child := range node.children {
		write(child, out)
	}
}

func serialize(root *Node) string {
	var out strings.Builder
	if root != nil {
		write(root, &out)
	}
	return out.String()
}

func read(words []string, at *int) *Node {
	val, _ := strconv.ParseInt(words[*at], 10, 64)
	count, _ := strconv.ParseInt(words[*at+1], 10, 64)
	*at += 2
	node := &Node{val: val}
	for i := int64(0); i < count; i++ {
		node.children = append(node.children, read(words, at))
	}
	return node
}

func deserialize(data string) *Node {
	if len(data) == 0 {
		return nil
	}
	words := strings.Split(data, " ")
	at := 0
	return read(words, &at)
}

func step(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func buildRandom(i int64, vals []int64, kids [][]int64) *Node {
	node := &Node{val: vals[i]}
	for _, k := range kids[i] {
		node.children = append(node.children, buildRandom(k, vals, kids))
	}
	return node
}

func total(node *Node) int64 {
	sum := node.val
	for _, child := range node.children {
		sum += total(child)
	}
	return sum
}

func main() {
	n := int64(10000)
	rounds := int64(100)
	if len(os.Args) > 1 {
		rounds, _ = strconv.ParseInt(os.Args[1], 10, 64)
	}
	seed := int64(428)
	chars := int64(0)
	checksum := int64(0)
	for r := int64(0); r < rounds; r++ {
		reach := 1 + step(&seed)%1000
		vals := make([]int64, 0, n)
		kids := make([][]int64, 0, n)
		for i := int64(0); i < n; i++ {
			vals = append(vals, step(&seed)%10001)
			kids = append(kids, nil)
			if i > 0 {
				lim := i
				if reach < lim {
					lim = reach
				}
				back := 1 + step(&seed)%lim
				kids[i-back] = append(kids[i-back], i)
			}
		}
		tree := buildRandom(0, vals, kids)
		text := serialize(tree)
		back := deserialize(text)
		chars += int64(len(text))
		checksum = (checksum*31 + int64(len(text)) + total(back)) % 1000000007
	}
	fmt.Printf("%d rounds of %d nodes: %d characters, checksum %d\n", rounds, n, chars, checksum)
}
