// LeetCode #889 bench: recursion with a table of postorder positions, on
// 4000 random trees of 1,000 nodes, half of them full. The same algorithm
// as construct_from_pre_post.kara, with LeetCode's Rust tree type.
use std::cell::RefCell;
use std::collections::VecDeque;
use std::rc::Rc;

struct TreeNode {
    val: i64,
    left: Option<Rc<RefCell<TreeNode>>>,
    right: Option<Rc<RefCell<TreeNode>>>,
}

type Tree = Option<Rc<RefCell<TreeNode>>>;

fn new_node(val: i64) -> Rc<RefCell<TreeNode>> {
    Rc::new(RefCell::new(TreeNode { val, left: None, right: None }))
}

fn construct_from_pre_post(preorder: &[i64], postorder: &[i64]) -> Tree {
    let mut at = vec![0usize; preorder.len() + 1];
    for (i, &v) in postorder.iter().enumerate() {
        at[v as usize] = i;
    }
    build(preorder, &at, 0, preorder.len() as i64 - 1, 0)
}

// the subtree whose preorder is preorder[lo..=hi] and whose postorder
// starts at post_lo
fn build(preorder: &[i64], at: &[usize], lo: i64, hi: i64, post_lo: i64) -> Tree {
    if lo > hi {
        return None;
    }
    let node = new_node(preorder[lo as usize]);
    if lo < hi {
        let size = at[preorder[lo as usize + 1] as usize] as i64 - post_lo + 1;
        node.borrow_mut().left = build(preorder, at, lo + 1, lo + size, post_lo);
        node.borrow_mut().right = build(preorder, at, lo + size + 1, hi, post_lo + size);
    }
    Some(node)
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn walk(node: &Tree, pre: &mut Vec<i64>, post: &mut Vec<i64>) {
    if let Some(n) = node {
        let n = n.borrow();
        pre.push(n.val);
        walk(&n.left, pre, post);
        walk(&n.right, pre, post);
        post.push(n.val);
    }
}

// as in the Kāra bench: a random tree of n nodes holding 1 to n
fn random_tree(seed: &mut i64, n: i64, full: bool) -> Rc<RefCell<TreeNode>> {
    let mut vals: Vec<i64> = (1..=n).collect();
    for i in 1..n as usize {
        let j = (next_random(seed) % (i as i64 + 1)) as usize;
        vals.swap(i, j);
    }
    let mut nodes = vec![new_node(vals[0])];
    if full {
        let mut leaves = vec![nodes[0].clone()];
        while nodes.len() as i64 + 2 <= n {
            let k = (next_random(seed) % leaves.len() as i64) as usize;
            let leaf = leaves.swap_remove(k);
            let a = new_node(vals[nodes.len()]);
            let b = new_node(vals[nodes.len() + 1]);
            leaf.borrow_mut().left = Some(a.clone());
            leaf.borrow_mut().right = Some(b.clone());
            nodes.push(a.clone());
            nodes.push(b.clone());
            leaves.push(a);
            leaves.push(b);
        }
    } else {
        for k in 1..n as usize {
            let node = new_node(vals[k]);
            loop {
                let parent = nodes[(next_random(seed) % nodes.len() as i64) as usize].clone();
                let mut p = parent.borrow_mut();
                if next_random(seed) % 2 == 0 {
                    if p.left.is_none() {
                        p.left = Some(node.clone());
                        break;
                    }
                } else if p.right.is_none() {
                    p.right = Some(node.clone());
                    break;
                }
            }
            nodes.push(node);
        }
    }
    nodes[0].clone()
}

fn main() {
    let mut seed = 889;
    let mut total = 0i64;
    let mut check = 0i64;
    for c in 0..4000 {
        let full = c % 2 == 0;
        let n = if full { 999 } else { 1000 };
        let tree = Some(random_tree(&mut seed, n, full));
        let mut pre = Vec::new();
        let mut post = Vec::new();
        walk(&tree, &mut pre, &mut post);
        let root = construct_from_pre_post(&pre, &post);
        // the rebuilt tree in level order, 0 for a missing child
        let mut queue: VecDeque<Rc<RefCell<TreeNode>>> = VecDeque::new();
        if let Some(r) = root {
            check = (check * 131 + r.borrow().val) % 1000000007;
            queue.push_back(r);
        }
        while let Some(node) = queue.pop_front() {
            total += 1;
            let node = node.borrow();
            match &node.left {
                Some(l) => {
                    check = (check * 131 + l.borrow().val) % 1000000007;
                    queue.push_back(l.clone());
                }
                None => check = check * 131 % 1000000007,
            }
            match &node.right {
                Some(r) => {
                    check = (check * 131 + r.borrow().val) % 1000000007;
                    queue.push_back(r.clone());
                }
                None => check = check * 131 % 1000000007,
            }
        }
    }
    println!("4000 trees of up to 1000 nodes: {} nodes rebuilt, checksum {}", total, check);
}
