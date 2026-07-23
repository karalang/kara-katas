fn flip(left: &mut [i64], right: &mut [i64], root: i64) -> i64 {
    let mut cur = root;
    let mut prev = -1i64;
    let mut prev_right = -1i64;
    while cur != -1 {
        let next = left[cur as usize];
        left[cur as usize] = prev_right;
        prev_right = right[cur as usize];
        right[cur as usize] = prev;
        prev = cur;
        cur = next;
    }
    prev
}

fn main() {
    let l: i64 = 50000;
    let n = 2 * l;
    let passes: i64 = 1100;

    let mut val = vec![0i64; n as usize];
    let mut state: i64 = 12345;
    for c in 0..n {
        state = (state * 1103515245 + 12345) & 2147483647;
        val[c as usize] = state;
    }

    let mut left = vec![-1i64; n as usize];
    let mut right = vec![-1i64; n as usize];

    let mut sink: i64 = 0;
    for p in 0..passes {
        for i in 0..l {
            left[i as usize] = if i < l - 1 { i + 1 } else { -1 };
            right[i as usize] = l + i;
        }
        let pp = p % l;
        right[pp as usize] = l + ((p * 7 + 3) % l);

        let new_root = flip(&mut left, &mut right, 0);

        let mut chk = 0i64;
        for j in 0..n {
            chk = (chk * 1103515245
                + val[j as usize] * 3
                + left[j as usize]
                + 2
                + right[j as usize]
                + 5)
                & 2147483647;
        }
        chk = (chk * 1103515245 + new_root + 1) & 2147483647;
        sink = (sink + chk) & 2147483647;
    }
    println!("{}", sink);
}
