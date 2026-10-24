// Benchmark: LeetCode #951 Flip Equivalent Binary Trees -- the ★ arm,
// both pairings tried, on pairs of trees of 100 nodes, LeetCode's
// largest. Mirrors flip_equiv.kara, .c, .py and go-seq/. The tree is
// LeetCode's Rust shape, `Option<Rc<RefCell<TreeNode>>>`, reference
// counted as Kāra's `shared struct` is.
use std::cell::RefCell;
use std::rc::Rc;

struct TreeNode {
    val: i64,
    left: Option<Rc<RefCell<TreeNode>>>,
    right: Option<Rc<RefCell<TreeNode>>>,
}

type Tree = Option<Rc<RefCell<TreeNode>>>;

fn node(val: i64, left: Tree, right: Tree) -> Rc<RefCell<TreeNode>> {
    Rc::new(RefCell::new(TreeNode { val, left, right }))
}

fn flip_equiv(root1: &Tree, root2: &Tree) -> bool {
    match (root1, root2) {
        (None, None) => true,
        (Some(a), Some(b)) => {
            let (a, b) = (a.borrow(), b.borrow());
            a.val == b.val
                && ((flip_equiv(&a.left, &b.left) && flip_equiv(&a.right, &b.right))
                    || (flip_equiv(&a.left, &b.right) && flip_equiv(&a.right, &b.left)))
        }
        _ => false,
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_tree(values: &[i64], seed: &mut i64) -> Rc<RefCell<TreeNode>> {
    let root = node(values[0], None, None);
    for &v in &values[1..] {
        let new = node(v, None, None);
        let mut cur = root.clone();
        loop {
            let go_left = next_random(seed) % 2 == 0;
            let next = if go_left { cur.borrow().left.clone() } else { cur.borrow().right.clone() };
            match next {
                Some(child) => cur = child,
                None => {
                    if go_left {
                        cur.borrow_mut().left = Some(new);
                    } else {
                        cur.borrow_mut().right = Some(new);
                    }
                    break;
                }
            }
        }
    }
    root
}

fn flipped_copy(t: &Tree, rename: &[i64], seed: &mut i64) -> Tree {
    let t = t.as_ref()?.borrow();
    let l = flipped_copy(&t.left, rename, seed);
    let r = flipped_copy(&t.right, rename, seed);
    if next_random(seed) % 2 == 0 {
        Some(node(rename[t.val as usize], l, r))
    } else {
        Some(node(rename[t.val as usize], r, l))
    }
}

fn main() {
    let (rounds, count, n): (i64, usize, i64) = (50000, 20, 100);
    let mut seed = 951;
    let mut firsts: Vec<Tree> = Vec::new();
    let mut seconds: Vec<Tree> = Vec::new();
    for c in 0..count {
        let mut values: Vec<i64> = (0..n).collect();
        for i in 0..n {
            let j = i + next_random(&mut seed) % (n - i);
            values.swap(i as usize, j as usize);
        }
        let t = Some(random_tree(&values, &mut seed));
        let mut rename: Vec<i64> = (0..n).collect();
        if c % 2 == 1 {
            let a = next_random(&mut seed) % n;
            let b = next_random(&mut seed) % n;
            rename[a as usize] = b;
            rename[b as usize] = a;
        }
        seconds.push(flipped_copy(&t, &rename, &mut seed));
        firsts.push(t);
    }
    let mut yes: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds as usize {
        for i in 0..count {
            let k = (r + i) % count;
            let bit = if flip_equiv(&firsts[k], &seconds[k]) { 1 } else { 0 };
            yes += bit;
            check = (check * 31 + bit + k as i64) % 1000000007;
        }
    }
    println!("{rounds} rounds over {count} pairs of trees of {n} nodes: {yes} flip equivalent, checksum {check}");
}
