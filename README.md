# QuantPilot

智能化金融时序数据管理引擎，为量化投资提供毫秒级分析能力。

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![DuckDB Version](https://img.shields.io/badge/DuckDB-0.9.2-green)](https://duckdb.org/)

## 项目描述 
QuantPilot 是一款面向金融量化研究的高性能时序数据管理引擎，创新性地将流式处理与批量分析相结合。系统基于 DuckDB 内核深度优化，提供从数据摄入、智能存储到实时分析的全链路解决方案，特别针对高频交易场景下的低延迟查询需求设计。 

## 技术亮点 

- 🚀 亚秒级响应：列式存储 + 内存映射技术实现千万级数据聚合 &lt; 500ms 
- 📊 多频融合：支持 tick 级、分钟级、日级数据统一存储与关联分析 
- 🔮 AI 驱动优化：基于查询模式自适应的索引选择与缓存策略 
- ⚡ 混合执行引擎：实时流处理 (CEP) 与批量 OLAP 查询统一接口 
- 📡 异构数据源：东方财富 / 聚宽 / Tushare 等 API 原生支持


## 核心特性

### 实时数据流处理
- 微批处理引擎支持1秒级延迟
- CEP复杂事件处理模式
```python
# 识别跳空缺口
engine.detect_pattern(
    "price > prev(price)*1.05",
    window=timedelta(minutes=5)
)
