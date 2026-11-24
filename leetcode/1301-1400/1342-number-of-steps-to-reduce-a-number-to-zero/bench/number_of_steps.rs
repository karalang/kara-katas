// LeetCode #1342 bench in Rust: the ★ arm (halve an even number, take one
// from an odd one, count the steps) on the same 5 passes over 10^6 + 1
// numbers.

fn number_of_steps(mut num: i32) -> i32 {
    let mut steps = 0;
    while num > 0 {
        if num % 2 == 0 {
            num /= 2;
        } else {
            num -= 1;
        }
        steps += 1;
    }
    steps
}

fn main() {
    let mut check: i64 = 0;
    for pass in 0..5i64 {
        for x in 0..1000001i64 {
            let steps = number_of_steps(((x + check) % 1000001) as i32);
            check = (check * 31 + steps as i64 + pass) % 1000000007;
        }
    }
    println!("5 passes over 10^6 + 1 numbers: checksum {}", check);
}
