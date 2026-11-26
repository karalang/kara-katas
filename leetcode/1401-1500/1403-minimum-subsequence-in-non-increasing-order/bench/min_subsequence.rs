// LeetCode #1403 bench, Rust: the same sort and greedy take, workload and
// checksum as min_subsequence.kara.

fn min_subsequence(nums: &Vec<i32>) -> Vec<i32> {
    let mut order = nums.clone();
    order.sort();
    order.reverse();
    let mut rest: i32 = order.iter().sum();
    let mut taken: i64 = 0;
    let mut picked = Vec::new();
    for &x in order.iter() {
        picked.push(x);
        taken += x as i64;
        rest -= x;
        if taken > rest as i64 {
            break;
        }
    }
    picked
}

fn main() {
    let mut seed: i64 = 1403;
    let mut pool: Vec<i32> = Vec::new();
    for _ in 0..100000 {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        pool.push((seed / 65536 % 100 + 1) as i32);
    }
    let mut check: i64 = 0;
    for r in 0..20000i64 {
        let at = ((check + r * 7919) % 99501) as usize;
        let window = pool[at..at + 500].to_vec();
        let picked = min_subsequence(&window);
        let last = picked[picked.len() - 1] as i64;
        check = (check * 131 + picked.len() as i64 * 101 + last) % 1000000007;
    }
    println!("20000 windows of 500 numbers: checksum {}", check);
}
