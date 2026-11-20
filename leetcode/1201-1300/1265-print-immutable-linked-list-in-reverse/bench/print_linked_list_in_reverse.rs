// LeetCode #1265 bench, in Rust: the ★ arm (by recursion: a node prints
// after everything after it has, every call through a `&dyn` trait object)
// on 100 random lists of 1000 nodes built once, 300 rounds; everything each
// round prints folded into a checksum. The nodes are `Rc`s, as Kāra's
// `shared struct` is counted, and what they print goes in one
// `Rc<RefCell<Vec<i64>>>`.
use std::cell::RefCell;
use std::rc::Rc;

trait ImmutableListNode {
    fn print_value(&self);
    fn get_next(&self) -> Option<Rc<dyn ImmutableListNode>>;
}

fn print_linked_list_in_reverse(head: &dyn ImmutableListNode) {
    if let Some(next) = head.get_next() {
        print_linked_list_in_reverse(&*next);
    }
    head.print_value();
}

struct Node {
    val: i64,
    next: Option<Rc<Node>>,
    printed: Rc<RefCell<Vec<i64>>>,
}

impl ImmutableListNode for Node {
    fn print_value(&self) {
        self.printed.borrow_mut().push(self.val);
    }

    fn get_next(&self) -> Option<Rc<dyn ImmutableListNode>> {
        match &self.next {
            Some(n) => Some(n.clone()),
            None => None,
        }
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let printed = Rc::new(RefCell::new(Vec::new()));
    let mut seed = 1265i64;
    let mut heads: Vec<Rc<Node>> = Vec::new();
    for _ in 0..100 {
        let mut head: Option<Rc<Node>> = None;
        for _ in 0..1000 {
            head = Some(Rc::new(Node {
                val: next_random(&mut seed) % 2001 - 1000,
                next: head,
                printed: printed.clone(),
            }));
        }
        heads.push(head.unwrap());
    }
    let mut check: i64 = 0;
    for round in 0..300 {
        for h in &heads {
            printed.borrow_mut().clear();
            print_linked_list_in_reverse(&**h);
            check = (check + round) % 1000000007;
            for v in printed.borrow().iter() {
                check = (check * 131 + v + 1000) % 1000000007;
            }
        }
    }
    println!("300 rounds of 100 lists of 1000 nodes: checksum {}", check);
}
