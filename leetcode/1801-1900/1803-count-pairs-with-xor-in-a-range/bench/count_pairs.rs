// LeetCode #1803: Count Pairs With XOR in a Range -- the bench in Rust: the
// ★ arm over 40 random lists of 20000 numbers built once, 100 calls.

const BITS: i64 = 15;

fn count_below(nums: &[i32], limit: i32) -> i64 {
    let mut children: Vec<usize> = vec![0; 2];
    let mut counts: Vec<i64> = vec![0; 1];
    let mut pairs: i64 = 0;
    for &x in nums {
        let mut node = 0usize;
        for b in (0..BITS).rev() {
            let xb = (x >> b & 1) as usize;
            let lb = limit >> b & 1;
            if lb == 1 {
                let same = children[2 * node + xb];
                if same != 0 {
                    pairs += counts[same];
                }
                node = children[2 * node + 1 - xb];
            } else {
                node = children[2 * node + xb];
            }
            if node == 0 {
                break;
            }
        }
        let mut at = 0usize;
        counts[0] += 1;
        for b in (0..BITS).rev() {
            let xb = (x >> b & 1) as usize;
            if children[2 * at + xb] == 0 {
                children[2 * at + xb] = counts.len();
                counts.push(0);
                children.push(0);
                children.push(0);
            }
            at = children[2 * at + xb];
            counts[at] += 1;
        }
    }
    pairs
}

fn count_pairs(nums: &[i32], low: i32, high: i32) -> i32 {
    (count_below(nums, high + 1) - count_below(nums, low)) as i32
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1803;
    let mut lists: Vec<Vec<i32>> = Vec::new();
    for _ in 0..40 {
        let nums: Vec<i32> = (0..20000).map(|_| (1 + next_random(&mut seed) % 20000) as i32).collect();
        lists.push(nums);
    }
    let mut check: i64 = 0;
    for call in 0..100i64 {
        let low = 1 + next_random(&mut seed) % 20000;
        let high = low + next_random(&mut seed) % (20001 - low);
        let nums = &lists[((check + call) % 40) as usize];
        check = (check * 31 + count_pairs(nums, low as i32, high as i32) as i64) % 1000000007;
    }
    println!("100 calls over 40 lists of 20000 numbers: checksum {}", check);
}
