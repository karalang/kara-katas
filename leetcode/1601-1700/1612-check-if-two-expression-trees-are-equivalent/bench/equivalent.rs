// LeetCode #1612: Check If Two Expression Trees are Equivalent -- the bench
// in Rust, mirroring equivalent.kara: one walk counts the first tree's
// leaves up and the second's down, into one array of 26 counts. Each node
// is an `Rc<RefCell<Node>>`, as in LeetCode's template and as Kāra's
// `shared struct` is counted.

use std::cell::RefCell;
use std::rc::Rc;

struct Node {
    val: char,
    left: Option<Tree>,
    right: Option<Tree>,
}

type Tree = Rc<RefCell<Node>>;

fn tally(node: &Option<Tree>, sign: i32, counts: &mut [i32; 26]) {
    if let Some(n) = node {
        let n = n.borrow();
        if n.val == '+' {
            tally(&n.left, sign, counts);
            tally(&n.right, sign, counts);
        } else {
            counts[(n.val as u8 - b'a') as usize] += sign;
        }
    }
}

fn check_equivalence(root1: Option<Tree>, root2: Option<Tree>) -> bool {
    let mut counts = [0; 26];
    tally(&root1, 1, &mut counts);
    tally(&root2, -1, &mut counts);
    counts.iter().all(|&c| c == 0)
}

fn node(c: char, left: Option<Tree>, right: Option<Tree>) -> Tree {
    Rc::new(RefCell::new(Node { val: c, left, right }))
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn big(seed: &mut i64) -> i64 {
    let a = next_random(seed);
    a * 32768 + next_random(seed)
}

fn random_expression(leaves: &[char], seed: &mut i64) -> Tree {
    let mut loose: Vec<Tree> = leaves.iter().map(|&c| node(c, None, None)).collect();
    while loose.len() > 1 {
        let a = loose.swap_remove((big(seed) % loose.len() as i64) as usize);
        let b = loose.swap_remove((big(seed) % loose.len() as i64) as usize);
        loose.push(node('+', Some(a), Some(b)));
    }
    loose.pop().unwrap()
}

fn main() {
    let mut seed: i64 = 1612;
    let n: i64 = 50000;
    let mut pairs = Vec::new();
    for _ in 0..10 {
        let leaves: Vec<char> = (0..n).map(|_| (b'a' + (next_random(&mut seed) % 26) as u8) as char).collect();
        let mut other = leaves.clone();
        for i in (1..n).rev() {
            let j = big(&mut seed) % (i + 1);
            other.swap(i as usize, j as usize);
        }
        if next_random(&mut seed) % 2 == 0 {
            let i = big(&mut seed) % n;
            other[i as usize] = (b'a' + (next_random(&mut seed) % 26) as u8) as char;
        }
        let one = random_expression(&leaves, &mut seed);
        let two = random_expression(&other, &mut seed);
        pairs.push((one, two));
    }
    let mut check: i64 = 0;
    let mut equivalent = 0;
    for (one, two) in &pairs {
        for k in 0..10 {
            let same = if k % 2 == 0 {
                check_equivalence(Some(one.clone()), Some(two.clone()))
            } else {
                check_equivalence(Some(two.clone()), Some(one.clone()))
            };
            if same {
                equivalent += 1;
            }
            check = (check * 31 + if same { 1 } else { 0 } + 1) % 1000000007;
        }
    }
    println!("10 pairs of 50000 leaves from 26 letters, 100 checks: {equivalent} equivalent, checksum {check}");
}
