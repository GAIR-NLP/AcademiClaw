#include <iostream>
#include <queue>
#include <vector>

using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(0);

    int n;
    long long C;
    if (!(cin >> n >> C)) return 0;

    // 最小堆维护“买入成本”
    priority_queue<long long, vector<long long>, greater<long long>> pq;
    long long totalProfit = 0;

    for (int i = 0; i < n; ++i) {
        long long price;
        cin >> price;
        // 如果当前价格扣除手续费后大于堆顶成本，则尝试交易
        if (!pq.empty() && price - C > pq.top()) {
            totalProfit += (price - C - pq.top());
            pq.pop();
            // 第一次推入：代表当前卖出点作为一个“反悔买入点”
            // 后续若有更高价 p_k，收益变为 (p_k - C - p_j) + (p_j - C - p_i)
            // 实际上逻辑应调整为推入 price - C 以抵消掉多收的一次 C
            pq.push(price - C); 
            pq.push(price); // 当前价格作为新买入点
        } else {
            pq.push(price);
        }
    }
    cout << totalProfit << endl;
    return 0;
}