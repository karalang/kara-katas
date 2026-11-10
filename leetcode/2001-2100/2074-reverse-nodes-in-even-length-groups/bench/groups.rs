// LeetCode #2074: Reverse Nodes in Even Length Groups -- Rust mirror of
// the ★ arm's benchmark (groups.kara). The nodes are
// `Rc<RefCell<ListNode>>`, the model of Kāra's `shared struct`.
use std::cell::RefCell;
use std::rc::Rc;

type Link = Option<Rc<RefCell<ListNode>>>;

struct ListNode {
    val: i64,
    next: Link,
}

fn reverse_even_length_groups(head: Link) -> Link {
    let first = head?;
    let mut before = first.clone();
    let mut want = 2;
    loop {
        let Some(start) = before.borrow().next.clone() else {
            break;
        };
        let mut len = 0;
        let mut end = start.clone();
        let mut cur = Some(start.clone());
        while len < want {
            let Some(node) = cur else {
                break;
            };
            len += 1;
            cur = node.borrow().next.clone();
            end = node;
        }
        if len % 2 == 0 {
            let mut turned = end.borrow().next.clone();
            let mut rest = Some(start.clone());
            for _ in 0..len {
                let node = rest.unwrap();
                rest = node.borrow().next.clone();
                node.borrow_mut().next = turned;
                turned = Some(node);
            }
            before.borrow_mut().next = turned;
            before = start;
        } else {
            before = end;
        }
        want += 1;
    }
    Some(first)
}

fn build(m: i64, round: i64) -> Link {
    let mut head: Link = None;
    let mut j = m - 1;
    while j >= 0 {
        head = Some(Rc::new(RefCell::new(ListNode { val: (j * 7919 + round) % 100001, next: head })));
        j -= 1;
    }
    head
}

fn main() {
    let mut check: i64 = 0;
    for r in 0..2000 {
        let mut cur = reverse_even_length_groups(build(10000 + r % 7, r));
        while let Some(node) = cur {
            let n = node.borrow();
            check = (check * 31 + n.val) % 1000000007;
            cur = n.next.clone();
        }
    }
    println!("2000 rounds: checksum {check}");
}
