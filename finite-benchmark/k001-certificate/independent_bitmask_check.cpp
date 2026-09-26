// Independent K=10 exact-integer search using Gosper fixed-popcount bitmasks.
// This uses state updates as bits leave/enter, unlike the recursive scorer.
#include <array>
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <stdexcept>
using i64=std::int64_t;
using u64=std::uint64_t;
constexpr int N=50, K=10;
static std::array<i64,N> b;
static std::array<std::array<i64,N>,N> a;

static i64 direct(u64 mask,i64 c) {
    i64 s=c;
    for(int i=0;i<N;++i) if(mask&(1ULL<<i)) {
        s+=b[i];
        for(int j=0;j<i;++j) if(mask&(1ULL<<j)) s+=a[i][j];
    }
    return s;
}

static i64 interaction(int i,u64 mask) {
    i64 s=b[i];
    while(mask) {
        int j=__builtin_ctzll(mask);
        s+=a[i][j];
        mask&=mask-1;
    }
    return s;
}

int main(int argc,char** argv) {
    if(argc!=2) throw std::runtime_error("usage: independent_bitmask_check integer_coefficients.txt");
    std::ifstream in(argv[1]);
    i64 n,scale,c,upper_c;
    if(!(in>>n>>scale>>c>>upper_c)||n!=N||scale!=10000000000000000LL)
        throw std::runtime_error("invalid header");
    std::array<i64,N> f;
    std::array<std::array<i64,N>,N> q;
    for(auto &v:f) if(!(in>>v)) throw std::runtime_error("invalid f");
    for(auto &row:q) for(auto &v:row) if(!(in>>v)) throw std::runtime_error("invalid Q");
    for(int i=0;i<N;++i) {
        b[i]=f[i]+q[i][i];
        for(int j=0;j<N;++j) a[i][j]=q[i][j]+q[j][i];
    }
    const u64 limit=1ULL<<N;
    u64 mask=(1ULL<<K)-1, count=0, winner=0;
    i64 current=direct(mask,c),best=INT64_MAX;
    do {
        ++count;
        if(current<best) {best=current;winner=mask;}
        if(count%100000000ULL==0 && current!=direct(mask,c))
            throw std::runtime_error("incremental score disagrees with direct score");
        u64 low=mask&-mask;
        u64 high=mask+low;
        u64 next=(((high^mask)>>2)/low)|high;
        if(next>=limit) break;
        u64 removed=mask&~next, added=next&~mask;
        u64 active=mask;
        while(removed) {
            int i=__builtin_ctzll(removed);
            active&=~(1ULL<<i);
            current-=interaction(i,active);
            removed&=removed-1;
        }
        while(added) {
            int i=__builtin_ctzll(added);
            current+=interaction(i,active);
            active|=1ULL<<i;
            added&=added-1;
        }
        if(active!=next) throw std::runtime_error("mask update mismatch");
        mask=next;
    } while(true);
    i64 threshold=(upper_c+999999)/1000000;
    if(count!=10272278170ULL||best<=threshold||best!=direct(winner,c))
        throw std::runtime_error("K=10 certificate mismatch");
    std::cout<<"K=10; visited="<<count<<"; best_lower="<<best
             <<"; threshold_upper="<<threshold<<"; winner_mask="<<winner
             <<"; subset=";
    bool comma=false;
    for(int i=0;i<N;++i) if(winner&(1ULL<<i)) {
        std::cout<<(comma?",":"")<<i; comma=true;
    }
    std::cout<<"\nSTATUS=PASS_INDEPENDENT_BITMASK\n";
}
