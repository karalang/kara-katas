// Benchmark for #538: Rust mirror of the ★ arm (reverse in order,
// recursively); see convert_bst.kara. The tree is
// `Rc<RefCell<TreeNode>>`, the closest match to a `shared struct`.
use std::cell::RefCell;
use std::rc::Rc;

struct TreeNode {
    val: i64,
    left: Option<Rc<RefCell<TreeNode>>>,
    right: Option<Rc<RefCell<TreeNode>>>,
}

type Node = Option<Rc<RefCell<TreeNode>>>;

fn visit(node: &Node, total: &mut i64) {
    let Some(n) = node else {
        return;
    };
    let mut n = n.borrow_mut();
    visit(&n.right, total);
    *total += n.val;
    n.val = *total;
    visit(&n.left, total);
}

fn convert_bst(root: &Node) -> &Node {
    let mut total = 0;
    visit(root, &mut total);
    root
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn leaf(v: i64) -> Rc<RefCell<TreeNode>> {
    Rc::new(RefCell::new(TreeNode { val: v, left: None, right: None }))
}

// A search tree of distinct values, inserted in the order given; every
// node is also listed in `nodes`, in the same order.
fn build(values: &[i64], nodes: &mut Vec<Rc<RefCell<TreeNode>>>) -> Node {
    let root = leaf(values[0]);
    nodes.push(root.clone());
    for &v in &values[1..] {
        let mut node = root.clone();
        loop {
            let go_left = v < node.borrow().val;
            let next = if go_left { node.borrow().left.clone() } else { node.borrow().right.clone() };
            match next {
                Some(child) => node = child,
                None => {
                    let fresh = leaf(v);
                    if go_left {
                        node.borrow_mut().left = Some(fresh.clone());
                    } else {
                        node.borrow_mut().right = Some(fresh.clone());
                    }
                    nodes.push(fresh);
                    break;
                }
            }
        }
    }
    Some(root)
}

fn main() {
    // 100 random search trees of 10,000 distinct values (the problem's
    // most) from -10,000 to 10,000, built once. Then 50 times over, each
    // tree has its values put back and is converted.
    let trees = 100;
    let mut seed: i64 = 538;
    let mut pool: Vec<i64> = (-10000..10001).collect();
    let mut roots: Vec<Node> = Vec::new();
    let mut lists: Vec<Vec<Rc<RefCell<TreeNode>>>> = Vec::new();
    let mut originals: Vec<Vec<i64>> = Vec::new();
    for _ in 0..trees {
        for i in 0..10000usize {
            let high = next_random(&mut seed);
            let j = i + ((high * 32768 + next_random(&mut seed)) % (20001 - i as i64)) as usize;
            pool.swap(i, j);
        }
        let values = pool[0..10000].to_vec();
        let mut nodes = Vec::new();
        roots.push(build(&values, &mut nodes));
        lists.push(nodes);
        originals.push(values);
    }
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for _ in 0..50 {
        for t in 0..trees {
            for (node, &v) in lists[t].iter().zip(&originals[t]) {
                node.borrow_mut().val = v;
            }
            let top = convert_bst(&roots[t]).as_ref().unwrap().borrow().val;
            total += top;
            checksum = (checksum * 31 + top + 1000000000) % 1000000007;
        }
    }
    println!("{trees} trees of 10000 values, 50 times each: total {total}, checksum {checksum}");
}
