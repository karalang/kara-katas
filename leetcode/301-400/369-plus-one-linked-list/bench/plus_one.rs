// Benchmark for #369 -- mirror of plus_one.kara. Rc<RefCell<..>> stands in
// for the shared struct with mutable fields.
use std::cell::RefCell;
use std::rc::Rc;

struct ListNode {
    val: i64,
    next: Option<Rc<RefCell<ListNode>>>,
}

type Link = Option<Rc<RefCell<ListNode>>>;

fn plus_one(head: Link) -> Link {
    let front = Rc::new(RefCell::new(ListNode { val: 0, next: head }));
    let mut last = front.clone();
    let mut at = front.borrow().next.clone();
    while let Some(node) = at {
        if node.borrow().val != 9 {
            last = node.clone();
        }
        at = node.borrow().next.clone();
    }
    last.borrow_mut().val += 1;
    let mut rest = last.borrow().next.clone();
    while let Some(node) = rest {
        node.borrow_mut().val = 0;
        rest = node.borrow().next.clone();
    }
    if front.borrow().val == 1 {
        Some(front)
    } else {
        front.borrow().next.clone()
    }
}

fn main() {
    let mut seed: i64 = 369;
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for i in 0..20 {
        let mut head: Link = None;
        for k in 0..100000 {
            seed = (seed * 1103515245 + 12345) % 2147483648;
            let d = if i % 2 == 0 && k < 50000 { 9 } else { (seed / 65536) % 10 };
            let val = if k == 99999 && d == 0 { 1 } else { d };
            head = Some(Rc::new(RefCell::new(ListNode { val, next: head })));
        }
        for _ in 0..20 {
            head = plus_one(head);
        }
        let mut at = head;
        while let Some(node) = at {
            total += 1;
            checksum = (checksum * 31 + node.borrow().val) % 1000000007;
            at = node.borrow_mut().next.take();
        }
    }
    println!("{} digits, checksum {}", total, checksum);
}
