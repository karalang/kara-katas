// LeetCode #1317 bench, Rust mirror of the Kāra bench: the ★ arm (the first
// number tried from 1 up, each pair's digits read off by `% 10` and `/ 10`,
// until neither has a 0) on every n from 2 to 10^4; 300 passes, each
// starting its walk through the range at a place chosen by the checksum so
// far and folding both numbers of every answer into it.

fn has_zero(x: i64) -> bool {
    let mut rest = x;
    while rest > 0 {
        if rest % 10 == 0 {
            return true;
        }
        rest /= 10;
    }
    false
}

fn get_no_zero_integers(n: i64) -> Vec<i64> {
    let mut a = 1;
    while has_zero(a) || has_zero(n - a) {
        a += 1;
    }
    vec![a, n - a]
}

fn main() {
    let mut check: i64 = 0;
    for pass in 0..300i64 {
        let start = check % 9999;
        for k in 0..9999i64 {
            let n = 2 + (start + k) % 9999;
            let v = get_no_zero_integers(n);
            check = (check * 31 + v[0] * 7 + v[1] + pass) % 1000000007;
        }
    }
    println!("300 passes over every n from 2 to 10^4: checksum {}", check);
}
