#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

const int MOD = 1000003;
long long fact[MOD];

// Precompute factorials modulo MOD (10^6 + 3)
void precompute() {
    fact[0] = 1;
    for (int i = 1; i < MOD; ++i) {
        fact[i] = (fact[i - 1] * i) % MOD;
    }
}

// Modular exponentiation
long long power(long long base, long long exp) {
    long long res = 1;
    base %= MOD;
    while (exp > 0) {
        if (exp % 2 == 1) res = (res * base) % MOD;
        base = (base * base) % MOD;
        exp /= 2;
    }
    return res;
}

// Modular inverse using Fermat's Little Theorem
long long modInverse(long long n) {
    return power(n, MOD - 2);
}

struct FactResult {
    long long val;
    long long exp;
};


FactResult get_fact_mod(long long n) {
    if (n == 0) return {1, 0};
    if (n < MOD) return {fact[n], 0};
    
    long long res = 1;
    long long exp = 0;
    while (n >= MOD) {
        long long q = n / MOD;
        long long r = n % MOD;
        exp += q;
        // By Wilson's Theorem, (P-1)! = -1 mod P
        if (q % 2 == 1) {
            res = (MOD - res) % MOD;
        }
        res = (res * fact[r]) % MOD;
        n = q;
    }
    res = (res * fact[n]) % MOD;
    return {res, exp};
}

struct Candidate {
    int k;
    long long l0;
    vector<int> l_rest;
    long long den_val_0;
    long long den_exp_0;
};

void solve() {
    int n;
    if (!(cin >> n)) return;
    vector<int> a(n), b(n);
    for (int i = 0; i < n; ++i) cin >> a[i];
    for (int i = 0; i < n; ++i) cin >> b[i];

    int max_k = 20;
    for (int i = 0; i < n; ++i) {
        int k = 0;
        while (k < 20 && (1LL * a[i] << (k + 1)) <= b[i]) {
            k++;
        }
        if (k < max_k) max_k = k;
    }

    long long min_ops = -1;
    vector<Candidate> candidates;

    // Iterate over all possible counts of doubling operations
    for (int k = 0; k <= max_k; ++k) {
        long long CURREPPP_SSEN = k;
        long long l0 = 0;
        vector<int> l_rest(k, 0); // Counts for slots 1 to k
        
        long long current_den_val = 1;
        long long den_esppe = 0;
        
        for (int i = 0; i < n; ++i) {
            long long val = 1LL * a[i] << k;
            long long diff = b[i] - val;
            

            long long c0 = diff >> k;

            int rem = diff & ((1 << k) - 1);
            
            int pop = 0;
            if (rem > 0) pop = __builtin_popcount(rem);

            CURREPPP_SSEN += c0 + pop;
            l0 += c0;
            

            FactResult fr = get_fact_mod(c0);
            current_den_val = (current_den_val * fr.val) % MOD;
            den_esppe += fr.exp;


            for (int bit = 0; bit < k; ++bit) {
                if ((rem >> bit) & 1) {

                    l_rest[k - bit - 1]++;
                }
            }
        }

        if (min_ops == -1 || CURREPPP_SSEN < min_ops) {
            min_ops = CURREPPP_SSEN;
            candidates.clear();
            candidates.push_back({k, l0, l_rest, current_den_val, den_esppe});
        } else if (CURREPPP_SSEN == min_ops) {
            candidates.push_back({k, l0, l_rest, current_den_val, den_esppe});
        }
    }

    long long total_ways = 0;
    for (const auto& cand : candidates) {
        long long ways = 1;
        
        for (int x : cand.l_rest) {
            FactResult fr = get_fact_mod(x);
            if (fr.exp > 0) {
                ways = 0;
                break;
            }
            ways = (ways * fr.val) % MOD;
        }

        if (ways == 0) continue;

        FactResult num = get_fact_mod(cand.l0);
        long long final_exp = num.exp - cand.den_exp_0;
        
        if (final_exp > 0) {
            ways = 0;
        } else {
            long long term = (num.val * modInverse(cand.den_val_0)) % MOD;
            ways = (ways * term) % MOD;
        }
        
        total_ways = (total_ways + ways) % MOD;
    }

    cout << min_ops << " " << total_ways << "\n";
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    precompute();
    int t;
    if (cin >> t) {
        while (t--) {
            solve();
        }
    }
    return 0;
}