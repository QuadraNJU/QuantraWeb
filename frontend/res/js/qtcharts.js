var QuantraCharts = {
    vol: function (res) {
        return [{
            type: 'bar',
            name: '交易量',
            xAxisIndex: 1,
            yAxisIndex: 1,
            data: res.volume
        }];
    },

    macd: function (res) {
        var short = 12, long = 26, mid = 9;
        var dif = [], dea = [], macd = [];
        for (var i = 0; i < res.data.length; i++) {
            if (i < long - 1) {
                dif.push(null);
                dea.push(null);
                macd.push(null);
            } else {
                dif.push(this.utils.ema(
                    res.data.slice(i - long + 1, i + 1).map(function (d) {
                        return d[1];
                    })
                ));
                if (i < long + mid - 2) {
                    dea.push(null);
                    macd.push(null);
                } else {
                    dea.push(this.utils.ema(dif.slice(i - mid + 1, i + 1)));
                    macd.push((dif[i] - dea[i]) * 2);
                }
            }
        }
        return [{
            type: 'line',
            name: 'DIF',
            xAxisIndex: 1,
            yAxisIndex: 1,
            data: dif
        }, {
            type: 'line',
            name: 'DEA',
            xAxisIndex: 1,
            yAxisIndex: 1,
            data: dea
        }, {
            type: 'line',
            name: 'MACD',
            xAxisIndex: 1,
            yAxisIndex: 1,
            data: macd
        }];
    },

    boll: function (res) {
        var m = 20;
        var boll = [], ub = [], lb = [];
        for (var i = 0; i < res.data.length; i++) {
            if (i < m - 1) {
                boll.push(null);
                ub.push(null);
                lb.push(null);
            } else {
                var sliced = res.data.slice(i - m + 1, i + 1).map(function (d) {
                    return d[1];
                });
                boll.push(this.utils.ma(sliced));
                var sigma = this.utils.std(sliced);
                ub.push(boll[i] + 2 * sigma);
                lb.push(boll[i] - 2 * sigma);
            }
        }
        return [{
            type: 'line',
            name: 'BOLL',
            xAxisIndex: 1,
            yAxisIndex: 1,
            data: boll
        }, {
            type: 'line',
            name: 'BOLL-UB',
            xAxisIndex: 1,
            yAxisIndex: 1,
            data: ub
        }, {
            type: 'line',
            name: 'BOLL-LB',
            xAxisIndex: 1,
            yAxisIndex: 1,
            data: lb
        }];
    },

    kdj: function (res) {
        var n = 9, m = 3;
        var k = [], d = [], j = [], rsv = [];
        for (var i = 0; i < res.data.length; i++) {
            if (i < n - 1) {
                rsv.push(null);
                k.push(null);
                d.push(null);
                j.push(null);
            } else {
                var sliced_n = res.data.slice(i - n + 1, i + 1);
                var llv = Math.min.apply(Math, sliced_n.map(function (d) {
                    return d[2];
                }));
                var hhv = Math.max.apply(Math, sliced_n.map(function (d) {
                    return d[3];
                }));
                rsv.push((res.data[i][1] - llv) / (hhv - llv) * 100);
                if (i < n + m - 2) {
                    k.push(null);
                    d.push(null);
                    j.push(null);
                } else {
                    k.push(this.utils.ma(rsv.slice(i - m + 1, i + 1)));
                    if (i < n + 2 * m - 3) {
                        d.push(null);
                        j.push(null);
                    } else {
                        d.push(this.utils.ma(k.slice(i - m + 1, i + 1)));
                        j.push(3 * k[i] - 2 * d[i]);
                    }
                }
            }
        }
        return [{
            type: 'line',
            name: 'K',
            xAxisIndex: 1,
            yAxisIndex: 1,
            data: k
        }, {
            type: 'line',
            name: 'D',
            xAxisIndex: 1,
            yAxisIndex: 1,
            data: d
        }, {
            type: 'line',
            name: 'J',
            xAxisIndex: 1,
            yAxisIndex: 1,
            data: j
        }];
    },

    psy: function (res) {
        var n = 12, psy = [];
        for (var i = 0; i < res.data.length; i++) {
            if (i < n) {
                psy.push(null);
            } else {
                var count = 0;
                for (var j = i - n + 1; j <= i; j++) {
                    if (res.data[j][1] > res.data[j - 1][1]) {
                        count++;
                    }
                }
                psy.push(count / n * 100);
            }
        }
        return [{
            type: 'line',
            name: 'PSY',
            xAxisIndex: 1,
            yAxisIndex: 1,
            data: psy
        }];
    },

    utils: {
        ma: function (arr) {
            return arr.reduce(function (a, b) {
                    return a + b;
                }) / arr.length;
        },

        ema: function (arr) {
            var alpha = 2 / (arr.length + 1), sum = 0;
            for (var i = 0; i < arr.length; i++) {
                sum += Math.pow(alpha, i) * arr[i];
            }
            return alpha * sum;
        },

        std: function (arr) {
            var mean = this.ma(arr);
            return Math.sqrt(arr.map(function (a) {
                    return Math.pow(a - mean, 2)
                })
                    .reduce(function (a, b) {
                        return a + b;
                    }) / arr.length);
        }
    }
};