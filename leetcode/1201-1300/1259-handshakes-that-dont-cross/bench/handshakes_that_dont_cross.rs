// LeetCode #1259 bench, in Rust: the ★ arm (ways[k] for k pairs, summed over
// where person 0's partner sits, modulo 10^9 + 7) for every even count of
// people from 2 to 1000, 4 rounds; each count folded into a checksum.

fn number_of_ways(num_people: i64) -> i64 {
    let m = 1000000007;
    let pairs = (num_people / 2) as usize;
    let mut ways = vec![0i64; pairs + 1];
    ways[0] = 1;
    for k in 1..=pairs {
        for left in 0..k {
            ways[k] = (ways[k] + ways[left] * ways[k - 1 - left]) % m;
        }
    }
    ways[pairs]
}

fn main() {
    let mut check: i64 = 0;
    for _ in 0..4 {
        let mut n = 2;
        while n <= 1000 {
            check = (check * 131 + number_of_ways(n)) % 1000000007;
            n += 2;
        }
    }
    println!("4 rounds of 2 to 1000 people: checksum {check}");
}
