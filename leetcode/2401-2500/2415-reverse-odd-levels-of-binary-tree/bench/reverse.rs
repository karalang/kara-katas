// LeetCode #2415: Reverse Odd Levels of Binary Tree -- the bench, the ★ arm
// in Rust: mirror pairs walked down together, the values of each pair on
// an odd level swapped. The nodes are `Rc<RefCell<TreeNode>>`, LeetCode's
// and the model of Kāra's `shared struct`.
use std::cell::RefCell;
use std::rc::Rc;

type Link = Option<Rc<RefCell<TreeNode>>>;

struct TreeNode {
    val: i32,
    left: Link,
    right: Link,
}

fn swap_pairs(a: &Link, b: &Link, odd: bool) {
    if let (Some(x), Some(y)) = (a, b) {
        if odd {
            let t = x.borrow().val;
            x.borrow_mut().val = y.borrow().val;
            y.borrow_mut().val = t;
        }
        let (x, y) = (x.borrow(), y.borrow());
        swap_pairs(&x.left, &y.right, !odd);
        swap_pairs(&x.right, &y.left, !odd);
    }
}

fn reverse_odd_levels(root: Link) -> Link {
    if let Some(r) = &root {
        let r = r.borrow();
        swap_pairs(&r.left, &r.right, true);
    }
    root
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn edge(root: &Rc<RefCell<TreeNode>>, left: bool) -> i64 {
    let mut at = root.clone();
    loop {
        let next = if left { at.borrow().left.clone() } else { at.borrow().right.clone() };
        match next {
            Some(c) => at = c,
            None => return at.borrow().val as i64,
        }
    }
}

fn main() {
    let mut seed = 2415;
    let mut roots: Vec<Rc<RefCell<TreeNode>>> = Vec::new();
    for _ in 0..10 {
        let nodes: Vec<Rc<RefCell<TreeNode>>> = (0..16383)
            .map(|_| {
                let v = ((next_random(&mut seed) * 32768 + next_random(&mut seed)) % 100000) as i32;
                Rc::new(RefCell::new(TreeNode { val: v, left: None, right: None }))
            })
            .collect();
        for i in 0..8191 {
            let mut n = nodes[i].borrow_mut();
            n.left = Some(nodes[2 * i + 1].clone());
            n.right = Some(nodes[2 * i + 2].clone());
        }
        roots.push(nodes[0].clone());
    }
    let mut check: i64 = 0;
    for p in 0..1000 {
        for root in &roots {
            let r = reverse_odd_levels(Some(root.clone())).unwrap();
            let a = r.borrow().left.as_ref().unwrap().borrow().val as i64;
            let b = r.borrow().right.as_ref().unwrap().borrow().val as i64;
            check = (check * 31 + a + p) % 1000000007;
            check = (check * 31 + b + edge(&r, true) + edge(&r, false)) % 1000000007;
        }
    }
    println!("1000 passes over 10 trees of 2^14 - 1 nodes: checksum {}", check);
}
