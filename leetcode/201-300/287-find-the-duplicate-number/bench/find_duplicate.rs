// Benchmark harness for LeetCode #287 — Find the Duplicate Number.
// Mirrors find_duplicate.kara algorithm-for-algorithm.

fn find_duplicate(nums: &Vec<i64>) -> i64 {
    let mut slow = nums[0];
    let mut fast = nums[0];
    slow = nums[slow as usize];
    fast = nums[nums[fast as usize] as usize];
    while slow != fast {
        slow = nums[slow as usize];
        fast = nums[nums[fast as usize] as usize];
    }
    let mut finder = nums[0];
    while finder != slow {
        finder = nums[finder as usize];
        slow = nums[slow as usize];
    }
    finder
}

fn main() {
    let np: i64 = 4;
    let n: i64 = 200000;
    let iters: i64 = 80;

    let mut arrays: Vec<Vec<i64>> = Vec::new();
    let mut p = 0i64;
    while p < np {
        let mut order: Vec<i64> = Vec::new();
        let mut v = 1i64;
        while v <= n {
            order.push(v);
            v += 1;
        }
        let mut x = p + 12345;
        let mut k = n - 1;
        while k > 0 {
            x = (x * 1103515245 + 12345) % 2147483648;
            let j = (x / 65536) % (k + 1);
            let tmp = order[k as usize];
            order[k as usize] = order[j as usize];
            order[j as usize] = tmp;
            k -= 1;
        }

        let mut arr: Vec<i64> = Vec::new();
        let mut z = 0i64;
        while z <= n {
            arr.push(0);
            z += 1;
        }
        let mut t = 0i64;
        while t < n {
            let nxt = (t + 1) % n;
            arr[order[t as usize] as usize] = order[nxt as usize];
            t += 1;
        }
        arr[0] = order[(p * 37) as usize];
        arrays.push(arr);
        p += 1;
    }

    let mut sink: i64 = 0;
    let mut it = 0i64;
    while it < iters {
        let idx = ((it * 3) % np) as usize;
        sink = (sink * 31 + find_duplicate(&arrays[idx])) % 1000000007;
        it += 1;
    }
    println!("{}", sink);
}
