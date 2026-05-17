// LeetCode #2 bench mirror — algorithmic peer of iterative.kara.
//
// Uses `Rc<RefCell<ListNode>>` for the linked list to mirror Kāra's
// `shared struct` reference semantics — same per-node RC overhead and
// the same alloc-per-digit shape. Compiled with `rustc -O`.

use std::cell::RefCell;
use std::rc::Rc;

type Link = Option<Rc<RefCell<ListNode>>>;

struct ListNode {
    val: i64,
    next: Link,
}

fn add_two_numbers(l1: &Link, l2: &Link) -> Link {
    let dummy = Rc::new(RefCell::new(ListNode { val: 0, next: None }));
    let mut tail = dummy.clone();
    let mut a = l1.clone();
    let mut b = l2.clone();
    let mut carry: i64 = 0;
    loop {
        let mut s: i64 = carry;
        let mut done = true;
        if let Some(n) = a.clone() {
            s += n.borrow().val;
            a = n.borrow().next.clone();
            done = false;
        }
        if let Some(n) = b.clone() {
            s += n.borrow().val;
            b = n.borrow().next.clone();
            done = false;
        }
        if done && s == 0 {
            break;
        }
        let node = Rc::new(RefCell::new(ListNode {
            val: s % 10,
            next: None,
        }));
        tail.borrow_mut().next = Some(node.clone());
        tail = node;
        carry = s / 10;
    }
    let result = dummy.borrow().next.clone();
    result
}

fn from_array(arr: &[i64]) -> Link {
    if arr.is_empty() {
        return None;
    }
    let head = Rc::new(RefCell::new(ListNode {
        val: arr[0],
        next: None,
    }));
    let mut tail = head.clone();
    for &v in &arr[1..] {
        let node = Rc::new(RefCell::new(ListNode { val: v, next: None }));
        tail.borrow_mut().next = Some(node.clone());
        tail = node;
    }
    Some(head)
}

fn main() {
    const N: usize = 100;
    const K: i64 = 500_000;
    let a = vec![9i64; N];
    let b = vec![9i64; N];
    let l1 = from_array(&a);
    let l2 = from_array(&b);
    let mut sum: i64 = 0;
    for _ in 0..K {
        let out = add_two_numbers(&l1, &l2);
        if let Some(node) = std::hint::black_box(out) {
            sum += node.borrow().val;
        }
    }
    println!("{}", sum);
}
