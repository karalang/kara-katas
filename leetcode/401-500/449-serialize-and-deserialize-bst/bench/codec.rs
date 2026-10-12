// Benchmark for #449: mirror of codec.kara (preorder, rebuilt with
// bounds) on 10 random search trees of 50,000 values, built once, then
// serialized and deserialized 20 times over.
use std::cell::RefCell;
use std::fmt::Write;
use std::rc::Rc;

struct TreeNode {
    val: i64,
    left: Option<Rc<RefCell<TreeNode>>>,
    right: Option<Rc<RefCell<TreeNode>>>,
}

type Node = Option<Rc<RefCell<TreeNode>>>;

fn write_preorder(node: &Node, out: &mut String) {
    if let Some(n) = node {
        let n = n.borrow();
        if !out.is_empty() {
            out.push(',');
        }
        write!(out, "{}", n.val).unwrap();
        write_preorder(&n.left, out);
        write_preorder(&n.right, out);
    }
}

fn serialize(root: &Node) -> String {
    let mut out = String::new();
    write_preorder(root, &mut out);
    out
}

// Builds the subtree of values from low to high, both inclusive, taking
// them from values[*at] onward.
fn build(values: &[i64], at: &mut usize, low: i64, high: i64) -> Node {
    if *at == values.len() || values[*at] < low || values[*at] > high {
        return None;
    }
    let v = values[*at];
    *at += 1;
    let left = build(values, at, low, v - 1);
    let right = build(values, at, v + 1, high);
    Some(Rc::new(RefCell::new(TreeNode {
        val: v,
        left,
        right,
    })))
}

fn deserialize(data: &str) -> Node {
    let mut values: Vec<i64> = Vec::new();
    if !data.is_empty() {
        for token in data.split(',') {
            values.push(token.parse().expect("a number"));
        }
    }
    let mut at = 0;
    build(&values, &mut at, i64::MIN, i64::MAX)
}

fn insert(root: Node, v: i64) -> Node {
    let fresh = Rc::new(RefCell::new(TreeNode {
        val: v,
        left: None,
        right: None,
    }));
    let Some(top) = root else {
        return Some(fresh);
    };
    let mut node = top.clone();
    loop {
        let next = {
            let n = node.borrow();
            if v < n.val {
                n.left.clone()
            } else {
                n.right.clone()
            }
        };
        match next {
            Some(child) => node = child,
            None => {
                let mut n = node.borrow_mut();
                if v < n.val {
                    n.left = Some(fresh);
                } else {
                    n.right = Some(fresh);
                }
                break;
            }
        }
    }
    Some(top)
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let trees: i64 = 10;
    let n: i64 = 50000;
    let rounds = 20;
    let mut seed: i64 = 449;
    let mut roots: Vec<Node> = Vec::new();
    for t in 0..trees {
        // A shuffle of 0 to n - 1, spread out and shifted per tree.
        let mut values: Vec<i64> = (0..n).map(|i| i * 3 + t).collect();
        for i in 0..n {
            let r = next_random(&mut seed) * 32768 + next_random(&mut seed);
            values.swap(i as usize, (i + r % (n - i)) as usize);
        }
        let mut root: Node = None;
        for v in values {
            root = insert(root, v);
        }
        roots.push(root);
    }
    let mut characters: i64 = 0;
    let mut checksum: i64 = 0;
    for _ in 0..rounds {
        for root in &roots {
            let text = serialize(root);
            let back = deserialize(&text);
            let top = match &back {
                Some(node) => node.borrow().val,
                None => -1,
            };
            characters += text.len() as i64;
            checksum = (checksum * 31 + text.len() as i64 + top) % 1000000007;
        }
    }
    println!(
        "{rounds} rounds on {trees} trees of {n}: {characters} characters, checksum {checksum}"
    );
}
