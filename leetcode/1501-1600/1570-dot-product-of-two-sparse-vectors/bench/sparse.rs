// LeetCode #1570: Dot Product of Two Sparse Vectors -- bench: the ★ arm
// (index-ordered pairs merged by two pointers) over 20 vectors of 500000
// values, one in 10 of them from 1 to 100 and the rest 0, each made sparse
// once; then the product of every ordered pair of them, 400 products.

struct SparseVector {
    pairs: Vec<(i64, i64)>,
}

impl SparseVector {
    fn new(nums: &[i64]) -> SparseVector {
        SparseVector {
            pairs: nums.iter().enumerate().filter(|(_, &x)| x != 0).map(|(i, &x)| (i as i64, x)).collect(),
        }
    }

    fn dot_product(&self, other: &SparseVector) -> i64 {
        let (mut i, mut j, mut total) = (0, 0, 0i64);
        while i < self.pairs.len() && j < other.pairs.len() {
            let (a, x) = self.pairs[i];
            let (b, y) = other.pairs[j];
            if a == b {
                total += x * y;
                i += 1;
                j += 1;
            } else if a < b {
                i += 1;
            } else {
                j += 1;
            }
        }
        total
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn mix(check: i64, x: i64) -> i64 {
    (check * 31 + x + 1) % 1000000007
}

fn main() {
    let n = 500000;
    let mut seed = 1570;
    let mut vectors: Vec<SparseVector> = Vec::new();
    for _ in 0..20 {
        let nums: Vec<i64> = (0..n)
            .map(|_| {
                let draw = next_random(&mut seed);
                if draw % 10 == 0 { draw / 10 % 100 + 1 } else { 0 }
            })
            .collect();
        vectors.push(SparseVector::new(&nums));
    }
    let (mut check, mut total) = (0i64, 0i64);
    for i in 0..vectors.len() {
        for j in 0..vectors.len() {
            let product = vectors[i].dot_product(&vectors[j]);
            total += product;
            check = mix(check, product);
        }
    }
    println!("400 products of 20 vectors of 500000 values: products sum {}, checksum {}", total, check);
}
