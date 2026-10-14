// Benchmark for #588: Go mirror of the ★ arm (a tree of shared nodes);
// see ../file_system.kara. Each node is a pointer, and a directory keeps
// its entries in a map, sorted when it is listed, since Go has no sorted
// map.
package main

import (
	"fmt"
	"sort"
	"strings"
)

type node struct {
	isFile   bool
	content  strings.Builder
	children map[string]*node
}

func newNode() *node {
	return &node{children: map[string]*node{}}
}

type fileSystem struct {
	root *node
}

func (fs *fileSystem) walk(path string, make bool) *node {
	n := fs.root
	for _, name := range strings.Split(path, "/") {
		if name == "" {
			continue
		}
		child, ok := n.children[name]
		if !ok && make {
			child = newNode()
			n.children[name] = child
		}
		n = child
	}
	return n
}

func (fs *fileSystem) ls(path string) []string {
	n := fs.walk(path, false)
	if n.isFile {
		parts := strings.Split(path, "/")
		return []string{parts[len(parts)-1]}
	}
	names := make([]string, 0, len(n.children))
	for name := range n.children {
		names = append(names, name)
	}
	sort.Strings(names)
	return names
}

func (fs *fileSystem) mkdir(path string) {
	fs.walk(path, true)
}

func (fs *fileSystem) addContentToFile(filePath, content string) {
	n := fs.walk(filePath, true)
	n.isFile = true
	n.content.WriteString(content)
}

func (fs *fileSystem) readContentFromFile(filePath string) string {
	return fs.walk(filePath, false).content.String()
}

// ---- benchmark --------------------------------------------------------------

type op struct {
	kind, path, content string
}

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func dirPath(depth int64, seed *int64) string {
	alphabet := "abcde"
	path := ""
	for i := int64(0); i < depth; i++ {
		k := nextRandom(seed) % 5
		path += "/" + alphabet[k:k+1]
	}
	return path
}

func script(seed *int64) []op {
	names := "fghij"
	made := []string{"/"}
	files := []string{}
	ops := []op{}
	for len(ops) < 300 {
		roll := nextRandom(seed) % 10
		if roll < 3 {
			ops = append(ops, op{"ls", made[nextRandom(seed)%int64(len(made))], ""})
		} else if roll < 4 && len(files) > 0 {
			ops = append(ops, op{"read", files[nextRandom(seed)%int64(len(files))], ""})
		} else if roll < 7 {
			path := dirPath(1+nextRandom(seed)%4, seed)
			made = append(made, path)
			ops = append(ops, op{"mkdir", path, ""})
		} else {
			k := nextRandom(seed) % 5
			path := dirPath(nextRandom(seed)%4, seed) + "/" + names[k:k+1]
			content := ""
			for i, n := int64(0), 1+nextRandom(seed)%5; i < n; i++ {
				c := nextRandom(seed) % 5
				content += names[c : c+1]
			}
			made = append(made, path)
			files = append(files, path)
			ops = append(ops, op{"add", path, content})
		}
	}
	return ops
}

func main() {
	var count, rounds int64 = 200, 200
	var seed int64 = 588
	scripts := [][]op{}
	for i := int64(0); i < count; i++ {
		scripts = append(scripts, script(&seed))
	}
	var lines, checksum int64
	for round := int64(0); round < rounds; round++ {
		for g := int64(0); g < count; g++ {
			fs := &fileSystem{root: newNode()}
			for _, o := range scripts[(round*7+g)%count] {
				switch o.kind {
				case "ls":
					for _, name := range fs.ls(o.path) {
						checksum = (checksum*31 + int64(len(name))) % 1000000007
					}
					lines++
				case "mkdir":
					fs.mkdir(o.path)
				case "add":
					fs.addContentToFile(o.path, o.content)
				default:
					checksum = (checksum*31 + int64(len(fs.readContentFromFile(o.path)))) % 1000000007
					lines++
				}
			}
		}
	}
	fmt.Printf("%d scripts of 300 commands, %d rounds: %d answers, checksum %d\n", count, rounds, lines, checksum)
}
