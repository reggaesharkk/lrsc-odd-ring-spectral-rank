// Exhaustive exact-integer lower-bound search for an adjacent LRSC mask cell.
// Compile: g++ -O3 -std=c++17 -Wall -Wextra exact_search.cpp -o exact_search
// Usage: ./exact_search integer_coefficients.txt MIN_K MAX_K
//
// Coverage invariant: visit(depth,first,partial) represents precisely the
// increasing prefix chosen[0..depth-1]. Every completion has a unique next
// index x in [first, 50-(K-depth)], hence induction gives a bijection to the
// K-subsets of {0,...,49}. The count is independently checked against C(50,K).
#include <array>
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <limits>
#include <stdexcept>

constexpr int N=50;
using i64=std::int64_t;
using u64=std::uint64_t;
static std::array<i64,N> b;
static std::array<std::array<i64,N>,N> a;
static std::array<int,11> chosen;
static std::array<int,11> best_indices;
static i64 best, constant;
static u64 count_visited;
static int K;

static void visit(int depth, int first, i64 partial) {
    if(depth==K) {
        ++count_visited;
        if(partial<best) {
            best=partial;
            best_indices=chosen;
        }
        return;
    }
    int remaining=K-depth;
    for(int x=first;x<=N-remaining;++x) {
        i64 increment=b[x];
        for(int t=0;t<depth;++t) increment+=a[x][chosen[t]];
        chosen[depth]=x;
        visit(depth+1,x+1,partial+increment);
    }
}

static u64 binomial(int n,int k) {
    __int128 v=1;
    for(int i=1;i<=k;++i) v=v*(n-k+i)/i;
    return static_cast<u64>(v);
}

int main(int argc,char** argv) {
    if(argc!=4) {std::cerr<<"usage: exact_search COEFFICIENTS MIN_K MAX_K\n";return 2;}
    std::ifstream in(argv[1]);
    i64 n,scale,upper_c;
    if(!(in>>n>>scale>>constant>>upper_c)||n!=N||scale!=10000000000000000LL)
        throw std::runtime_error("invalid coefficient header");
    std::array<i64,N> f;
    std::array<std::array<i64,N>,N> q;
    for(auto &v:f) if(!(in>>v)) throw std::runtime_error("truncated f");
    for(auto &row:q) for(auto &v:row) if(!(in>>v)) throw std::runtime_error("truncated Q");
    i64 extra; if(in>>extra) throw std::runtime_error("unexpected coefficient data");
    i64 maxb=0,maxa=0;
    for(int x=0;x<N;++x) {
        b[x]=f[x]+q[x][x];
        maxb=std::max(maxb,static_cast<i64>(std::llabs(b[x])));
        for(int y=0;y<N;++y) {
            a[x][y]=q[x][y]+q[y][x];
            maxa=std::max(maxa,static_cast<i64>(std::llabs(a[x][y])));
        }
    }
    __int128 absolute_upper=std::llabs(constant)+static_cast<__int128>(11)*maxb
                            +static_cast<__int128>(55)*maxa;
    if(absolute_upper>=std::numeric_limits<i64>::max()) throw std::runtime_error("integer overflow risk");
    i64 threshold=(upper_c+999999)/1000000; // ceil(1e-6 * upper c)
    int mink=std::atoi(argv[2]), maxk=std::atoi(argv[3]);
    if(mink<1||maxk>11||mink>maxk) throw std::runtime_error("K range must be within 1..11");
    std::cout<<"scale="<<scale<<"; threshold_upper="<<threshold
             <<"; integer_absolute_upper="<<static_cast<i64>(absolute_upper)<<std::endl;
    if(constant<=threshold) throw std::runtime_error("K=0 fails");
    for(K=mink;K<=maxk;++K) {
        best=std::numeric_limits<i64>::max();count_visited=0;
        visit(0,0,constant);
        u64 expected=binomial(N,K);
        if(count_visited!=expected) throw std::runtime_error("count failure");
        std::cout<<"K="<<K<<"; visited="<<count_visited<<"; expected="<<expected
                 <<"; best_lower="<<best<<"; threshold_upper="<<threshold
                 <<"; margin="<<(best-threshold)<<"; subset=";
        for(int i=0;i<K;++i) std::cout<<(i?",":"")<<best_indices[i];
        std::cout<<std::endl;
    }
    std::cout<<"STATUS=ENUMERATED"<<std::endl;
}
