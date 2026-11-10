// LeetCode #2095: Delete the Middle Node of a Linked List -- Rust mirror of
// the ★ arm's benchmark (middle.kara): the same 20000 lists, each with its
// middle deleted 50 times by the same two runners. The nodes are
// `Rc<RefCell<ListNode>>`, the model of Kāra's `shared struct`.
use std::cell::RefCell;
use std::rc::Rc;

type Link = Option<Rc<RefCell<ListNode>>>;

struct ListNode {
    val: i64,
    next: Link,
}

fn delete_middle(head: Link) -> Link {
    let first = head?;
    let second = first.borrow().next.clone()?;
    let mut slow = first.clone();
    let mut fast = second.borrow().next.clone();
    while let Some(f) = fast {
        let Some(after) = f.borrow().next.clone() else {
            break;
        };
        let next = slow.borrow().next.clone().unwrap();
        slow = next;
        fast = after.borrow().next.clone();
    }
    let middle = slow.borrow().next.clone().unwrap();
    slow.borrow_mut().next = middle.borrow().next.clone();
    Some(first)
}

fn build(m: i64, round: i64) -> Link {
    let mut head: Link = None;
    let mut j = m - 1;
    while j >= 0 {
        head = Some(Rc::new(RefCell::new(ListNode { val: (round * 7919 + j * 104729) % 100000 + 1, next: head })));
        j -= 1;
    }
    head
}

fn main() {
    let rounds: i64 = 20000;
    let mut left: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        let mut list = build(1000, r);
        for _ in 0..50 {
            list = delete_middle(list);
        }
        let mut cur = list;
        while let Some(node) = cur {
            let n = node.borrow();
            left += 1;
            check = (check * 31 + n.val) % 1_000_000_007;
            cur = n.next.clone();
        }
    }
    println!("{} rounds: {} nodes left, checksum {}", rounds, left, check);
}
