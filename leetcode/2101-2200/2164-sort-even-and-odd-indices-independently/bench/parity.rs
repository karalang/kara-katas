// LeetCode #2164: Sort Even and Odd Indices Independently -- the
// benchmark's Rust mirror of parity.kara.

fn sort_even_odd(nums: Vec<i64>) -> Vec<i64> {
    let mut even: Vec<i64> = nums.iter().step_by(2).cloned().collect();
    let mut odd: Vec<i64> = nums.iter().skip(1).step_by(2).cloned().collect();
    even.sort();
    odd.sort_by(|a, b| b.cmp(a));
    let mut out: Vec<i64> = Vec::new();
    for i in 0..nums.len() {
        if i % 2 == 0 {
            out.push(even[i / 2]);
        } else {
            out.push(odd[i / 2]);
        }
    }
    out
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2164i64;
    let mut lists: Vec<Vec<i64>> = Vec::new();
    for _ in 0..1000 {
        lists.push((0..100).map(|_| next_random(&mut seed) % 100 + 1).collect());
    }
    let mut check = 0i64;
    for round in 0..200usize {
        for k in 0..1000usize {
            let at = (next_random(&mut seed) % 100) as usize;
            lists[k][at] = next_random(&mut seed) % 100 + 1;
            let out = sort_even_odd(lists[k].clone());
            check = (check * 31 + out[round % 100] + out[(k * 7) % 100]) % 1000000007;
        }
    }
    println!("200000 solves: checksum {}", check);
}
