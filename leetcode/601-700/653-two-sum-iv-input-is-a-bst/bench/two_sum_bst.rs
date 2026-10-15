// Benchmark for #653: in order, then two ends, as the Kara ★ arm.
use std::cell::RefCell;
use std::collections::HashSet;
use std::rc::Rc;

struct TreeNode {
    val: i64,
    left: Option<Rc<RefCell<TreeNode>>>,
    right: Option<Rc<RefCell<TreeNode>>>,
}

type Node = Rc<RefCell<TreeNode>>;

fn find_target(root: &Option<Node>, k: i64) -> bool {
    let mut values: Vec<i64> = Vec::new();
    in_order(root, &mut values);
    if values.len() < 2 {
        return false;
    }
    let mut low = 0;
    let mut high = values.len() - 1;
    while low < high {
        let sum = values[low] + values[high];
        if sum == k {
            return true;
        } else if sum < k {
            low += 1;
        } else {
            high -= 1;
        }
    }
    false
}

fn in_order(node: &Option<Node>, values: &mut Vec<i64>) {
    if let Some(n) = node {
        let b = n.borrow();
        in_order(&b.left, values);
        values.push(b.val);
        in_order(&b.right, values);
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let size = 200000;
    let queries = 300;
    let mut seed: i64 = 653;
    let mut seen: HashSet<i64> = HashSet::new();
    let mut root: Option<Node> = None;
    let mut count = 0;
    while count < size {
        let hi = next_random(&mut seed);
        let v = (hi * 32768 + next_random(&mut seed)) % 1000000;
        if !seen.insert(v) {
            continue;
        }
        count += 1;
        let c = Rc::new(RefCell::new(TreeNode { val: v, left: None, right: None }));
        let Some(r) = root.clone() else {
            root = Some(c);
            continue;
        };
        let mut node = r;
        loop {
            let next = {
                let mut b = node.borrow_mut();
                let slot = if v < b.val { &mut b.left } else { &mut b.right };
                match slot {
                    Some(n) => n.clone(),
                    None => {
                        *slot = Some(c);
                        break;
                    }
                }
            };
            node = next;
        }
    }
    let mut found = 0;
    let mut checksum: i64 = 0;
    for _ in 0..queries {
        let hi = next_random(&mut seed);
        let k = (hi * 32768 + next_random(&mut seed)) % 3000000;
        let hit = find_target(&root, k);
        if hit {
            found += 1;
        }
        checksum = (checksum * 2 + if hit { 1 } else { 0 }) % 1000000007;
    }
    println!("{size} values, {queries} targets: {found} found, checksum {checksum}");
}
