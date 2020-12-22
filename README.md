# NTHU iLMS backup tool

![Test](https://github.com/afq984/ilmsdump/workflows/Test/badge.svg) ![Lint](https://github.com/afq984/ilmsdump/workflows/Lint/badge.svg) [![Coverage Status](https://coveralls.io/repos/github/afq984/ilmsdump/badge.svg?branch=main)](https://coveralls.io/github/afq984/ilmsdump?branch=main)

[Online demo](https://ilmsdump.afq984.net)

## Installation

Requirements: Python 3.8 or later

```
python -m pip install -U https://github.com/afq984/ilmsdump/archive/main.zip
```

The same command can be used to update to the latest version.

You may want to specify `--user`, or install in a [virtual environment].

## Usage Examples

### 登入

```
ilmsdump --login
```

重新登入：

```
ilmsdump --logout --login
```

### 匯出課程

使用網址中的 Course ID 匯出 [0001](http://lms.nthu.edu.tw/course/74) 以及 [10910CS542200](http://lms.nthu.edu.tw/course/46274):

```
ilmsdump 74 46274
```

匯出所有修過的課：

```
ilmsdump enrolled
```

#### 只列出課程不下載

```
ilmsdump --dry enrolled
```

### 查看使用說明

```
ilmsdump --help
```

### 查看匯出的課程

```
ilmsserve
```

預設網址為 http://localhost:8080 ，可用 --port 來改

Or

```
podman run --rm --mount type=bind,source=$PWD/ilmsdump.out,target=/data,ro=true -p 8080:8080 ghcr.io/afq984/ilmsserve:main
```

## Features & Status

> ✔️ supported; 🚧 work in progress; ❓ maybe; ❌ lack of interest or too complicated

*   登入 ✔️
    *   PHPSESSID ✔️
    *   帳號密碼 ✔️
*   課程說明 ✔️
*   課程活動(公告) ✔️
    *   公告 ✔️
        *   附件 ✔️
    *   活動 ❌
*   上課教材 ✔️
    *   附件 ✔️
    *   Evercam/Powercam 影片 ✔️
    *   討論 ❌
*   討論區 ✔️
    *   附件 ✔️
*   作業 ✔️
    *   作業資訊 ✔️
        *   附件 ✔️
    *   已繳交作業 ✔️
        *   附件 ✔️
        *   評分 ✔️
        *   評語 ✔️
        *   分組作業 ✔️
        *   討論 ❌
*   問卷 ❌
*   線上測驗 ❌
*   出缺勤(統計) ❌
*   成績計算 ✔️
*   小組專區 ✔️
    *   討論 ❌

### See Also

[自iLMS備份課程檔案-浮水印.pdf] [backup]

[virtual environment]: https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment
[自iLMS備份課程檔案-浮水印.pdf]: http://lms.nthu.edu.tw/sys/read_attach.php?id=2470763
[backup]: https://github.com/afq984/ilmsdump/blob/backup/%E8%87%AAiLMS%E5%82%99%E4%BB%BD%E8%AA%B2%E7%A8%8B%E6%AA%94%E6%A1%88-%E6%B5%AE%E6%B0%B4%E5%8D%B0.pdf


## Development

Install in editable mode for easy modification & testing:

```
(venv) pip install -e .[dev]
```

[nox](https://nox.thea.codes/) is used to drive the tests.

### Testing

```
python -m pytest tests
# or
nox -s test
```

### Linting

```
nox -s lint
```

### Format Code

```
nox -s format
```

### Report Issues

https://github.com/afq984/ilmsdump/issues
