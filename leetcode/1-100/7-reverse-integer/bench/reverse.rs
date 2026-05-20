// Benchmark workload — pop-and-push Reverse Integer. Rust mirror of
// bench/reverse.kara. Same N, K, same LCG-style input fill, same sink
// formula — see that file's header for the workload rationale.

fn reverse(x: i32) -> i32 {
    let mut x = x;
    let mut result: i32 = 0;
    let int_max: i32 = 2_147_483_647;
    let int_min: i32 = -2_147_483_648;
    let max_div: i32 = int_max / 10;
    let min_div: i32 = int_min / 10;
    while x != 0 {
        let digit: i32 = x % 10;
        if result > max_div || (result == max_div && digit > 7) {
            return 0;
        }
        if result < min_div || (result == min_div && digit < -8) {
            return 0;
        }
        result = result * 10 + digit;
        x /= 10;
    }
    result
}

fn main() {
    let n: i64 = 1024;
    let k_iters: i64 = 50_000_000;

    let mut inputs: Vec<i32> = Vec::with_capacity(n as usize);
    for i in 0..n {
        let raw: i64 = i.wrapping_mul(2_654_435_769).wrapping_add(305_419_896);
        let v32: i32 = raw as i32;
        inputs.push(v32);
    }

    let mut sum: i64 = 0;
    for k in 0..k_iters {
        let idx = (k % n) as usize;
        let x = inputs[idx];
        let r = reverse(x);
        sum += r as i64;
    }
    println!("{}", sum);
}
