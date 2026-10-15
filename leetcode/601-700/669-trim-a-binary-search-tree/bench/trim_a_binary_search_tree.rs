// Benchmark for #669: recursion, in place, as the Kara ★ arm.
use std::cell::RefCell;
use std::rc::Rc;

struct TreeNode {
    val: i64,
    left: Option<Node>,
    right: Option<Node>,
}

type Node = Rc<RefCell<TreeNode>>;

fn trim_bst(root: Option<Node>, low: i64, high: i64) -> Option<Node> {
    let n = root?;
    let val = n.borrow().val;
    if val < low {
        let right = n.borrow_mut().right.take();
        trim_bst(right, low, high)
    } else if val > high {
        let left = n.borrow_mut().left.take();
        trim_bst(left, low, high)
    } else {
        let left = n.borrow_mut().left.take();
        let right = n.borrow_mut().right.take();
        let left = trim_bst(left, low, high);
        let right = trim_bst(right, low, high);
        {
            let mut b = n.borrow_mut();
            b.left = left;
            b.right = right;
        }
        Some(n)
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn leaf(v: i64) -> Node {
    Rc::new(RefCell::new(TreeNode { val: v, left: None, right: None }))
}

fn bst(values: &[i64]) -> Option<Node> {
    let root = leaf(values[0]);
    for &v in &values[1..] {
        let mut at = root.clone();
        loop {
            let next = {
                let mut b = at.borrow_mut();
                let slot = if v < b.val { &mut b.left } else { &mut b.right };
                match slot {
                    Some(c) => c.clone(),
                    None => {
                        *slot = Some(leaf(v));
                        break;
                    }
                }
            };
            at = next;
        }
    }
    Some(root)
}

fn checksum(root: &Option<Node>) -> i64 {
    let mut sum = 0;
    let mut stack: Vec<Node> = Vec::new();
    if let Some(r) = root {
        stack.push(r.clone());
    }
    while let Some(n) = stack.pop() {
        let b = n.borrow();
        sum = (sum * 31 + b.val) % 1000000007;
        if let Some(r) = &b.right {
            stack.push(r.clone());
        }
        if let Some(l) = &b.left {
            stack.push(l.clone());
        }
    }
    sum
}

fn main() {
    let mut seed: i64 = 669;
    let mut order: Vec<i64> = (0..10000).collect();
    for i in 1..10000usize {
        let j = (next_random(&mut seed) % (i as i64 + 1)) as usize;
        order.swap(i, j);
    }
    let rounds: i64 = 300;
    let mut sum: i64 = 0;
    for r in 0..rounds {
        let low = r * 37 % 10000;
        let high = low + r * 53 % 5000;
        let kept = trim_bst(bst(&order), low, high);
        sum = (sum * 31 + checksum(&kept)) % 1000000007;
    }
    println!("10000 nodes, {} rounds: checksum {}", rounds, sum);
}
