// LeetCode #1411 bench, Rust: rows of two colours and of three, 6 of each
// in the first row, workload and checksum as num_of_ways.kara.

fn num_of_ways(n: i32) -> i32 {
    let modulus: i64 = 1000000007;
    let mut two: i64 = 6;
    let mut three: i64 = 6;
    for _ in 1..n {
        let next_two = (3 * two + 2 * three) % modulus;
        let next_three = (2 * two + 2 * three) % modulus;
        two = next_two;
        three = next_three;
    }
    ((two + three) % modulus) as i32
}

fn main() {
    let mut check: i64 = 0;
    for k in 0..40000i64 {
        let n = 1 + (check + k) % 5000;
        check = (check * 131 + num_of_ways(n as i32) as i64) % 1000000007;
    }
    println!("40000 grids of up to 5000 rows: checksum {}", check);
}
