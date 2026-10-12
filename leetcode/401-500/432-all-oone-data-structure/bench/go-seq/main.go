// Benchmark for #432: mirror of all_one.kara (a list of count buckets).
// Go's collector frees the buckets; a bucket's set of keys is a map.
package main

import (
	"fmt"
	"os"
	"strconv"
)

type Bucket struct {
	count      int64
	keys       map[string]struct{}
	prev, next *Bucket
}

func newBucket(count int64) *Bucket {
	return &Bucket{count: count, keys: map[string]struct{}{}}
}

func linkAfter(at *Bucket, count int64) *Bucket {
	b := newBucket(count)
	after := at.next
	b.next = after
	after.prev = b
	at.next = b
	b.prev = at
	return b
}

func unlink(b *Bucket) {
	b.prev.next = b.next
	b.next.prev = b.prev
}

func anyKey(b *Bucket) string {
	for k := range b.keys {
		return k
	}
	return ""
}

type AllOne struct {
	head, tail *Bucket
	bucketOf   map[string]*Bucket
}

func newAllOne() *AllOne {
	head := newBucket(0)
	tail := newBucket(-1)
	head.next = tail
	tail.prev = head
	return &AllOne{head: head, tail: tail, bucketOf: map[string]*Bucket{}}
}

func (ds *AllOne) inc(key string) {
	cur, ok := ds.bucketOf[key]
	if !ok {
		cur = ds.head
	}
	after := cur.next
	up := after
	if after.count != cur.count+1 {
		up = linkAfter(cur, cur.count+1)
	}
	up.keys[key] = struct{}{}
	ds.bucketOf[key] = up
	if cur.count > 0 {
		delete(cur.keys, key)
		if len(cur.keys) == 0 {
			unlink(cur)
		}
	}
}

func (ds *AllOne) dec(key string) {
	cur := ds.bucketOf[key]
	if cur.count == 1 {
		delete(ds.bucketOf, key)
	} else {
		before := cur.prev
		down := before
		if before.count != cur.count-1 {
			down = linkAfter(before, cur.count-1)
		}
		down.keys[key] = struct{}{}
		ds.bucketOf[key] = down
	}
	delete(cur.keys, key)
	if len(cur.keys) == 0 {
		unlink(cur)
	}
}

func (ds *AllOne) getMaxKey() string { return anyKey(ds.tail.prev) }
func (ds *AllOne) getMinKey() string { return anyKey(ds.head.next) }

func nextRandom(seed *int64) int64 {
	*seed = (*seed*1103515245 + 12345) % 2147483648
	return *seed / 65536
}

func keyID(key string) int64 {
	if key == "" {
		return -1
	}
	var id int64
	for i := 0; i < len(key); i++ {
		if key[i] != 'k' {
			id = id*10 + int64(key[i]-'0')
		}
	}
	return id
}

func main() {
	keys := int64(10000)
	operations := int64(2000000)
	if len(os.Args) > 1 {
		operations, _ = strconv.ParseInt(os.Args[1], 10, 64)
	}
	seed := int64(432)
	ds := newAllOne()
	count := make([]int64, keys)
	var queries, checksum int64
	for i := int64(0); i < operations; i++ {
		roll := nextRandom(&seed) % 10
		hi := nextRandom(&seed)
		id := (hi*32768 + nextRandom(&seed)) % keys
		if roll < 2 {
			var answer string
			if roll == 0 {
				answer = ds.getMaxKey()
			} else {
				answer = ds.getMinKey()
			}
			a := keyID(answer)
			c := int64(0)
			if a >= 0 {
				c = count[a]
			}
			queries++
			checksum = (checksum*31 + c + 1) % 1000000007
		} else if roll < 5 && count[id] > 0 {
			ds.dec("k" + strconv.FormatInt(id, 10))
			count[id]--
		} else {
			ds.inc("k" + strconv.FormatInt(id, 10))
			count[id]++
		}
	}
	fmt.Printf("%d operations on %d keys: %d queries, checksum %d\n", operations, keys, queries, checksum)
}
