// app container
var app = {

    // UI parts

    nav: {},

    modals: {},

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
            window.history.replaceState(null, null, '#' + hash);
            //window.location.hash = hash;
        },
        load: function (name, param) {
            app.modals.showLoading('正在加载页面');
            this.name = name;
            this.setParam(param, true);
            app.nav.selected = name;
            $('#content').load('res/views/' + name + '.html?' + new Date().getTime(), function () {
                app.requests.wsClose();
                app.modals.hideLoading();
            });
        }
    },

    requests: {
        ws: null,
        wsConnect: function (path) {
            this.wsClose();
            app.requests.ws = new WebSocket('ws://' + location.host + '/' + path);
        },
        wsClose: function () {
            if (app.requests.ws != null) {
                app.requests.ws.close();
            }
        },
        get: function (url, cb) {
            return $.ajax({
                url: url,
                timeout: 5000,
                dataType: 'json',
                success: function (result, status, xhr) {
                    if (result.ok == false) {
                        app.modals.alert('danger', '错误', result.msg ? result.msg : '未知错误');
                    } else {
                        cb && cb(result);
                    }
                },
                error: function (xhr, status, error) {
                    app.modals.alert('danger', '错误', '无法连接服务器，请稍后重试');
                }
            });
        },
        post: function (url, data, cb) {
            return $.ajax({
                url: url,
                timeout: 5000,
                method: 'POST',
                data: data,
                dataType: 'json',
                success: function (result, status, xhr) {
                    if (result.ok == false) {
                        app.modals.alert('danger', '错误', result.msg ? result.msg : '未知错误');
                    } else {
                        cb && cb(result);
                    }
                },
                error: function (xhr, status, error) {
                    app.modals.alert('danger', '错误', '无法连接服务器，请稍后重试');
                }
            });
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

        toFixed: function (num) {
            return Number(num.toFixed(2));
        }
    }
};
