// Benchmark workload for LeetCode #328 — Rust mirror of odd_even_list.kara.
//
// Same workload: a list of LEN nodes built once, then PUNCHES punches, each
// regrouping the list in place and walking it once to fold a rolling hash
// and replace one value. A Kāra `shared struct` is a reference-counted node
// whose `mut` fields carry a borrow flag, so the honest twin is
// `Rc<RefCell<Node>>`. The list is leaked at the end, as the C twin leaks
// it: dropping a million-node `Rc` chain recurses once per node.
use std::cell::RefCell;
use std::rc::Rc;

const LEN: i64 = 1_000_000;
const PUNCHES: i64 = 10;
const MODULUS: i64 = 1_073_741_789;

struct ListNode {
    val: i64,
    next: Option<Rc<RefCell<ListNode>>>,
}

type Link = Option<Rc<RefCell<ListNode>>>;

fn odd_even_list(head: Link) -> Link {
    let first = head?;
    let second_link = first.borrow().next.clone();
    let second = match second_link {
        None => return Some(first),
        Some(s) => s,
    };
    let mut odd = first.clone();
    let mut even = second.clone();
    loop {
        let next_link = even.borrow().next.clone();
        let n = match next_link {
            None => break,
            Some(n) => n,
        };
        odd.borrow_mut().next = Some(n.clone());
        odd = n.clone();
        let after = n.borrow().next.clone();
        even.borrow_mut().next = after.clone();
        match after {
            None => break,
            Some(m) => even = m,
        }
    }
    odd.borrow_mut().next = Some(second);
    Some(first)
}

fn next_rand(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 328;
    let mut head: Link = None;
    for _ in 0..LEN {
        let hi = next_rand(&mut seed);
        let lo = next_rand(&mut seed);
        head = Some(Rc::new(RefCell::new(ListNode { val: (hi * 32768 + lo) % 1_000_000, next: head })));
    }
    let mut sink: i64 = 0;
    for _ in 0..PUNCHES {
        head = odd_even_list(head);
        let hi = next_rand(&mut seed);
        let lo = next_rand(&mut seed);
        let pos = (hi * 32768 + lo) % LEN;
        let hi = next_rand(&mut seed);
        let lo = next_rand(&mut seed);
        let fresh = (hi * 32768 + lo) % 1_000_000;
        let mut cur = head.clone();
        let mut k: i64 = 0;
        while let Some(n) = cur {
            if k == pos {
                n.borrow_mut().val = fresh;
            }
            sink = (sink * 31 + n.borrow().val * (k + 1)) % MODULUS;
            let next_link = n.borrow().next.clone();
            cur = next_link;
            k += 1;
        }
    }
    println!("sink {}", sink);
    std::mem::forget(head);
}
