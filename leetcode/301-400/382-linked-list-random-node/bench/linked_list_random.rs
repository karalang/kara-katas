// Benchmark mirror of linked_list_random.kara (#382): reservoir sampling
// over a singly linked list of reference-counted nodes, as Kāra's shared
// struct is.
use std::rc::Rc;

struct ListNode {
    val: i64,
    next: Option<Rc<ListNode>>,
}

struct Solution {
    head: Option<Rc<ListNode>>,
    seed: i64,
}

impl Solution {
    fn below(&mut self, n: i64) -> i64 {
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648;
        (self.seed / 65536) % n
    }

    fn get_random(&mut self) -> i64 {
        let mut kept = 0;
        let mut i = 0;
        let mut at = self.head.clone();
        while let Some(node) = at {
            i += 1;
            if self.below(i) == 0 {
                kept = node.val;
            }
            at = node.next.clone();
        }
        kept
    }
}

fn main() {
    let mut seed: i64 = 7;
    let mut head: Option<Rc<ListNode>> = None;
    for _ in 0..10000 {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        head = Some(Rc::new(ListNode { val: (seed / 65536) % 20001 - 10000, next: head }));
    }
    let mut s = Solution { head, seed: 382 };
    let mut checksum: i64 = 0;
    for _ in 0..20000 {
        checksum = (checksum * 31 + s.get_random() + 10000) % 1000000007;
    }
    println!("checksum {}", checksum);
}
