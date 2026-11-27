// LeetCode #1846: Maximum Element After Decreasing and Rearranging -- the
// bench in Rust: the ★ arm over 200 calls on the first 50000 to 99999 of
// one list of 10^5 numbers from 1 to 60000, built once, each run's length
// drawn from the checksum so far. Each call is handed its own copy of its
// run, which the arm sorts.

fn maximum_element_after_decrementing_and_rearranging(mut arr: Vec<i64>) -> i64 {
    arr.sort();
    let mut top = 0;
    for &x in arr.iter() {
        top = (top + 1).min(x);
    }
    top
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1846;
    let mut base: Vec<i64> = Vec::new();
    for _ in 0..100000 {
        let hi = next_random(&mut seed);
        base.push(1 + (hi * 32768 + next_random(&mut seed)) % 60000);
    }
    let mut check: i64 = 0;
    for call in 0..200 {
        let n = (50000 + (check + call) % 50000) as usize;
        check = (check * 31 + maximum_element_after_decrementing_and_rearranging(base[..n].to_vec())) % 1000000007;
    }
    println!("200 calls: checksum {}", check);
}
