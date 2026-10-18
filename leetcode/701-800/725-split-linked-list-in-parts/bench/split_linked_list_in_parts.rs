// LeetCode #725: Split Linked List in Parts -- count, then cut in place.
// Benchmark mirror of the Kara star arm: count the nodes, then walk the
// list once, taking each part's head, stepping to its last node and
// cutting the link after it. A Kara `shared struct` is a
// reference-counted node whose `mut` fields carry a borrow flag, so the
// honest twin is `Rc<RefCell<ListNode>>`.
use std::cell::RefCell;
use std::rc::Rc;

struct ListNode {
    val: i64,
    next: Link,
}

type Link = Option<Rc<RefCell<ListNode>>>;

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn split_list_to_parts(head: &Link, k: i64) -> Vec<Link> {
    let mut n = 0;
    let mut cur = head.clone();
    while let Some(node) = cur {
        n += 1;
        cur = node.borrow().next.clone();
    }
    let size = n / k;
    let extra = n % k;
    let mut parts: Vec<Link> = Vec::new();
    cur = head.clone();
    for i in 0..k {
        parts.push(cur.clone());
        let len = if i < extra { size + 1 } else { size };
        if len > 0 {
            if let Some(first) = cur.clone() {
                let mut tail = first;
                for _ in 0..len - 1 {
                    let next = tail.borrow().next.clone();
                    if let Some(next) = next {
                        tail = next;
                    }
                }
                cur = tail.borrow_mut().next.take();
            }
        }
    }
    parts
}

// Put the parts back together, starting from part `from` and going round.
fn rejoin(parts: &[Link], from: usize) -> Link {
    let k = parts.len();
    let mut head: Link = None;
    let mut i = k;
    while i > 0 {
        i -= 1;
        if let Some(first) = parts[(from + i) % k].clone() {
            let mut tail = first.clone();
            loop {
                let next = tail.borrow().next.clone();
                match next {
                    Some(next) => tail = next,
                    None => break,
                }
            }
            tail.borrow_mut().next = head;
            head = Some(first);
        }
    }
    head
}

fn main() {
    let mut seed: i64 = 725;
    let mut lists: Vec<Link> = Vec::new();
    for _ in 0..20 {
        let mut head: Link = None;
        for _ in 0..1000 {
            head = Some(Rc::new(RefCell::new(ListNode { val: next_random(&mut seed) % 1000, next: head })));
        }
        lists.push(head);
    }
    let mut hash: i64 = 0;
    for round in 0..5000i64 {
        for d in 0..20i64 {
            let k = 1 + (round * 7 + d) % 50;
            let parts = split_list_to_parts(&lists[d as usize], k);
            for p in parts.iter() {
                let v = match p {
                    Some(first) => first.borrow().val + 1,
                    None => 0,
                };
                hash = (hash * 31 + v) % 1000000007;
            }
            lists[d as usize] = rejoin(&parts, (round % k) as usize);
        }
    }
    println!("5000 rounds of 20 lists of 1000 numbers: hash {}", hash);
}
