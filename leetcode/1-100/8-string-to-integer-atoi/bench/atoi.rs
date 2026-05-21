// Benchmark workload — one-pass atoi (LeetCode #8). Rust mirror of
// bench/atoi.kara. Same N, K, same input set, same sink formula —
// see that file's header for the workload rationale.

fn my_atoi(s: &str) -> i32 {
    let bytes = s.as_bytes();
    let n = bytes.len();

    let space: u8 = b' ';
    let plus:  u8 = b'+';
    let minus: u8 = b'-';
    let zero:  u8 = b'0';
    let nine:  u8 = b'9';

    let mut i: usize = 0;
    while i < n && bytes[i] == space {
        i += 1;
    }

    let mut sign: i32 = 1;
    if i < n && bytes[i] == plus {
        i += 1;
    } else if i < n && bytes[i] == minus {
        sign = -1;
        i += 1;
    }

    let int_max: i32 = 2_147_483_647;
    let int_min: i32 = -2_147_483_648;
    let max_div: i32 = int_max / 10;

    let mut result: i32 = 0;
    while i < n {
        let b = bytes[i];
        if b < zero || b > nine {
            break;
        }
        let digit: i32 = (b as i32) - (zero as i32);
        if result > max_div || (result == max_div && digit > 7) {
            if sign == 1 {
                return int_max;
            }
            return int_min;
        }
        result = result * 10 + digit;
        i += 1;
    }

    sign * result
}

fn main() {
    let n: i64 = 8;
    let k_iters: i64 = 10_000_000;

    let inputs: Vec<&str> = vec![
        "42",
        "   -42",
        "4193 with words",
        "91283472332",
        "+1",
        "  0000000000012345678",
        "-2147483648",
        "  -0012a42",
    ];

    let mut sum: i64 = 0;
    for k in 0..k_iters {
        let idx = (k % n) as usize;
        let r = my_atoi(inputs[idx]);
        sum += r as i64;
    }
    println!("{}", sum);
}
