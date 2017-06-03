// app container
var app = {

    // UI parts

    nav: {},

    loading: {},

    // View loader

    views: {
        name: '',
        param: {},
        setParam: function (param, clear) {
            if (clear) {
                this.param = param;
            } else if (param) {
                for (var key in param) {
                    this.param[key] = param[key];
                }
            }
            var hash = this.name;
            if (this.param) {
                hash += '?' + $.param(this.param);
            } else {
                this.param = {};
            }
            window.location.hash = hash;
        },
        load: function (name, param) {
            app.loading.show();
            this.name = name;
            this.setParam(param, true);
            app.nav.selected = name;
            $('#content').load('res/views/' + name + '.html?' + new Date().getTime(), function () {
                app.loading.hide();
            });
        }
    },

    requests: {
        ws: null,
        wsConnect: function (path) {
            if (app.requests.ws != null) {
                app.requests.ws.close();
            }
            app.requests.ws = new WebSocket('ws://' + location.host + '/' + path);
        }
    },

    index: {
        min_date: '',
        max_date: '',
        stocks: {},
        fetch: function () {
            return $.getJSON('/api/stock/index').done(function (data) {
                app.index.min_date = data.min;
                app.index.max_date = data.max;
                app.index.stocks = data.index;
            });
        }
    },

    utils: {
        formatCode: function (code) {
            var s = '00000' + code;
            return s.substr(s.length - 6);
        },

        formatPercent: function (pct) {
            return Math.round(pct * 10000) / 100 + '%';
        },

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
