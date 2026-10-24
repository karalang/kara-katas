// Benchmark: LeetCode #971 Flip Binary Tree To Match Preorder Traversal
// -- the ★ arm, one walk flipping where the voyage says, on 200 random
// trees of 100 nodes. Mirrors flip_match_voyage.kara, .c, .py and
// go-seq/. The tree is LeetCode's `Option<Rc<RefCell<TreeNode>>>`.

use std::cell::RefCell;
use std::rc::Rc;

type Tree = Option<Rc<RefCell<TreeNode>>>;

struct TreeNode {
    val: i64,
    left: Tree,
    right: Tree,
}

fn new_node(val: i64) -> Rc<RefCell<TreeNode>> {
    Rc::new(RefCell::new(TreeNode { val, left: None, right: None }))
}

fn walk(t: &Tree, voyage: &[i64], i: &mut usize, flipped: &mut Vec<i64>) -> bool {
    match t {
        None => true,
        Some(node) => {
            let node = node.borrow();
            if node.val != voyage[*i] {
                return false;
            }
            *i += 1;
            let wrong_left = match &node.left {
                Some(l) => l.borrow().val != voyage[*i],
                None => false,
            };
            if wrong_left {
                flipped.push(node.val);
                walk(&node.right, voyage, i, flipped) && walk(&node.left, voyage, i, flipped)
            } else {
                walk(&node.left, voyage, i, flipped) && walk(&node.right, voyage, i, flipped)
            }
        }
    }
}

fn flip_match_voyage(root: &Tree, voyage: &[i64]) -> Vec<i64> {
    let mut i = 0;
    let mut flipped = Vec::new();
    if walk(root, voyage, &mut i, &mut flipped) {
        flipped
    } else {
        vec![-1]
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_permutation(n: i64, seed: &mut i64) -> Vec<i64> {
    let mut a: Vec<i64> = (1..=n).collect();
    let mut i = n - 1;
    while i > 0 {
        let j = next_random(seed) % (i + 1);
        a.swap(i as usize, j as usize);
        i -= 1;
    }
    a
}

fn random_tree(vals: &[i64], seed: &mut i64) -> Rc<RefCell<TreeNode>> {
    let root = new_node(vals[0]);
    for &v in &vals[1..] {
        let node = new_node(v);
        let mut cur = root.clone();
        loop {
            let next = if next_random(seed) % 2 == 0 {
                let mut c = cur.borrow_mut();
                match &c.left {
                    Some(l) => l.clone(),
                    None => {
                        c.left = Some(node);
                        break;
                    }
                }
            } else {
                let mut c = cur.borrow_mut();
                match &c.right {
                    Some(r) => r.clone(),
                    None => {
                        c.right = Some(node);
                        break;
                    }
                }
            };
            cur = next;
        }
    }
    root
}

fn random_voyage(t: &Tree, seed: &mut i64, out: &mut Vec<i64>) {
    if let Some(node) = t {
        let node = node.borrow();
        out.push(node.val);
        if next_random(seed) % 2 == 0 {
            random_voyage(&node.left, seed, out);
            random_voyage(&node.right, seed, out);
        } else {
            random_voyage(&node.right, seed, out);
            random_voyage(&node.left, seed, out);
        }
    }
}

fn main() {
    let rounds = 1000;
    let count = 200;
    let mut seed = 971;
    let mut trees: Vec<Tree> = Vec::new();
    let mut voyages: Vec<Vec<i64>> = Vec::new();
    for c in 0..count {
        let vals = random_permutation(100, &mut seed);
        let root = Some(random_tree(&vals, &mut seed));
        let mut voyage = Vec::new();
        random_voyage(&root, &mut seed, &mut voyage);
        if c % 4 == 3 {
            let i = (next_random(&mut seed) % 100) as usize;
            let j = (next_random(&mut seed) % 100) as usize;
            voyage.swap(i, j);
        }
        trees.push(root);
        voyages.push(voyage);
    }
    let mut flips: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for s in 0..count {
            let c = (r + s) % count;
            for v in flip_match_voyage(&trees[c], &voyages[c]) {
                flips += 1;
                check = (check * 31 + v + 2) % 1000000007;
            }
        }
    }
    println!("{rounds} rounds over {count} trees of 100 nodes: {flips} values, checksum {check}");
}
