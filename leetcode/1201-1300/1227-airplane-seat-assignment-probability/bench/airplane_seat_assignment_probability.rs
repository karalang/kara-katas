// LeetCode #1227 bench: the running-sum arm in Rust, over the same 1000
// random n up to 10^5 as the Kāra bench.

fn nth_person_gets_nth_seat(n: i64) -> f64 {
    let mut f = 1.0;
    let mut sum = 0.0;
    for m in 2..=n {
        f = (1.0 + sum) / m as f64;
        sum += f;
    }
    f
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1227;
    let mut total = 0.0;
    for _ in 0..1000 {
        let n = next_random(&mut seed) % 30000 * 3 + next_random(&mut seed) % 10000 + 1;
        total += nth_person_gets_nth_seat(n);
    }
    println!("1000 random n up to 10^5: total {total:.5}");
}
