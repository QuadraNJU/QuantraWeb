#    public static double MA_CLOSE(StockInfoPtr ptr, int n) {
#         double[] nums = new double[n];
#         int i = 0;
#         while (i < n && ptr != null) {
#             nums[i] = ptr.get().getClose();
#             ptr = ptr.prev();
#             i++;
#         }
#         if (i < n) {
#             return Double.NaN;
#         } else {
#             return NumericalStatisticUtil.MEAN(nums);
#         }
#     }
from numpy import mean, NaN

from stock.data.stock_data import StockData


def MA_n(code, date, n):
    infos = StockData().get_by_code(code)
    n_days_infos = infos[infos.date <= date][0:n]
    if len(n_days_infos) == n:
        return mean(n_days_infos.close)
    else:
        return NaN


# public static double EMA(double[] list) {
#     double alpha = 2.0 / (list.length + 1);
#     return alpha * IntStream
#             .range(0, list.length - 1)
#             .mapToDouble(i -> Math.pow(alpha, i) * list[i])
#             .sum();
# }
def __EMA(lis):
    alpha = 2.0 / (len(lis) + 1)
    _sum = 0
    for i in range(0, len(lis) - 1):
        _sum += alpha ** i * lis[i]
    return _sum * alpha


def EMA_n(code, date, n):
    infos = StockData().get_by_code(code)
    n_days_infos = infos[infos.date <= date][0:n]
    if len(n_days_infos) == n:
        return __EMA(n_days_infos.close.tolist())
    else:
        return NaN
