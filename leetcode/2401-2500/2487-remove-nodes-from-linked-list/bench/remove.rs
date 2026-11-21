// LeetCode #2487: Remove Nodes From Linked List -- Rust mirror of the ★
// arm's benchmark (remove.kara): the same 22000 lists, each cleared by the
// same stack. The nodes are `Rc<RefCell<ListNode>>`, the model of Kāra's
// `shared struct`.
use std::cell::RefCell;
use std::rc::Rc;

type Link = Option<Rc<RefCell<ListNode>>>;

struct ListNode {
    val: i64,
    next: Link,
}

fn remove_nodes(head: Link) -> Link {
    let mut stack: Vec<Rc<RefCell<ListNode>>> = Vec::new();
    let mut cur = head;
    while let Some(node) = cur {
        cur = node.borrow().next.clone();
        while let Some(top) = stack.last() {
            if top.borrow().val >= node.borrow().val {
                break;
            }
            stack.pop();
        }
        stack.push(node);
    }
    let mut result: Link = None;
    while let Some(node) = stack.pop() {
        node.borrow_mut().next = result;
        result = Some(node);
    }
    result
}

fn build(m: i64, round: i64, check: i64) -> Link {
    let mut head: Link = None;
    let mut j = m - 1;
    while j >= 0 {
        head = Some(Rc::new(RefCell::new(ListNode { val: (m - j) * 10 + (round * 7919 + j * 104729 + check) % 37, next: head })));
        j -= 1;
    }
    head
}

fn main() {
    let rounds: i64 = 22000;
    let mut kept: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        let mut cur = remove_nodes(build(1000, r, check));
        while let Some(node) = cur {
            let n = node.borrow();
            kept += 1;
            check = (check * 31 + n.val) % 1_000_000_007;
            cur = n.next.clone();
        }
    }
    println!("{} lists of 1000 nodes: {} kept, checksum {}", rounds, kept, check);
}
