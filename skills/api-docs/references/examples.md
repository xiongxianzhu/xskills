# API 文档示例

本文档以虚构的「图书管理系统」API 为例，展示文档编写规范。

## 文档头部与元信息示例

```markdown
# 图书管理系统API文档_第三方调用

[TOC]

> 版本号(Version): 1.0.2
> 创建时间(Created at): 20250301
> 更新时间(Updated at): 20250306
> 作者(Authors): zhangsan
> 密级(Confidential level): **内部**
> 文档语法(Document syntax): markdown
```

## 修改记录示例

```markdown
## 修改记录

### 1.0.2

- 新增接口`3.3. 归还图书`；
- 接口`3.1. 图书查询`新增入参`category`。

### 1.0.1

- 接口`3.2. 借阅图书(下单)`新增入参`remark`；
- `1.2.1. 请求地址`补充生产环境的服务地址。
```

## 说明示例

```markdown
## 说明

该文档由图书管理系统后端提供给第三方调用。

图书管理系统(Library Management System，缩写：lms)。
```

## 请求地址示例

### 1.2.1. 请求地址

| 调用环境 |        服务地址(内网)        | 服务地址(外网) |
| :------: | :--------------------------: | :------------: |
| 生产环境 | `http://10.168.188.72:10240` |       无       |
| 测试环境 | `http://10.168.199.40:10240` |       无       |

## 错误码示例

### 2.1. 公共错误码

| 错误码 | 描述 |
| :----: | :--: |
|   0    | 成功 |
|   -1   | 失败 |

### 2.2. 业务错误码

| 错误码 |    描述    |
| :----: | :--------: |
|  1001  | 签名校验失败 |
|  2001  | 图书不存在 |
|  2002  | 库存不足   |

## 接口示例一：基础查询接口

### 3.1. 图书查询

`GET` `/lms/api/vendor/books/search/`

上行参数：

`request headers`参数：

|     参数      |  类型  | 必填 | 默认值 |                             备注                             |
| :-----------: | :----: | :--: | :----: | :----------------------------------------------------------: |
|   x-app-id    | string |  是  |        |            应用ID，如`app_3q5swjighk12zea4`             |
|  x-timestamp  | string |  是  |        | 时间戳，格式为yyyy-MM-dd HH:mm:ss，时区为GMT+8，例如：2025-03-01 12:00:00 |
|   x-format    | string |  否  |        |              响应格式，固定值为`json`               |
|   x-version   | string |  是  |        |               API版本，固定值为`1.0`                |
| x-sign-method | string |  是  |        |   签名的摘要算法，固定值为`hmac-sha256`    |
|    x-sign     | string |  是  |        |                            签名                             |

`request params`参数：

|   参数   |  类型  | 必填 | 默认值 |                       备注                       |
| :------: | :----: | :--: | :----: | :----------------------------------------------: |
| keyword  | string |  否  |        |              搜索关键词(书名/作者)               |
| category | string |  否  |        | 图书分类<br />TECH=技术<br />LIT=文学<br />SCI=科学 |
|   page   |  int   |  否  |   1    |                      页码                        |
| per_page |  int   |  否  |   20   |                    每页数量                      |

下行参数：

|    参数     |  类型  | 默认值 |       备注       |
| :---------: | :----: | :----: | :--------------: |
|    code     |  int   |        |      错误码      |
|     msg     | string |        |       消息       |
|    data     | object |        |       数据       |
| └total      |  int   |        |      总数量      |
| └books      | array  |        |    图书列表      |
| └└book_id   | string |        |      图书ID      |
| └└title     | string |        |      书名        |
| └└author    | string |        |      作者        |
| └└category  | string |        |      分类        |
| └└stock     |  int   |        |    剩余库存      |

`成功`，返回JSON示例：

```json
{
    "code": 0,
    "msg": "SUCCESS",
    "data": {
        "total": 2,
        "books": [
            {
                "book_id": "BK00001",
                "title": "Python编程指南",
                "author": "李四",
                "category": "TECH",
                "stock": 5
            },
            {
                "book_id": "BK00002",
                "title": "数据结构与算法",
                "author": "王五",
                "category": "TECH",
                "stock": 3
            }
        ]
    }
}
```

`失败`，返回JSON示例：

```json
{
    "code": -1,
    "msg": "查询失败"
}
```

## 接口示例二：带说明与枚举的写入接口

### 3.2. 借阅图书(下单)

`POST` `/lms/api/vendor/borrows/create/`

说明：

> - 同一读者同时借阅同一本书不能超过1本；
> - 借阅数量不能超过该图书的当前库存。

上行参数：

`request headers`参数：

|     参数      |  类型  | 必填 | 默认值 |                             备注                             |
| :-----------: | :----: | :--: | :----: | :----------------------------------------------------------: |
|   x-app-id    | string |  是  |        |            应用ID，如`app_3q5swjighk12zea4`             |
|  x-timestamp  | string |  是  |        | 时间戳，格式为yyyy-MM-dd HH:mm:ss，时区为GMT+8，例如：2025-03-01 12:00:00 |
|   x-format    | string |  否  |        |              响应格式，固定值为`json`               |
|   x-version   | string |  是  |        |               API版本，固定值为`1.0`                |
| x-sign-method | string |  是  |        |   签名的摘要算法，固定值为`hmac-sha256`    |
|    x-sign     | string |  是  |        |                            签名                             |

`request json`参数：

