// Benchmark for #654: a stack of the right spine, as the Kara ★ arm.
use std::cell::RefCell;
use std::rc::Rc;

struct TreeNode {
    val: i64,
    left: Option<Rc<RefCell<TreeNode>>>,
    right: Option<Rc<RefCell<TreeNode>>>,
}

type Node = Rc<RefCell<TreeNode>>;

fn construct_maximum_binary_tree(nums: &[i64]) -> Option<Node> {
    let mut stack: Vec<Node> = Vec::new();
    for &x in nums {
        let node = Rc::new(RefCell::new(TreeNode { val: x, left: None, right: None }));
        while !stack.is_empty() && stack[stack.len() - 1].borrow().val < x {
            node.borrow_mut().left = stack.pop();
        }
        if let Some(top) = stack.last() {
            top.borrow_mut().right = Some(node.clone());
        }
        stack.push(node);
    }
    stack.first().cloned()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let inputs = 8;
    let rounds = 100;
    let n: i64 = 200000;
    let mut seed: i64 = 654;
    let mut lists: Vec<Vec<i64>> = Vec::new();
    for _ in 0..inputs {
        let mut nums: Vec<i64> = (0..n).collect();
        let mut i = n - 1;
        while i > 0 {
            let hi = next_random(&mut seed);
            let j = (hi * 32768 + next_random(&mut seed)) % (i + 1);
            nums.swap(i as usize, j as usize);
            i -= 1;
        }
        lists.push(nums);
    }
    let mut checksum: i64 = 0;
    for r in 0..rounds {
        let root = construct_maximum_binary_tree(&lists[(r * 3) % inputs]);
        let mut left = 0;
        let mut at = root.clone();
        while let Some(node) = at {
            left += 1;
            at = node.borrow().left.clone();
        }
        let mut right = 0;
        let mut at = root.clone();
        while let Some(node) = at {
            right += 1;
            at = node.borrow().right.clone();
        }
        checksum = (checksum * 31 + left * 1000 + right) % 1000000007;
    }
    println!("{inputs} orders of {n}, {rounds} rounds: checksum {checksum}");
}
