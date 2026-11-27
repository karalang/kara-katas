// LeetCode #1835: Find XOR Sum of All Pairs Bitwise AND -- the bench in Rust: the ★ arm over
// 3000 calls on pairs of 20 lists of 10^5 numbers from 0 to 10^9, built
// once, each call's two lists drawn from the checksum so far. The arm
// borrows both lists, so no call copies one.

fn get_xor_sum(arr1: &[i64], arr2: &[i64]) -> i64 {
    let mut left = 0;
    for &a in arr1.iter() {
        left ^= a;
    }
    let mut right = 0;
    for &b in arr2.iter() {
        right ^= b;
    }
    left & right
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1835;
    let mut lists: Vec<Vec<i64>> = Vec::new();
    for _ in 0..20 {
        let mut list: Vec<i64> = Vec::new();
        for _ in 0..100000 {
            let hi = next_random(&mut seed);
            list.push((hi * 32768 + next_random(&mut seed)) % 1000000001);
        }
        lists.push(list);
    }
    let mut check: i64 = 0;
    for call in 0..3000 {
        let i = ((check + call) % 20) as usize;
        let j = ((check / 20 + call * 7) % 20) as usize;
        check = (check * 31 + get_xor_sum(&lists[i], &lists[j])) % 1000000007;
    }
    println!("3000 calls: checksum {}", check);
}