|    参数    |  类型  | 必填 | 默认值 |                             备注                             |
| :--------: | :----: | :--: | :----: | :----------------------------------------------------------: |
|  book_id   | string |  是  |        |                           图书ID                             |
| reader_id  | string |  是  |        |                           读者ID                             |
|  quantity  |  int   |  是  |        |                        借阅数量                              |
| borrow_type| string |  是  |        | 借阅类型<br />NORMAL=普通借阅<br />RENEW=续借<br />RESERVE=预约借阅 |
|   remark   | string |  否  |        |                          备注                                |

下行参数：

|      参数      |  类型  | 默认值 |         备注         |
| :------------: | :----: | :----: | :------------------: |
|      code      |  int   |        |        错误码        |
|      msg       | string |        |         消息         |
|      data      | object |        |         数据         |
| └borrow_no     | string |        |       借阅单号       |
| └return_date   | string |        | 应还日期，格式yyyy-MM-dd |

`成功`，返回JSON示例：

```json
{
    "code": 0,
    "msg": "SUCCESS",
    "data": {
        "borrow_no": "BR20250301001",
        "return_date": "2025-04-01"
    }
}
```

`失败`，返回JSON示例：

```json
{
    "code": 2002,
    "msg": "库存不足"
}
```

## 接口示例三：嵌套对象与数组

### 3.3. 归还图书

`POST` `/lms/api/vendor/borrows/return/`

说明：

> - 支持批量归还，一次最多归还10本；
> - 超期归还会在响应中返回逾期天数与罚金。

上行参数：

`request headers`参数：

|     参数      |  类型  | 必填 | 默认值 |                             备注                             |
| :-----------: | :----: | :--: | :----: | :----------------------------------------------------------: |
|   x-app-id    | string |  是  |        |            应用ID，如`app_3q5swjighk12zea4`             |
|  x-timestamp  | string |  是  |        | 时间戳，格式为yyyy-MM-dd HH:mm:ss，时区为GMT+8，例如：2025-03-01 12:00:00 |
|   x-format    | string |  否  |        |              响应格式，固定值为`json`               |
|   x-version   | string |  是  |        |               API版本，固定值为`1.0`                |
| x-sign-method | string |  是  |        |   签名的摘要算法，固定值为`hmac-sha256`    |
|    x-sign     | string |  是  |        |                            签名                             |

`request json`参数：

|     参数      |  类型  | 必填 | 默认值 |                    备注                    |
| :-----------: | :----: | :--: | :----: | :----------------------------------------: |
|    items      | array  |  是  |        |              归还项目列表                  |
| └borrow_no    | string |  是  |        |               借阅单号                     |
| └returned_at  | string |  是  |        | 归还时间<br />格式为yyyy-MM-dd HH:mm:ss   |
| └condition    | string |  是  |        | 图书状况<br />GOOD=完好<br />DAMAGED=损坏  |

下行参数：

|       参数       |  类型  | 默认值 |       备注       |
| :--------------: | :----: | :----: | :--------------: |
|       code       |  int   |        |      错误码      |
|       msg        | string |        |       消息       |
|       data       | object |        |       数据       |
| └results         | array  |        |   归还结果列表   |
| └└borrow_no      | string |        |     借阅单号     |
| └└status         | string |        | 归还状态<br />SUCCESS=成功<br />OVERDUE=逾期 |
| └└overdue_days   |  int   |        |  逾期天数(如有)  |
| └└fine           | string |        |   罚金(如有)     |

`成功`，返回JSON示例：

```json
{
    "code": 0,
    "msg": "SUCCESS",
    "data": {
        "results": [
            {
                "borrow_no": "BR20250301001",
                "status": "SUCCESS",
                "overdue_days": 0,
                "fine": "0.00"
            },
            {
                "borrow_no": "BR20250215003",
                "status": "OVERDUE",
                "overdue_days": 5,
                "fine": "2.50"
            }
        ]
    }
}
```

`失败`，返回JSON示例：

```json
{
    "code": -1,
    "msg": "归还失败"
}
```

## 接口示例四：已废除接口写法

### 3.4. ~~图书预约~~(已废除)

`POST` `/lms/api/vendor/books/reserve/`

说明：

> 目前预约功能已合并到借阅接口（borrow_type=RESERVE），故此接口不再使用。

上行参数：

`request headers`参数：

|     参数      |  类型  | 必填 | 默认值 |                             备注                             |
| :-----------: | :----: | :--: | :----: | :----------------------------------------------------------: |
|   x-app-id    | string |  是  |        |            应用ID，如`app_3q5swjighk12zea4`             |
|  x-timestamp  | string |  是  |        | 时间戳，格式为yyyy-MM-dd HH:mm:ss，时区为GMT+8 |
|   x-format    | string |  否  |        |              响应格式，固定值为`json`               |
|   x-version   | string |  是  |        |               API版本，固定值为`1.0`                |
| x-sign-method | string |  是  |        |   签名的摘要算法，固定值为`hmac-sha256`    |
|    x-sign     | string |  是  |        |                            签名                             |

`request json`参数：

|   参数    |  类型  | 必填 | 默认值 |   备注   |
| :-------: | :----: | :--: | :----: | :------: |
|  book_id  | string |  是  |        |  图书ID  |
| reader_id | string |  是  |        |  读者ID  |

下行参数：

| 参数 |  类型  | 默认值 | 备注   |
| :--: | :----: | :----: | :----: |
| code |  int   |        | 错误码 |
| msg  | string |        |  消息  |

`成功`，返回JSON示例：

```json
{
    "code": 0,
    "msg": "SUCCESS"
}
```

`失败`，返回JSON示例：

```json
{
    "code": -1,
    "msg": ""
}
```
