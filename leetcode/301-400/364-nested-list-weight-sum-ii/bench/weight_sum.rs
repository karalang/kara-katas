// Benchmark for #364 -- mirror of weight_sum.kara.

enum Nested {
    Int(i64),
    List(Vec<Nested>),
}

fn max_depth(list: &[Nested], depth: i64) -> i64 {
    let mut deepest = 0;
    for item in list {
        match item {
            Nested::Int(_) => deepest = deepest.max(depth),
            Nested::List(inner) => deepest = deepest.max(max_depth(inner, depth + 1)),
        }
    }
    deepest
}

fn weighted(list: &[Nested], depth: i64, top: i64) -> i64 {
    let mut total = 0;
    for item in list {
        match item {
            Nested::Int(v) => total += v * (top - depth + 1),
            Nested::List(inner) => total += weighted(inner, depth + 1, top),
        }
    }
    total
}

fn depth_sum_inverse(list: &[Nested]) -> i64 {
    let top = max_depth(list, 1);
    weighted(list, 1, top)
}

fn next(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn build(seed: &mut i64, depth: i64) -> Vec<Nested> {
    let n = next(seed) % 13;
    let mut out = Vec::new();
    for _ in 0..n {
        if depth < 14 && next(seed) % 3 == 0 {
            out.push(Nested::List(build(seed, depth + 1)));
        } else {
            out.push(Nested::Int(next(seed) % 201 - 100));
        }
    }
    out
}

fn main() {
    let mut seed: i64 = 364;
    let mut checksum: i64 = 0;
    for _ in 0..10 {
        let list = build(&mut seed, 1);
        for _ in 0..20 {
            checksum = (checksum * 31 + depth_sum_inverse(&list) + 1000000000000000) % 1000000007;
        }
    }
    println!("checksum {checksum}");
}
