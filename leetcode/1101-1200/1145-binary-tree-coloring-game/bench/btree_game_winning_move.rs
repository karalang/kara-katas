// LeetCode #1145: Binary Tree Coloring Game -- the Rust mirror of
// btree_game_winning_move.kara over LeetCode's own `Rc<RefCell<TreeNode>>`:
// one walk counting every subtree; at the first player's node its two
// sides and the rest of the tree are the three parts blue can take, and
// blue wins when one holds more than half.
use std::cell::RefCell;
use std::rc::Rc;

struct TreeNode {
    val: i32,
    left: Option<Rc<RefCell<TreeNode>>>,
    right: Option<Rc<RefCell<TreeNode>>>,
}

type Node = Option<Rc<RefCell<TreeNode>>>;

fn count(node: &Node, x: i64, sides: &mut (i64, i64)) -> i64 {
    let Some(t) = node else {
        return 0;
    };
    let t = t.borrow();
    let l = count(&t.left, x, sides);
    let r = count(&t.right, x, sides);
    if t.val as i64 == x {
        *sides = (l, r);
    }
    l + r + 1
}

fn btree_game_winning_move(root: &Node, n: i64, x: i64) -> bool {
    let mut sides = (0, 0);
    count(root, x, &mut sides);
    let (l, r) = sides;
    let above = n - 1 - l - r;
    l.max(r).max(above) * 2 > n
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn leaf(v: i32) -> Rc<RefCell<TreeNode>> {
    Rc::new(RefCell::new(TreeNode { val: v, left: None, right: None }))
}

fn random_tree(seed: &mut i64, count: i64) -> Rc<RefCell<TreeNode>> {
    let mut pool: Vec<i32> = (1..count + 1).map(|v| v as i32).collect();
    for j in (1..pool.len()).rev() {
        let k = (next_random(seed) % (j as i64 + 1)) as usize;
        pool.swap(j, k);
    }
    let root = leaf(pool[0]);
    let mut nodes = vec![Rc::clone(&root)];
    for i in 1..count as usize {
        let c = leaf(pool[i]);
        loop {
            let at = &nodes[(next_random(seed) % nodes.len() as i64) as usize];
            let mut at = at.borrow_mut();
            if next_random(seed) % 2 == 0 {
                if at.left.is_none() {
                    at.left = Some(Rc::clone(&c));
                    break;
                }
            } else if at.right.is_none() {
                at.right = Some(Rc::clone(&c));
                break;
            }
        }
        nodes.push(c);
    }
    root
}

fn main() {
    // 20 trees of 99 nodes, built once. Each of 1000 rounds asks every tree
    // about 99 first moves drawn at random.
    let mut seed = 1145;
    let trees: Vec<Node> = (0..20).map(|_| Some(random_tree(&mut seed, 99))).collect();
    let mut wins = 0;
    let mut check = 0;
    for _ in 0..1000 {
        for t in trees.iter() {
            for _ in 0..99 {
                let x = next_random(&mut seed) % 99 + 1;
                let answer = btree_game_winning_move(t, 99, x);
                if answer {
                    wins += 1;
                }
                check = (check * 31 + x + if answer { 1 } else { 0 }) % 1000000007;
            }
        }
    }
    println!("1000 rounds over 20 trees of 99 nodes: blue wins {wins}, checksum {check}");
}
