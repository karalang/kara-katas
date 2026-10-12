// Benchmark for #430: mirror of flatten.kara (recursion). The Kāra
// `shared struct` is reference counted, so a node here is an
// Rc<RefCell<Node>>; prev links are strong too, as in the Kāra program,
// and the walk breaks every link so the nodes are freed.
use std::cell::RefCell;
use std::rc::Rc;

type Link = Option<Rc<RefCell<Node>>>;

struct Node {
    val: i64,
    prev: Link,
    next: Link,
    child: Link,
}

fn flatten_level(head: Rc<RefCell<Node>>) -> Rc<RefCell<Node>> {
    let mut cur = head;
    loop {
        let after = cur.borrow().next.clone();
        let child = cur.borrow().child.clone();
        if let Some(c) = child {
            let child_tail = flatten_level(c.clone());
            cur.borrow_mut().next = Some(c.clone());
            c.borrow_mut().prev = Some(cur.clone());
            cur.borrow_mut().child = None;
            match &after {
                Some(a) => {
                    child_tail.borrow_mut().next = Some(a.clone());
                    a.borrow_mut().prev = Some(child_tail.clone());
                }
                None => return child_tail,
            }
        }
        match after {
            Some(a) => cur = a,
            None => return cur,
        }
    }
}

fn flatten(head: Link) -> Link {
    if let Some(h) = &head {
        flatten_level(h.clone());
    }
    head
}

fn step(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn make_level(length: i64, budget: &mut i64, depth: i64, next_val: &mut i64, seed: &mut i64) -> Link {
    let mut head: Link = None;
    let mut last: Link = None;
    for _ in 0..length {
        if *budget == 0 {
            break;
        }
        *budget -= 1;
        let node = Rc::new(RefCell::new(Node { val: *next_val, prev: None, next: None, child: None }));
        *next_val += 1;
        if depth < 6 && *budget > 0 && step(seed) % 4 == 0 {
            let child_length = 1 + step(seed) % 8;
            node.borrow_mut().child = make_level(child_length, budget, depth + 1, next_val, seed);
        }
        match &last {
            Some(l) => {
                l.borrow_mut().next = Some(node.clone());
                node.borrow_mut().prev = Some(l.clone());
            }
            None => head = Some(node.clone()),
        }
        last = Some(node);
    }
    head
}

fn main() {
    let n: i64 = 1000;
    let rounds: i64 = std::env::args().nth(1).map_or(2000, |s| s.parse().unwrap());
    let mut seed: i64 = 430;
    let mut misplaced: i64 = 0;
    let mut checksum: i64 = 0;
    for _ in 0..rounds {
        let mut budget = n;
        let mut next_val = 1;
        let head = make_level(n, &mut budget, 0, &mut next_val, &mut seed);
        let mut cur = flatten(head);
        let mut expect = 1;
        while let Some(node) = cur {
            let val = node.borrow().val;
            if val != expect {
                misplaced += 1;
            }
            expect += 1;
            checksum = (checksum * 31 + val) % 1000000007;
            cur = node.borrow().next.clone();
            node.borrow_mut().prev = None;
            node.borrow_mut().next = None;
        }
    }
    println!("{} rounds of {} nodes: {} misplaced, checksum {}", rounds, n, misplaced, checksum);
}
