// Benchmark for #536: the ★ arm (recursive descent); see ../README.md
// § Benchmarks. Mirrors str2tree.kara, with LeetCode's Rust tree type,
// `Option<Rc<RefCell<TreeNode>>>`, for the ★ arm's `shared struct`.

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

// The tree that starts at byte i, leaving i just past it.
fn parse(b: &[u8], i: &mut usize) -> Rc<RefCell<TreeNode>> {
    let mut sign = 1;
    if b[*i] == b'-' {
        sign = -1;
        *i += 1;
    }
    let mut val: i64 = 0;
    while *i < b.len() && b[*i] >= b'0' && b[*i] <= b'9' {
        val = val * 10 + (b[*i] - b'0') as i64;
        *i += 1;
    }
    let n = node(sign * val, None, None);
    if *i < b.len() && b[*i] == b'(' {
        *i += 1;
        n.borrow_mut().left = Some(parse(b, i));
        *i += 1;
    }
    if *i < b.len() && b[*i] == b'(' {
        *i += 1;
        n.borrow_mut().right = Some(parse(b, i));
        *i += 1;
    }
    n
}

fn str2tree(s: &str) -> Tree {
    if s.is_empty() {
        return None;
    }
    let mut i = 0;
    Some(parse(s.as_bytes(), &mut i))
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_tree(seed: &mut i64, n: i64) -> Tree {
    if n == 0 {
        return None;
    }
    let val = next_random(seed) % 2001 - 1000;
    let rest = n - 1;
    let left = if rest == 0 {
        0
    } else if next_random(seed) % 3 == 0 {
        rest
    } else {
        1 + next_random(seed) % rest
    };
    let l = random_tree(seed, left);
    let r = random_tree(seed, rest - left);
    Some(node(val, l, r))
}

fn render(t: &Tree, out: &mut String) {
    let Some(n) = t else {
        return;
    };
    let n = n.borrow();
    out.push_str(&n.val.to_string());
    if n.left.is_some() {
        out.push('(');
        render(&n.left, out);
        out.push(')');
    }
    if n.right.is_some() {
        out.push('(');
        render(&n.right, out);
        out.push(')');
    }
}

fn walk(t: &Tree, stats: &mut [i64; 2]) {
    let Some(n) = t else {
        return;
    };
    let n = n.borrow();
    stats[0] += 1;
    stats[1] = (stats[1] * 31 + n.val + 1000) % 1000000007;
    walk(&n.left, stats);
    walk(&n.right, stats);
}

fn main() {
    let mut seed: i64 = 536;
    let mut strings: Vec<String> = Vec::new();
    for _ in 0..20 {
        let tree = random_tree(&mut seed, 5500);
        let mut s = String::new();
        render(&tree, &mut s);
        strings.push(s);
    }
    let rounds = 100;
    let mut stats = [0i64; 2];
    for _ in 0..rounds {
        for s in strings.iter() {
            walk(&str2tree(s), &mut stats);
        }
    }
    println!("{} strings, {} rounds: {} nodes, checksum {}", strings.len(), rounds, stats[0], stats[1]);
}
