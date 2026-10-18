// LeetCode #707: Design Linked List -- singly linked, with a sentinel.
// Benchmark mirror of the Kara star arm: walk to the node before the
// position, then link a new node in after it or link past the next.

struct Node {
    val: i64,
    next: Option<Box<Node>>,
}

struct MyLinkedList {
    head: Box<Node>,
    size: i64,
}

impl MyLinkedList {
    fn new() -> Self {
        MyLinkedList { head: Box::new(Node { val: 0, next: None }), size: 0 }
    }

    fn before(&self, index: i64) -> &Node {
        let mut at: &Node = &self.head;
        for _ in 0..index {
            at = at.next.as_ref().unwrap();
        }
        at
    }

    fn before_mut(&mut self, index: i64) -> &mut Node {
        let mut at: &mut Node = &mut self.head;
        for _ in 0..index {
            at = at.next.as_mut().unwrap();
        }
        at
    }

    fn get(&self, index: i64) -> i64 {
        if index < 0 || index >= self.size {
            return -1;
        }
        self.before(index).next.as_ref().unwrap().val
    }

    fn add_at_head(&mut self, val: i64) {
        self.add_at_index(0, val);
    }

    fn add_at_tail(&mut self, val: i64) {
        self.add_at_index(self.size, val);
    }

    fn add_at_index(&mut self, index: i64, val: i64) {
        if index < 0 || index > self.size {
            return;
        }
        let prev = self.before_mut(index);
        let next = prev.next.take();
        prev.next = Some(Box::new(Node { val, next }));
        self.size += 1;
    }

    fn delete_at_index(&mut self, index: i64) {
        if index < 0 || index >= self.size {
            return;
        }
        let prev = self.before_mut(index);
        let gone = prev.next.take().unwrap();
        prev.next = gone.next;
        self.size -= 1;
    }
}

impl Drop for MyLinkedList {
    // Unlinks node by node, so a long list does not recurse.
    fn drop(&mut self) {
        let mut at = self.head.next.take();
        while let Some(mut node) = at {
            at = node.next.take();
        }
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed: i64 = 707;
    let mut values = 0;
    let mut checksum: i64 = 0;
    for _ in 0..5 {
        for _ in 0..10 {
            let mut list = MyLinkedList::new();
            for _ in 0..6000 {
                let op = next_random(&mut seed) % 5;
                let index = next_random(&mut seed) % (list.size + 3);
                let val = next_random(&mut seed) % 1001;
                if op == 0 {
                    checksum = (checksum * 31 + list.get(index) + 2) % 1000000007;
                } else if op == 1 {
                    list.add_at_head(val);
                } else if op == 2 {
                    list.add_at_tail(val);
                } else if op == 3 {
                    list.add_at_index(index, val);
                } else {
                    list.delete_at_index(index);
                }
            }
            values += list.size;
        }
    }
    println!("5 rounds of 10 lists of 6000 calls: {} values left, checksum {}", values, checksum);
}
