fn sq_digit_sum(n: i64) -> i64 {
    let mut total = 0i64;
    let mut x = n;
    while x > 0 {
        let d = x % 10;
        total += d * d;
        x /= 10;
    }
    total
}

fn is_happy(n: i64) -> bool {
    let mut slow = n;
    let mut fast = sq_digit_sum(n);
    while fast != 1 && slow != fast {
        slow = sq_digit_sum(slow);
        fast = sq_digit_sum(sq_digit_sum(fast));
    }
    fast == 1
}

fn main() {
    let limit: i64 = 4000000;
    let mut sink: i64 = 0;
    for i in 1..limit {
        if is_happy(i) {
            sink += 1;
        }
    }
    println!("{}", sink);
}
