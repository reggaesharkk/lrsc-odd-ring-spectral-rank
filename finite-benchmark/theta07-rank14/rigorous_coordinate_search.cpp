// Exact-integer lower bounds with outward-rounded Fourier-coordinate pruning.
// A completed run with no unresolved leaf certifies exclusion at its K.
#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <limits>
#include <stdexcept>
#include <vector>
using i64=std::int64_t;
using i128=__int128_t;
using u64=std::uint64_t;
constexpr int N=50,MAXK=15;
struct Coordinate {
    i64 target_lo,target_hi;
    std::array<i64,N> vlo,vhi;
    i64 lo[N+1][MAXK+1]{},hi[N+1][MAXK+1]{};
};
std::vector<Coordinate> z;
std::vector<i64> partial_lo,partial_hi;
std::array<i64,N> b;
std::array<std::array<i64,N>,N> a;
std::array<int,MAXK> selected{};
u64 nodes[MAXK+1]{},pruned[MAXK+1]{},leaves=0,total_nodes=0,cap,covered=0;
i64 c_lower,c_upper,threshold;
i128 coordinate_threshold;
int K;
bool capped=false,unresolved=false;
static u64 choose(int n,int k) {
    i128 v=1;
    for(int i=1;i<=k;++i)v=v*(n-k+i)/i;
    return static_cast<u64>(v);
}

static void visit(int depth,int first,i64 score) {
    if(capped||unresolved)return;
    ++nodes[depth];++total_nodes;
    if(total_nodes>cap){capped=true;return;}
    int r=K-depth;
    i128 squared_lower=0;
    for(size_t d=0;d<z.size();++d) {
        const auto &v=z[d];
        i64 required_lo=v.target_lo-partial_hi[d];
        i64 required_hi=v.target_hi-partial_lo[d];
        i64 distance=std::max({i64(0),v.lo[first][r]-required_hi,required_lo-v.hi[first][r]});
        squared_lower+=i128(distance)*distance;
        if(squared_lower>coordinate_threshold){++pruned[depth];covered+=choose(N-first,r);return;}
    }
    if(r==0) {
        ++leaves;
        ++covered;
        if(score<=threshold) {
            unresolved=true;
            std::cout<<"UNRESOLVED_LOWER_BOUND subset=";
            for(int t=0;t<K;++t)std::cout<<(t?",":"")<<selected[t];
            std::cout<<" score_lower="<<score<<" threshold_upper="<<threshold<<'\n';
        }
        return;
    }
    for(int x=first;x<=N-r;++x) {
        i64 increment=b[x];
        for(int t=0;t<depth;++t)increment+=a[x][selected[t]];
        selected[depth]=x;
        for(size_t d=0;d<z.size();++d){partial_lo[d]+=z[d].vlo[x];partial_hi[d]+=z[d].vhi[x];}
        visit(depth+1,x+1,score+increment);
        for(size_t d=0;d<z.size();++d){partial_lo[d]-=z[d].vlo[x];partial_hi[d]-=z[d].vhi[x];}
        if(capped||unresolved)return;
    }
}
int main(int argc,char**argv) {
    if(argc!=5)throw std::runtime_error("usage: search COEFFICIENTS COORDINATES K NODE_CAP");
    std::ifstream in(argv[1]);i64 n,scale;
    if(!(in>>n>>scale>>c_lower>>c_upper)||n!=N||scale!=10000000000000000LL)
        throw std::runtime_error("bad coefficients");
    std::array<i64,N> f;std::array<std::array<i64,N>,N> q;
    for(auto &x:f)if(!(in>>x))throw std::runtime_error("bad f");
    for(auto &row:q)for(auto &x:row)if(!(in>>x))throw std::runtime_error("bad Q");
    for(int i=0;i<N;++i){b[i]=f[i]+q[i][i];for(int j=0;j<N;++j)a[i][j]=q[i][j]+q[j][i];}
    threshold=(c_upper+999999)/1000000;
    coordinate_threshold=i128(c_upper)*1000000; // coordinate scale 1e14, c scale 1e16
    std::ifstream coord_in(argv[2]);int dimensions;i64 coord_scale;
    if(!(coord_in>>n>>dimensions>>coord_scale)||n!=N||coord_scale!=100000000000000LL||dimensions!=198)
        throw std::runtime_error("bad coordinate header");
    z.resize(dimensions);
    for(auto &v:z) {
        if(!(coord_in>>v.target_lo>>v.target_hi))throw std::runtime_error("bad target interval");
        for(int i=0;i<N;++i)if(!(coord_in>>v.vlo[i]>>v.vhi[i]))throw std::runtime_error("bad channel interval");
    }
    K=std::stoi(argv[3]);cap=std::stoull(argv[4]);
    if(K<1||K>MAXK)throw std::runtime_error("K out of range");
    i64 maxb=0,maxa=0,maxcoord=0;
    for(int i=0;i<N;++i){
        maxb=std::max(maxb,static_cast<i64>(std::llabs(b[i])));
        for(int j=0;j<N;++j)maxa=std::max(maxa,static_cast<i64>(std::llabs(a[i][j])));
    }
    for(const auto &v:z){
        maxcoord=std::max({maxcoord,static_cast<i64>(std::llabs(v.target_lo)),
            static_cast<i64>(std::llabs(v.target_hi))});
        for(int i=0;i<N;++i)maxcoord=std::max({maxcoord,
            static_cast<i64>(std::llabs(v.vlo[i])),
            static_cast<i64>(std::llabs(v.vhi[i]))});
    }
    i128 score_bound=std::llabs(c_lower)+i128(K)*maxb+i128(K)*(K-1)/2*maxa;
    if(score_bound>=std::numeric_limits<i64>::max()||maxcoord>1000000000000000LL)
        throw std::runtime_error("integer accumulator bound exceeded");
    for(auto &v:z)for(int first=0;first<=N;++first)for(int r=0;r<=K;++r) {
        if(r>N-first){
            v.lo[first][r]=std::numeric_limits<i64>::max()/4;
            v.hi[first][r]=std::numeric_limits<i64>::min()/4;
            continue;
        }
        std::vector<i64> lower(v.vlo.begin()+first,v.vlo.end());
        std::vector<i64> upper(v.vhi.begin()+first,v.vhi.end());
        std::sort(lower.begin(),lower.end());std::sort(upper.begin(),upper.end());
        for(int t=0;t<r;++t){v.lo[first][r]+=lower[t];v.hi[first][r]+=upper[upper.size()-1-t];}
    }
    partial_lo.assign(z.size(),0);partial_hi.assign(z.size(),0);
    visit(0,0,c_lower);
    for(int d=0;d<=K;++d)std::cout<<"K="<<K<<" depth="<<d<<" visited="<<nodes[d]<<" pruned="<<pruned[d]<<'\n';
    std::cout<<"K="<<K<<" total_nodes="<<total_nodes<<" leaves="<<leaves
             <<" capped="<<capped<<" unresolved="<<unresolved<<'\n';
    std::cout<<"K="<<K<<" covered="<<covered<<" expected="<<choose(N,K)<<'\n';
    if(!capped&&!unresolved&&covered==choose(N,K))std::cout<<"STATUS=PROVED_NO_PASS_AT_K"<<'\n';
    else std::cout<<"STATUS=INCOMPLETE"<<'\n';
}
