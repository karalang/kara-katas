// Benchmark: LeetCode #982 Triples with Bitwise AND Equal To Zero -- the
// ★ arm, pair counts and the free bits' submasks, on lists of LeetCode's
// largest size. Mirrors count_triplets.kara, .c, .py and go-seq/.

fn count_triplets(nums: &[i64]) -> i64 {
    let mut all = 0;
    for &x in nums {
        all |= x;
    }
    let mut size = 1;
    while size <= all {
        size *= 2;
    }
    let full = size - 1;
    let mut pairs = vec![0i64; size as usize];
    for &a in nums {
        for &b in nums {
            pairs[(a & b) as usize] += 1;
        }
    }
    let mut triples = 0;
    for &x in nums {
        let free = full ^ x;
        let mut s = free;
        loop {
            triples += pairs[s as usize];
            if s == 0 {
                break;
            }
            s = (s - 1) & free;
        }
    }
    triples
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let rounds = 15;
    let mut seed = 982;
    let lists: Vec<Vec<i64>> = (0..20)
        .map(|_| (0..1000).map(|_| next_random(&mut seed) % 65536).collect())
        .collect();
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for i in 0..20 {
            let t = count_triplets(&lists[(r + i) % 20]);
            total += t;
            check = (check * 31 + t) % 1000000007;
        }
    }
    println!("{} rounds over 20 lists of 1000 values: triples {}, checksum {}", rounds, total, check);
}
