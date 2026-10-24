// LeetCode #938: Range Sum of BST -- bench: recursion that skips
// subtrees. Mirrors range_sum_bst.kara, .c, .py and go-seq/. The tree
// is LeetCode's Rust one, `Option<Rc<RefCell<TreeNode>>>`, counted
// references like a Kāra `shared struct`.
use std::cell::RefCell;
use std::rc::Rc;

struct TreeNode {
    val: i64,
    left: Option<Rc<RefCell<TreeNode>>>,
    right: Option<Rc<RefCell<TreeNode>>>,
}

fn new_node(val: i64) -> Rc<RefCell<TreeNode>> {
    Rc::new(RefCell::new(TreeNode {
        val,
        left: None,
        right: None,
    }))
}

fn range_sum_bst(root: &Option<Rc<RefCell<TreeNode>>>, low: i64, high: i64) -> i64 {
    match root {
        None => 0,
        Some(node) => {
            let n = node.borrow();
            if n.val < low {
                range_sum_bst(&n.right, low, high)
            } else if n.val > high {
                range_sum_bst(&n.left, low, high)
            } else {
                n.val + range_sum_bst(&n.left, low, high) + range_sum_bst(&n.right, low, high)
            }
        }
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let rounds: i64 = 20;
    let count: i64 = 20;
    let queries: i64 = 50;
    let mut seed: i64 = 938;
    let mut trees: Vec<Option<Rc<RefCell<TreeNode>>>> = Vec::new();
    let mut lows: Vec<i64> = Vec::new();
    let mut highs: Vec<i64> = Vec::new();
    let mut pool: Vec<i64> = (1..100001).collect();
    for _ in 0..count {
        for i in 0..20000 {
            let j = i + next_random(&mut seed) % (100000 - i);
            pool.swap(i as usize, j as usize);
        }
        let root = new_node(pool[0]);
        for &v in &pool[1..20000] {
            let mut cur = root.clone();
            loop {
                let next = {
                    let mut c = cur.borrow_mut();
                    let side = if v < c.val { &mut c.left } else { &mut c.right };
                    match side {
                        Some(child) => child.clone(),
                        None => {
                            *side = Some(new_node(v));
                            break;
                        }
                    }
                };
                cur = next;
            }
        }
        trees.push(Some(root));
        for _ in 0..queries {
            let a = 1 + next_random(&mut seed) % 100000;
            let b = 1 + next_random(&mut seed) % 100000;
            lows.push(a.min(b));
            highs.push(a.max(b));
        }
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for i in 0..count {
            let c = ((r + i) % count) as usize;
            for q in 0..queries as usize {
                let k = c * queries as usize + q;
                let s = range_sum_bst(&trees[c], lows[k], highs[k]);
                total += s;
                check = (check * 1000003 + s) % 1000000007;
            }
        }
    }
    println!("{rounds} rounds over {count} trees of 20000 nodes, {queries} ranges each: sums adding to {total}, checksum {check}");
}
