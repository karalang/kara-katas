// LeetCode #897 bench: the ★ arm (an in-order walk that relinks as it
// goes) on 200,000 search trees of 100 nodes, LeetCode's largest, each
// made by putting in 100 random values from 0 to 1000; each chain is
// walked into a checksum. The same algorithm as increasing_bst.kara.
// LeetCode's Rust tree type, Option<Rc<RefCell<TreeNode>>>.
use std::cell::RefCell;
use std::rc::Rc;

struct TreeNode {
    val: i64,
    left: Option<Rc<RefCell<TreeNode>>>,
    right: Option<Rc<RefCell<TreeNode>>>,
}

type Tree = Rc<RefCell<TreeNode>>;

fn new_node(val: i64) -> Tree {
    Rc::new(RefCell::new(TreeNode { val, left: None, right: None }))
}

fn increasing_bst(root: Option<Tree>) -> Option<Tree> {
    let head = new_node(-1);
    let mut tail = head.clone();
    relink(root, &mut tail);
    let out = head.borrow_mut().right.take();
    out
}

fn relink(node: Option<Tree>, tail: &mut Tree) {
    if let Some(n) = node {
        let left = n.borrow_mut().left.take();
        relink(left, tail);
        tail.borrow_mut().right = Some(n.clone());
        *tail = n.clone();
        let right = n.borrow().right.clone();
        relink(right, tail);
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 897;
    let mut nodes: i64 = 0;
    let mut check: i64 = 0;
    for _ in 0..200000 {
        let root = new_node(next_random(&mut seed) % 1001);
        for _ in 1..100 {
            let v = next_random(&mut seed) % 1001;
            let mut cur = root.clone();
            loop {
                let next = if v < cur.borrow().val {
                    cur.borrow().left.clone()
                } else {
                    cur.borrow().right.clone()
                };
                match next {
                    Some(c) => cur = c,
                    None => {
                        let child = Some(new_node(v));
                        if v < cur.borrow().val {
                            cur.borrow_mut().left = child;
                        } else {
                            cur.borrow_mut().right = child;
                        }
                        break;
                    }
                }
            }
        }
        let mut cur = increasing_bst(Some(root));
        while let Some(n) = cur {
            nodes += 1;
            check = (check * 31 + n.borrow().val) % 1000000007;
            cur = n.borrow_mut().right.take();
        }
    }
    println!("200000 trees of 100 nodes: {} in the chains, checksum {}", nodes, check);
}
