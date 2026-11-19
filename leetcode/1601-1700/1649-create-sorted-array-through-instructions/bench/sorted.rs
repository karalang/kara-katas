// LeetCode #1649: Create Sorted Array through Instructions -- the bench's
// Rust mirror: the ★ arm on 60 random lists of 100000 instructions from 1
// to 100000, all drawn first.

const MOD: i64 = 1_000_000_007;

fn create_sorted_array(instructions: &[i32]) -> i32 {
    let top = *instructions.iter().max().unwrap() as i64;
    let mut tree = vec![0i64; (top + 1) as usize];
    let mut cost = 0;
    for (inserted, &v) in instructions.iter().enumerate() {
        let v = v as i64;
        let less = prefix(&tree, v - 1);
        let greater = inserted as i64 - prefix(&tree, v);
        cost = (cost + less.min(greater)) % MOD;
        let mut i = v;
        while i <= top {
            tree[i as usize] += 1;
            i += i & -i;
        }
    }
    cost as i32
}

fn prefix(tree: &[i64], v: i64) -> i64 {
    let mut total = 0;
    let mut i = v;
    while i > 0 {
        total += tree[i as usize];
        i -= i & -i;
    }
    total
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed: i64 = 1649;
    let mut lists: Vec<Vec<i32>> = Vec::new();
    for _ in 0..60 {
        let mut instructions = Vec::new();
        for _ in 0..100000 {
            instructions.push((next_random(&mut seed) % 100000 + 1) as i32);
        }
        lists.push(instructions);
    }
    let mut check: i64 = 0;
    let mut total: i64 = 0;
    for instructions in &lists {
        let cost = create_sorted_array(instructions) as i64;
        total += cost;
        check = (check * 31 + cost + 1) % 1000000007;
    }
    println!("60 lists of 100000 instructions: costs sum to {}, checksum {}", total, check);
}
