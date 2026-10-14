// Benchmark for #558: Rust mirror of the ★ arm (recursion, then a
// merge); see quad_tree_or.kara. The Kāra `shared enum` is a
// reference-counted handle, so a node here is an Rc<Quad>, and the
// answer shares the subtrees it keeps with the two trees.
use std::rc::Rc;

enum Quad {
    Leaf(bool),
    Split(Rc<Quad>, Rc<Quad>, Rc<Quad>, Rc<Quad>),
}

fn intersect(a: &Rc<Quad>, b: &Rc<Quad>) -> Rc<Quad> {
    match &**a {
        Quad::Leaf(v) => {
            if *v { a.clone() } else { b.clone() }
        }
        Quad::Split(a1, a2, a3, a4) => match &**b {
            Quad::Leaf(w) => {
                if *w { b.clone() } else { a.clone() }
            }
            Quad::Split(b1, b2, b3, b4) => {
                let top_left = intersect(a1, b1);
                let top_right = intersect(a2, b2);
                let bottom_left = intersect(a3, b3);
                let bottom_right = intersect(a4, b4);
                if let (Quad::Leaf(p), Quad::Leaf(q), Quad::Leaf(r), Quad::Leaf(s)) =
                    (&*top_left, &*top_right, &*bottom_left, &*bottom_right)
                {
                    if p == q && q == r && r == s {
                        return Rc::new(Quad::Leaf(*p));
                    }
                }
                Rc::new(Quad::Split(top_left, top_right, bottom_left, bottom_right))
            }
        },
    }
}

// ---- benchmark --------------------------------------------------------------

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

fn count(q: &Quad) -> i64 {
    match q {
        Quad::Leaf(_) => 1,
        Quad::Split(a, b, c, d) => 1 + count(a) + count(b) + count(c) + count(d),
    }
}

fn step(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let n: usize = 64;
    let count_trees: usize = 200;
    let rounds: usize = 300;
    let mut seed: i64 = 558;
    let mut trees: Vec<Rc<Quad>> = Vec::new();
    for _ in 0..count_trees {
        let block = 1usize << (step(&mut seed) % 5);
        let mut grid = vec![vec![0i64; n]; n];
        for br in 0..n / block {
            for bc in 0..n / block {
                let v = if step(&mut seed) % 3 == 0 { 1 } else { 0 };
                for r in 0..block {
                    for c in 0..block {
                        grid[br * block + r][bc * block + c] = v;
                    }
                }
            }
        }
        for _ in 0..40 {
            let r = (step(&mut seed) % n as i64) as usize;
            let c = (step(&mut seed) % n as i64) as usize;
            grid[r][c] = 1 - grid[r][c];
        }
        trees.push(build(&grid, 0, 0, n));
    }
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for round in 0..rounds {
        for i in 0..count_trees {
            let other = (i * 7 + round + 1) % count_trees;
            let nodes = count(&intersect(&trees[i], &trees[other]));
            total += nodes;
            checksum = (checksum * 31 + nodes) % 1000000007;
        }
    }
    println!("{} trees, {} rounds: {} nodes, checksum {}", count_trees, rounds, total, checksum);
}
