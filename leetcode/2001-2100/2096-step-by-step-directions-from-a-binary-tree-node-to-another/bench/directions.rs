// LeetCode #2096: Step-By-Step Directions From a Binary Tree Node to
// Another -- Rust mirror of the ★ arm's benchmark (directions.kara): the
// same random tree of 100000 nodes and 1000 questions, each answered by the
// same two depth-first searches. The nodes are `Rc<RefCell<TreeNode>>`, the
// model of Kāra's `shared struct`.
use std::cell::RefCell;
use std::rc::Rc;

type Link = Option<Rc<RefCell<TreeNode>>>;

struct TreeNode {
    val: i64,
    left: Link,
    right: Link,
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide_random(seed: &mut i64) -> i64 {
    let hi = next_random(seed);
    hi * 32768 + next_random(seed)
}

fn way_to(node: &Link, target: i64, way: &mut String) -> bool {
    let Some(n) = node else {
        return false;
    };
    let n = n.borrow();
    if n.val == target {
        return true;
    }
    way.push('L');
    if way_to(&n.left, target, way) {
        return true;
    }
    way.pop();
    way.push('R');
    if way_to(&n.right, target, way) {
        return true;
    }
    way.pop();
    false
}

fn get_directions(root: &Link, start_value: i64, dest_value: i64) -> String {
    let mut from = String::new();
    let mut to = String::new();
    way_to(root, start_value, &mut from);
    way_to(root, dest_value, &mut to);
    let a: Vec<char> = from.chars().collect();
    let b: Vec<char> = to.chars().collect();
    let mut common = 0;
    while common < a.len() && common < b.len() && a[common] == b[common] {
        common += 1;
    }
    let mut out = "U".repeat(a.len() - common);
    for &c in &b[common..] {
        out.push(c);
    }
    out
}

fn main() {
    let mut seed = 2096;
    let n: i64 = 100000;
    let mut values: Vec<i64> = (1..n + 1).collect();
    for i in (1..n as usize).rev() {
        let j = (wide_random(&mut seed) % (i as i64 + 1)) as usize;
        values.swap(i, j);
    }
    let nodes: Vec<Rc<RefCell<TreeNode>>> = values
        .iter()
        .map(|&v| Rc::new(RefCell::new(TreeNode { val: v, left: None, right: None })))
        .collect();
    for k in 1..n as usize {
        let mut at = nodes[(wide_random(&mut seed) % k as i64) as usize].clone();
        loop {
            if next_random(&mut seed) % 2 == 0 {
                let child = at.borrow().left.clone();
                match child {
                    Some(c) => at = c,
                    None => {
                        at.borrow_mut().left = Some(nodes[k].clone());
                        break;
                    }
                }
            } else {
                let child = at.borrow().right.clone();
                match child {
                    Some(c) => at = c,
                    None => {
                        at.borrow_mut().right = Some(nodes[k].clone());
                        break;
                    }
                }
            }
        }
    }
    let root = Some(nodes[0].clone());
    let mut steps = 0;
    let mut check: i64 = 0;
    for _ in 0..1000 {
        let s = wide_random(&mut seed) % n + 1;
        let t = (s + wide_random(&mut seed) % (n - 1)) % n + 1;
        let way = get_directions(&root, s, t);
        steps += way.len();
        for c in way.chars() {
            check = (check * 31 + c as i64) % 1000000007;
        }
    }
    println!("1000 answers: {} steps, checksum {}", steps, check);
}
