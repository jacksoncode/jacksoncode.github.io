# Gitbook使用常见问题

#### gitbook出现TypeError: cb.apply is not a function解决办法

执行gitbook -V的时候出现如下错误

````bash
[root@pes nodejs]# gitbook -V
CLI version: 2.3.2
Installing GitBook 3.2.3
/data/soft/nodejs/lib/node_modules/gitbook-cli/node_modules/npm/node_modules/graceful-fs/polyfills.js:287
      if (cb) cb.apply(this, arguments)
                 ^

TypeError: cb.apply is not a function
    at /data/soft/nodejs/lib/node_modules/gitbook-cli/node_modules/npm/node_modules/graceful-fs/polyfills.js:287:18
    at FSReqCallback.oncomplete (fs.js:169:5)
````

打开polyfills.js文件，找到这个函数

````js
function statFix (orig) {
  if (!orig) return orig
  // Older versions of Node erroneously returned signed integers for
  // uid + gid.
  return function (target, cb) {
    return orig.call(fs, target, function (er, stats) {
      if (!stats) return cb.apply(this, arguments)
      if (stats.uid < 0) stats.uid += 0x100000000
      if (stats.gid < 0) stats.gid += 0x100000000
      if (cb) cb.apply(this, arguments)
    })
  }
}
````

在第62-64行调用了这个函数

````js
fs.stat = statFix(fs.stat)
fs.fstat = statFix(fs.fstat)
fs.lstat = statFix(fs.lstat)
````

**把这三行代码注释掉就解决报错了。**
