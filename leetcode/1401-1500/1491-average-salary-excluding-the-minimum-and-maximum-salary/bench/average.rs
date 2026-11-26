// LeetCode #1491: Average Salary Excluding the Minimum and Maximum Salary --
// the bench in Rust, mirroring average.kara: one pass keeping the sum, the
// least and the most.

fn average(salary: &[i32]) -> f64 {
    let mut least = salary[0];
    let mut most = salary[0];
    let mut sum: i64 = 0;
    for &s in salary {
        least = least.min(s);
        most = most.max(s);
        sum += s as i64;
    }
    (sum - least as i64 - most as i64) as f64 / (salary.len() - 2) as f64
}

fn main() {
    let mut salary: Vec<i32> = (0..100i64).map(|k| (1000 + 9000 * k) as i32).collect();
    let mut check: i64 = 0;
    for pass in 0..2000000i64 {
        let k = pass % 100;
        salary[k as usize] = (1000 + 9000 * k + (check + pass) % 9000) as i32;
        let cents = (average(&salary) * 100.0).round() as i64;
        check = (check * 31 + cents) % 1000000007;
    }
    println!("2000000 calls: checksum {}", check);
}
