// LeetCode #2094: Finding 3-Digit Even Numbers -- Rust mirror of the ★
// arm's benchmark (even.kara): the same 100000 lists, each answered by the
// same counts and walk over the even numbers from 100 to 998.

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn find_even_numbers(digits: &[i64]) -> Vec<i64> {
    let mut have = [0i64; 10];
    for &d in digits {
        have[d as usize] += 1;
    }
    let mut found = Vec::new();
    for x in (100..1000i64).step_by(2) {
        let mut need = [0i64; 10];
        need[(x / 100) as usize] += 1;
        need[(x / 10 % 10) as usize] += 1;
        need[(x % 10) as usize] += 1;
        if (0..10).all(|d| need[d] <= have[d]) {
            found.push(x);
        }
    }
    found
}

fn main() {
    let mut seed = 2094;
    let mut count = 0usize;
    let mut check = 0i64;
    for _ in 0..100000 {
        let len = next_random(&mut seed) % 98 + 3;
        let top = [10, 6, 4][(next_random(&mut seed) % 3) as usize];
        let digits: Vec<i64> = (0..len).map(|_| next_random(&mut seed) % top).collect();
        let got = find_even_numbers(&digits);
        count += got.len();
        for &x in &got {
            check = (check * 31 + x) % 1000000007;
        }
    }
    println!("100000 answers: {} numbers, checksum {}", count, check);
}
