// LeetCode #1669: Merge In Between Linked Lists -- the bench's Rust mirror:
// the ★ arm on one list of 100000 nodes, 10000 times cut at a random
// place, 1 to 8 nodes taken out and a new list of 1 to 8 put in, every cut
// and value drawn first. Nodes are `Rc<RefCell<ListNode>>`, as Kāra's
// `shared struct` is.

use std::cell::RefCell;
use std::rc::Rc;

struct ListNode {
    val: i64,
    next: Option<Rc<RefCell<ListNode>>>,
}

type Handle = Rc<RefCell<ListNode>>;

fn merge_in_between(list1: Option<Handle>, a: i64, b: i64, list2: Option<Handle>) -> Option<Handle> {
    let head = list1.unwrap();
    let mut before = Rc::clone(&head);
    for _ in 1..a {
        let next = before.borrow().next.clone().unwrap();
        before = next;
    }
    let mut after = before.borrow().next.clone();
    for _ in a..=b {
        after = after.unwrap().borrow().next.clone();
    }
    let first = list2.unwrap();
    let mut last = Rc::clone(&first);
    loop {
        let next = last.borrow().next.clone();
        match next {
            Some(node) => last = node,
            None => break,
        }
    }
    before.borrow_mut().next = Some(first);
    last.borrow_mut().next = after;
    Some(head)
}

// ---- the harness ----------------------------------------------------------

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn build(values: &[i64]) -> Option<Handle> {
    let mut head: Option<Handle> = None;
    for &v in values.iter().rev() {
        head = Some(Rc::new(RefCell::new(ListNode { val: v, next: head })));
    }
    head
}

fn main() {
    let start: i64 = 100000;
    let rounds = 10000;
    let mut seed: i64 = 1669;
    let mut values: Vec<i64> = Vec::new();
    for _ in 0..start {
        values.push((next_random(&mut seed) * 32768 + next_random(&mut seed)) % 1000001);
    }
    let mut len = start;
    let mut cuts: Vec<(i64, i64, Vec<i64>)> = Vec::new();
    for _ in 0..rounds {
        let m = next_random(&mut seed) % 8 + 1;
        let a = (next_random(&mut seed) * 32768 + next_random(&mut seed)) % (len - 2) + 1;
        let b = a + next_random(&mut seed) % std::cmp::min(8, len - 1 - a);
        let mut list2 = Vec::new();
        for _ in 0..m {
            list2.push((next_random(&mut seed) * 32768 + next_random(&mut seed)) % 1000001);
        }
        len += m - (b - a + 1);
        cuts.push((a, b, list2));
    }
    let mut list = build(&values);
    for (a, b, list2) in &cuts {
        list = merge_in_between(list, *a, *b, build(list2));
    }
    let mut nodes = 0;
    let mut check: i64 = 0;
    let mut cur = list.clone();
    while let Some(node) = cur {
        nodes += 1;
        check = (check * 31 + node.borrow().val + 1) % 1000000007;
        cur = node.borrow().next.clone();
    }
    // unlink one node at a time, so the drop does not recurse 10^5 deep
    let mut cur = list;
    while let Some(node) = cur {
        cur = node.borrow_mut().next.take();
    }
    println!("{} nodes, {} merges: {} nodes, checksum {}", start, rounds, nodes, check);
}
