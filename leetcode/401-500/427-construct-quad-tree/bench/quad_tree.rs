// Benchmark for #427: mirror of quad_tree.kara (divide, then merge).
// The Kāra `shared enum` is a reference-counted handle, so a node here is
// an Rc<Quad>; four merged leaves are dropped and replaced by one.
use std::rc::Rc;

enum Quad {
    Leaf(bool),
    Split(Rc<Quad>, Rc<Quad>, Rc<Quad>, Rc<Quad>),
}

fn build(grid: &[Vec<i64>], row: usize, col: usize, size: usize) -> Rc<Quad> {
    if size == 1 {
        return Rc::new(Quad::Leaf(grid[row][col] == 1));
    }
    let half = size / 2;
    let top_left = build(grid, row, col, half);
    let top_right = build(grid, row, col + half, half);
    let bottom_left = build(grid, row + half, col, half);
    let bottom_right = build(grid, row + half, col + half, half);
    if let (Quad::Leaf(a), Quad::Leaf(b), Quad::Leaf(c), Quad::Leaf(d)) =
        (&*top_left, &*top_right, &*bottom_left, &*bottom_right)
    {
        if a == b && b == c && c == d {
            return Rc::new(Quad::Leaf(*a));
        }
    }
    Rc::new(Quad::Split(top_left, top_right, bottom_left, bottom_right))
}

fn construct(grid: &[Vec<i64>]) -> Rc<Quad> {
    build(grid, 0, 0, grid.len())
}

fn step(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn count(q: &Quad) -> i64 {
    match q {
        Quad::Leaf(_) => 1,
        Quad::Split(a, b, c, d) => 1 + count(a) + count(b) + count(c) + count(d),
    }
}

fn main() {
    let n: i64 = 64;
    let rounds: i64 = std::env::args().nth(1).map_or(20000, |s| s.parse().unwrap());
    let mut seed: i64 = 427;
    let mut grid = vec![vec![0i64; n as usize]; n as usize];
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for _ in 0..rounds {
        let size = 1i64 << (step(&mut seed) % 7);
        let top = step(&mut seed) % (n / size) * size;
        let left = step(&mut seed) % (n / size) * size;
        let v = step(&mut seed) % 2;
        for r in top..top + size {
            for c in left..left + size {
                grid[r as usize][c as usize] = v;
            }
        }
        let r = (step(&mut seed) % n) as usize;
        let c = (step(&mut seed) % n) as usize;
        grid[r][c] = 1 - grid[r][c];
        let nodes = count(&construct(&grid));
        total += nodes;
        checksum = (checksum * 31 + nodes) % 1000000007;
    }
    println!("{} rounds on a {} by {} grid: {} nodes, checksum {}", rounds, n, n, total, checksum);
}
