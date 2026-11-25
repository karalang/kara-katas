// LeetCode #1362 bench -- Rust: d counts down from the square root of
// num + 2, and the first d that divides num + 1 or num + 2 gives the answer.

fn isqrt(x: i64) -> i64 {
    let mut r = (x as f64).sqrt() as i64;
    while r * r > x {
        r -= 1;
    }
    while (r + 1) * (r + 1) <= x {
        r += 1;
    }
    r
}

fn closest_divisors(num: i32) -> Vec<i32> {
    let (one, two) = (num as i64 + 1, num as i64 + 2);
    let mut d = isqrt(two);
    while d > 0 {
        if one % d == 0 {
            return vec![d as i32, (one / d) as i32];
        }
        if two % d == 0 {
            return vec![d as i32, (two / d) as i32];
        }
        d -= 1;
    }
    vec![1, num + 1]
}

fn main() {
    // 10^4 questions, each num up to 10^9 drawn from the checksum so far,
    // both parts of every answer folded into it
    let mut check: i64 = 0;
    for r in 0..10000 {
        let num = (1 + (check * 7919 + r) % 1000000000) as i32;
        let pair = closest_divisors(num);
        check = (check * 31 + pair[0] as i64 * 7 + pair[1] as i64 + r) % 1000000007;
    }
    println!("10000 questions: checksum {}", check);
}
