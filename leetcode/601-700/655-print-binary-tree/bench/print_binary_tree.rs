// Benchmark for #655: each node placed from its parent, as the Kara ★ arm.
use std::cell::RefCell;
use std::rc::Rc;

struct TreeNode {
    val: i64,
    left: Option<Rc<RefCell<TreeNode>>>,
    right: Option<Rc<RefCell<TreeNode>>>,
}

type Node = Rc<RefCell<TreeNode>>;

fn print_tree(root: &Option<Node>) -> Vec<Vec<String>> {
    let h = height(root) - 1;
    let columns = (1usize << (h + 1)) - 1;
    let mut grid: Vec<Vec<String>> = Vec::new();
    for _ in 0..h + 1 {
        let mut row: Vec<String> = Vec::new();
        for _ in 0..columns {
            row.push(String::new());
        }
        grid.push(row);
    }
    place(root, 0, (columns - 1) / 2, h, &mut grid);
    grid
}

fn height(node: &Option<Node>) -> i64 {
    match node {
        None => 0,
        Some(n) => {
            let b = n.borrow();
            1 + height(&b.left).max(height(&b.right))
        }
    }
}

fn place(node: &Option<Node>, row: i64, column: usize, h: i64, grid: &mut Vec<Vec<String>>) {
    if let Some(n) = node {
        let b = n.borrow();
        grid[row as usize][column] = b.val.to_string();
        if row < h {
            let step = 1usize << (h - row - 1);
            place(&b.left, row + 1, column - step, h, grid);
            place(&b.right, row + 1, column + step, h, grid);
        }
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_tree(levels: i64, chance: i64, seed: &mut i64) -> Option<Node> {
    if levels == 0 {
        return None;
    }
    let n = Rc::new(RefCell::new(TreeNode { val: next_random(seed) % 199 - 99, left: None, right: None }));
    if next_random(seed) % 100 < chance {
        n.borrow_mut().left = random_tree(levels - 1, chance, seed);
    }
    if next_random(seed) % 100 < chance {
        n.borrow_mut().right = random_tree(levels - 1, chance, seed);
    }
    Some(n)
}

fn main() {
    let inputs = 8;
    let rounds = 10000;
    let mut seed: i64 = 655;
    let mut trees: Vec<Option<Node>> = Vec::new();
    for _ in 0..inputs {
        trees.push(random_tree(10, 85, &mut seed));
    }
    let mut cells = 0;
    let mut checksum: i64 = 0;
    for r in 0..rounds {
        let grid = print_tree(&trees[(r * 3) % inputs]);
        let mut filled = 0;
        let mut chars = 0;
        for row in grid.iter() {
            for cell in row.iter() {
                if !cell.is_empty() {
                    filled += 1;
                    chars += cell.len() as i64;
                }
            }
        }
        cells += grid.len() * grid[0].len();
        checksum = (checksum * 31 + filled * 1000 + chars) % 1000000007;
    }
    println!("{inputs} trees, {rounds} rounds: {cells} cells, checksum {checksum}");
}
