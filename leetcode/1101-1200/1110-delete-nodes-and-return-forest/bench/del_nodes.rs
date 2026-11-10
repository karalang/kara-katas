// LeetCode #1110: Delete Nodes And Return Forest -- the bench in Rust:
// the ★ arm over LeetCode's own `Rc<RefCell<TreeNode>>`, the same 16
// trees of 1000 nodes and the same rounds.

use std::cell::RefCell;
use std::collections::HashSet;
use std::rc::Rc;

struct TreeNode {
    val: i32,
    left: Option<Rc<RefCell<TreeNode>>>,
    right: Option<Rc<RefCell<TreeNode>>>,
}

type Node = Option<Rc<RefCell<TreeNode>>>;

fn prune(node: Node, parent_gone: bool, gone: &HashSet<i32>, roots: &mut Vec<Node>) -> Node {
    let n = node?;
    let deleted = gone.contains(&n.borrow().val);
    if parent_gone && !deleted {
        roots.push(Some(n.clone()));
    }
    let left = n.borrow_mut().left.take();
    let left = prune(left, deleted, gone, roots);
    n.borrow_mut().left = left;
    let right = n.borrow_mut().right.take();
    let right = prune(right, deleted, gone, roots);
    n.borrow_mut().right = right;
    if deleted { None } else { Some(n) }
}

fn del_nodes(root: Node, to_delete: Vec<i32>) -> Vec<Node> {
    let gone: HashSet<i32> = to_delete.iter().cloned().collect();
    let mut roots = Vec::new();
    prune(root, true, &gone, &mut roots);
    roots
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

struct Shape {
    values: Vec<i32>,
    left: Vec<i64>,
    right: Vec<i64>,
}

fn shape(seed: &mut i64) -> Shape {
    let mut values: Vec<i32> = (1..1001).collect();
    for i in 0..1000 {
        let j = i + (next_random(seed) % (1000 - i as i64)) as usize;
        values.swap(i, j);
    }
    let mut left = vec![-1i64; 1000];
    let mut right = vec![-1i64; 1000];
    for k in 1..1000i64 {
        loop {
            let at = (next_random(seed) % k) as usize;
            if next_random(seed) % 2 == 0 {
                if left[at] < 0 {
                    left[at] = k;
                    break;
                }
            } else if right[at] < 0 {
                right[at] = k;
                break;
            }
        }
    }
    Shape { values, left, right }
}

fn build(s: &Shape) -> Node {
    let nodes: Vec<Rc<RefCell<TreeNode>>> = s
        .values
        .iter()
        .map(|&v| Rc::new(RefCell::new(TreeNode { val: v, left: None, right: None })))
        .collect();
    for k in 0..1000 {
        if s.left[k] >= 0 {
            nodes[k].borrow_mut().left = Some(nodes[s.left[k] as usize].clone());
        }
        if s.right[k] >= 0 {
            nodes[k].borrow_mut().right = Some(nodes[s.right[k] as usize].clone());
        }
    }
    Some(nodes[0].clone())
}

fn main() {
    let mut seed = 1110;
    let shapes: Vec<Shape> = (0..16).map(|_| shape(&mut seed)).collect();
    let mut trees = 0;
    let mut check: i64 = 0;
    for round in 0..200 {
        for j in 0..shapes.len() {
            let third = (round + j as i64) % 3;
            let to_delete: Vec<i32> = (1..1001i64).filter(|v| v % 3 == third).map(|v| v as i32).collect();
            let roots = del_nodes(build(&shapes[j]), to_delete);
            trees += roots.len();
            for r in &roots {
                check = (check * 31 + r.as_ref().unwrap().borrow().val as i64) % 1000000007;
            }
        }
    }
    println!("200 rounds over 16 trees of 1000 nodes: {} trees, checksum {}", trees, check);
}
