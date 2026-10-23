// LeetCode #894 bench: the ★ arm (recursion with a memo, the trees sharing
// their subtrees) asked 1,500 times for every full tree of 19 nodes; each
// tree is walked in preorder into a checksum. The same algorithm as
// all_possible_fbt.kara, with LeetCode's Rust tree type.
use std::cell::RefCell;
use std::collections::HashMap;
use std::rc::Rc;

struct TreeNode {
    #[allow(dead_code)]
    val: i64,
    left: Option<Rc<RefCell<TreeNode>>>,
    right: Option<Rc<RefCell<TreeNode>>>,
}

type Tree = Rc<RefCell<TreeNode>>;

fn all_possible_fbt(n: i64) -> Vec<Tree> {
    let mut memo: HashMap<i64, Vec<Tree>> = HashMap::new();
    build(n, &mut memo)
}

fn build(n: i64, memo: &mut HashMap<i64, Vec<Tree>>) -> Vec<Tree> {
    if let Some(trees) = memo.get(&n) {
        return trees.clone();
    }
    let mut out: Vec<Tree> = Vec::new();
    if n == 1 {
        out.push(Rc::new(RefCell::new(TreeNode { val: 0, left: None, right: None })));
    } else if n % 2 == 1 {
        let mut left = 1;
        while left < n - 1 {
            let lefts = build(left, memo);
            let rights = build(n - 1 - left, memo);
            for l in &lefts {
                for r in &rights {
                    out.push(Rc::new(RefCell::new(TreeNode {
                        val: 0,
                        left: Some(l.clone()),
                        right: Some(r.clone()),
                    })));
                }
            }
            left += 2;
        }
    }
    memo.insert(n, out.clone());
    out
}

// the tree's preorder code, 1 for a node with children and 0 for a leaf,
// folded into a hash
fn code(node: &Option<Tree>, h: i64) -> i64 {
    match node {
        None => h,
        Some(t) => {
            let t = t.borrow();
            if t.left.is_none() {
                h * 3 % 1000000007
            } else {
                code(&t.right, code(&t.left, (h * 3 + 1) % 1000000007))
            }
        }
    }
}

fn main() {
    let mut trees = 0;
    let mut check = 0;
    for _ in 0..1500 {
        let all = all_possible_fbt(19);
        trees += all.len();
        for t in &all {
            check = (check * 131 + code(&Some(t.clone()), 1)) % 1000000007;
        }
    }
    println!("1500 calls for 19 nodes: {} trees, checksum {}", trees, check);
}
