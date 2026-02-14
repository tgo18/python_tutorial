# 第一章：Python3 语法基础

## 学习目标

掌握 Python3 的核心语法，建立与 Java 的知识映射。

## Java vs Python 语法速查

```java
// Java
public class Main {
    public static void main(String[] args) {
        System.out.println("Hello World");
    }
}
```

```python
# Python —— 就是这么简洁
print("Hello World")
```

## 文件清单

| 文件 | 内容 | 重点概念 |
|------|------|---------|
| `01_types_and_variables.py` | 类型与变量 | 动态类型、不可变类型、一切皆对象 |
| `02_control_flow.py` | 控制流 | for-in、match-case、海象运算符 |
| `03_functions.py` | 函数 | 一等公民、*args/**kwargs、闭包、lambda |
| `04_oop.py` | 面向对象 | 多继承、MRO、魔术方法、property |
| `05_decorators.py` | 装饰器 | 函数装饰器、类装饰器、带参装饰器 |
| `06_generators_iterators.py` | 生成器与迭代器 | yield、惰性求值、迭代器协议 |
| `07_type_hints.py` | 类型提示 | typing 模块、泛型、Protocol |
| `08_error_handling.py` | 异常处理 | 异常层次、自定义异常、EAFP 风格 |
| `09_comprehensions.py` | 推导式 | 列表/字典/集合推导式、嵌套推导式 |

## 学习建议

1. 每个文件都可以直接运行：`python3 01_types_and_variables.py`
2. 建议边看代码边在 Python REPL (`python3 -i`) 中实验
3. 重点关注与 Java 思维模式的差异
