// LeetCode #1171: Remove Zero Sum Consecutive Nodes from Linked List -- the
// ★ arm's bench in Rust: prefix sums in two passes, the last node of each
// running sum kept in a `HashMap`. A Kāra `shared struct` is a counted
// reference with interior mutability, so the nodes here are
// `Rc<RefCell<ListNode>>`. The same 32 lists and 400 rounds.
use std::cell::RefCell;
use std::collections::HashMap;
use std::rc::Rc;

struct ListNode {
    val: i64,
    next: Option<Rc<RefCell<ListNode>>>,
}

type Link = Option<Rc<RefCell<ListNode>>>;

fn remove_zero_sum_sublists(head: Link) -> Link {
    let dummy = Rc::new(RefCell::new(ListNode { val: 0, next: head }));
    let mut last: HashMap<i64, Rc<RefCell<ListNode>>> = HashMap::new();
    let mut sum = 0;
    let mut cur = Some(dummy.clone());
    while let Some(node) = cur {
        sum += node.borrow().val;
        last.insert(sum, node.clone());
        cur = node.borrow().next.clone();
    }
    sum = 0;
    cur = Some(dummy.clone());
    while let Some(node) = cur {
        sum += node.borrow().val;
        let next = last[&sum].borrow().next.clone();
        node.borrow_mut().next = next.clone();
        cur = next;
    }
    let out = dummy.borrow().next.clone();
    out
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_value(seed: &mut i64, kind: usize) -> i64 {
    match kind {
        0 => next_random(seed) % 5 - 2,
        1 => next_random(seed) % 11 - 5,
        2 => next_random(seed) % 101 - 50,
        _ => {
            let size = 1 + next_random(seed) % 3;
            if next_random(seed) % 2 == 0 { size } else { -size }
        }
    }
}

fn main() {
    let rounds = 400;
    let mut seed = 1171;
    let mut lists: Vec<Vec<i64>> = Vec::new();
    for l in 0..32 {
        lists.push((0..1000).map(|_| random_value(&mut seed, l % 4)).collect());
    }
    let mut kept: i64 = 0;
    let mut check: i64 = 0;
    for _ in 0..rounds {
        for l in 0..32 {
            let i = (next_random(&mut seed) % 1000) as usize;
            lists[l][i] = random_value(&mut seed, l % 4);
            let mut head: Link = None;
            for &v in lists[l].iter().rev() {
                head = Some(Rc::new(RefCell::new(ListNode { val: v, next: head })));
            }
            let mut cur = remove_zero_sum_sublists(head);
            while let Some(node) = cur {
                kept += 1;
                check = (check * 131 + node.borrow().val + 1001) % 1000000007;
                cur = node.borrow().next.clone();
            }
        }
    }
    println!("{rounds} rounds over 32 lists of 1000 values: {kept} kept, checksum {check}");
}
