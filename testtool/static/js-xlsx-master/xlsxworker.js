/* xlsx.js (C) 2013-present SheetJS -- http://sheetjs.com */
if (!importScripts) {
    var importScripts = (function (globalEval) {
        var xhr = new XMLHttpRequest;
        return function importScripts() {
            var
                args = Array.prototype.slice.call(arguments)
                , len = args.length
                , i = 0
                , meta
                , data
                , content
            ;
            for (; i < len; i++) {
                if (args[i].substr(0, 5).toLowerCase() === "data:") {
                    data = args[i];
                    content = data.indexOf(",");
                    meta = data.substr(5, content).toLowerCase();
                    data = decodeURIComponent(data.substr(content + 1));
                    if (/;\s*base64\s*[;,]/.test(meta)) {
                        data = atob(data);
                    }
                    if (/;\s*charset=[uU][tT][fF]-?8\s*[;,]/.test(meta)) {
                        data = decodeURIComponent(escape(data));
                    }
                } else {
                    xhr.open("GET", args[i], false);
                    xhr.send(null);
                    data = xhr.responseText;
                }
                globalEval(data);
            }
        };
    }(eval));
}
importScripts('shim.js');
/* uncomment the next line for encoding support */
importScripts('dist/cpexcel.js');
importScripts('jszip.js');
importScripts('xlsx.js');
postMessage({t: "ready"});

onmessage = function (evt) {
    var v;
    try {
        v = XLSX.read(evt.data.d, {type: evt.data.b});
        postMessage({t: "xlsx", d: JSON.stringify(v)});
    } catch (e) {
        postMessage({t: "e", d: e.stack || e});
    }
};
