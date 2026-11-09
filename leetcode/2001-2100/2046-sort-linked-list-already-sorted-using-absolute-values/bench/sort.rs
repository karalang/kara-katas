// LeetCode #2046 -- the ★ arm as a benchmark; mirror of sort.kara. The
// nodes are `Rc<RefCell<ListNode>>`, the model of Kāra's `shared struct`.
use std::cell::RefCell;
use std::rc::Rc;

type Link = Option<Rc<RefCell<ListNode>>>;

struct ListNode {
    val: i64,
    next: Link,
}

fn sort_linked_list(head: Link) -> Link {
    let first = head?;
    let mut front = first.clone();
    let mut prev = first.clone();
    let mut cur = first.borrow().next.clone();
    while let Some(node) = cur {
        cur = node.borrow().next.clone();
        if node.borrow().val < 0 {
            prev.borrow_mut().next = node.borrow().next.clone();
            node.borrow_mut().next = Some(front);
            front = node;
        } else {
            prev = node;
        }
    }
    Some(front)
}

fn build(m: i64, round: i64) -> Link {
    let mut head: Link = None;
    let mut j = m - 1;
    while j >= 0 {
        let v = if (7 * j + round) % 3 == 0 { -(j / 2) } else { j / 2 };
        head = Some(Rc::new(RefCell::new(ListNode { val: v, next: head })));
        j -= 1;
    }
    head
}

fn main() {
    let rounds: i64 = 20000;
    let m: i64 = 1000;
    let mut negatives: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        let mut cur = sort_linked_list(build(m, r));
        while let Some(node) = cur {
            let n = node.borrow();
            if n.val < 0 {
                negatives += 1;
            }
            check = (check * 31 + n.val + 1000) % 1_000_000_007;
            cur = n.next.clone();
        }
    }
    println!("{} rounds: {} negatives, checksum {}", rounds, negatives, check);
}
