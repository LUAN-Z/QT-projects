# Scrap IP from HTML

## ✎使用方法

**从网站手动获取源代码，通过`scrapy`模块进行`IP`数据提取，存入数据库。**

`程序UI整体界面`

![1555912430890](https://github.com/LUAN-Z/images/blob/master/IP_UI.png?raw=true)



### ✔ 从[高匿IP](`https://www.xicidaili.com`)主页获取源代码

**点击 *HTML文本框* 旁的 `浏览器图标`即可跳转到该网站**

![1555911925194](https://github.com/LUAN-Z/images/blob/master/IP_1.png?raw=true)

![1555912308167](https://github.com/LUAN-Z/images/blob/master/IP_code.png?raw=true)

##### 代码示例

```html
// 示例
<body>
    //
    //
    //
<tr class="odd">
      <td class="country"><alt="Cn"></td>
      <td>117.80.137.74</td>
      <td>9999</td>
      <td>
        <a href="/2019-04-22/jiangsu">江苏苏州</a>
      </td>
      <td class="country">高匿</td>
      <td>HTTP</td>
      <td class="country">
        <div title="0.479秒" class="bar">
          <div class="bar_inner fast" style="width:95%">
            
          </div>
        </div>
      </td>
      <td class="country">
        <div title="0.095秒" class="bar">
          <div class="bar_inner fast" style="width:97%">
            
          </div>
        </div>
      </td>
      
      <td>1分钟</td>
      <td>19-04-22 13:22</td>
    </tr>
    //
    //
    //
</body>
```

### ✔连接数据库

#### ☞初次使用需创建数据库

#### 本程序数据库为`mysql`

```mysql
CREATE DATABASE IF NOT EXISTS 'ippool';
CREATE TABLE IF NOT EXISTS 'ipinfo' (
IP地址 int(10) NOT NULL primary key,
端口 int(5)，
服务器地址 varchar(20));
```

#### ☑使用时，先连接数据库



### ✔将源代码粘贴至HTML文本框

![1555912879818](https://github.com/LUAN-Z/images/blob/master/IP_paste.png?raw=true)

### ✔数据提取

##### 点击 `提取`按钮，提取数据

![1555913069184](https://github.com/LUAN-Z/images/blob/master/IP_insert.png?raw=true)

### ✔查看数据库所有记录

##### 点击 *数据显示* 标签旁边的✔，即可显示数据库储存的所有IP的记录

![1555931019846](https://github.com/LUAN-Z/images/blob/master/IP_query.png?raw=true)



## ☠注意事项

### ✘[EEEOR]: 由于目标计算机积极拒绝，无法连接

**原因：数据库未连接**

**解决方法：检查数据库连接情况**



### ✘[EEEOR]: 文本格式错误

**该程序采用正则表达式检测HTML文本框内的内容是否存在`<table id="ip_list">`**

**若查找不到该内容则响应 `文本格式错误`**

###  '✘[EEEOR]: 出现错误，数据库回滚

**数据插入过程中出现错误**