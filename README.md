# 🤖 Multi-Agents Data Analysis System

<div align="center">


**基于 Strands Agents 框架的多智能体数据分析系统**

[功能特性](#-功能特性) • [快速开始](#-快速开始) • [系统架构](#-系统架构) • [使用示例](#-使用示例) • [报告展示](#-报告展示)

</div>

---

## 📋 项目简介

Multi-Agents 是一个基于 **Strands Agents** 框架构建的多智能体协作系统，专注于自动化的数据获取、分析和可视化工作流。通过多个专业化的智能体协同工作，实现从原始数据到精美 HTML 报告的全流程自动化处理。

### 🎯 核心价值

- **🔄 全流程自动化**：从数据获取到报告生成一站式完成
- **🤝 多智能体协作**：不同智能体各司其职，高效协同
- **📊 智能数据分析**：自动识别数据模式并进行深度分析
- **🎨 精美可视化输出**：生成交互式 HTML 报告

---

## ✨ 功能特性

### 🔍 数据获取智能体
- 支持多种数据源接入（API、数据库、文件等）
- 自动数据清洗和预处理
- 增量更新和缓存机制

### 📈 数据分析智能体
- 自动统计分析
- 趋势识别和预测
- 异常检测
- 相关性分析

### 🎨 可视化智能体
- 动态图表生成（折线图、柱状图、雷达图等）
- 交互式仪表板
- 响应式 HTML 报告
- 多维度数据对比展示

### 🧠 协调智能体
- 任务分配和调度
- 智能体间通信协调
- 工作流管理
- 错误处理和重试机制

---

## 🏗️ 系统架构

```
┌─────────────────────────────────────────────────────────┐
│                    协调智能体 (Coordinator)                │
│                   任务分配 & 流程管理                        │
└─────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
┌───────────────┐  ┌───────────────┐  ┌───────────────┐
│  数据获取智能体  │  │  数据分析智能体  │  │  可视化智能体   │
│  Data Fetcher  │  │  Data Analyzer │  │  Visualizer   │
├───────────────┤  ├───────────────┤  ├───────────────┤
│ • API 调用    │  │ • 统计分析     │  │ • 图表生成     │
│ • 数据清洗    │  │ • 趋势预测     │  │ • HTML 报告    │
│ • 格式转换    │  │ • 异常检测     │  │ • 交互组件     │
└───────────────┘  └───────────────┘  └───────────────┘
        │                   │                   │
        └───────────────────┼───────────────────┘
                            ▼
                   ┌───────────────┐
                   │   HTML 报告    │
                   │  📊📈📉🎨     │
                   └───────────────┘
```

---

## 🚀 快速开始

### 环境要求

- Python 3.8+
- pip 或 conda

### 安装步骤

1. **克隆项目**

```bash
git clone https://github.com/1844909740/mutli-agents.git
cd mutli-agents
```

2. **安装依赖**

```bash
pip install -r requirements.txt
```

3. **配置环境变量**

```bash
cp .env.example .env
# 编辑 .env 文件，填入必要的配置信息
```

4. **运行示例**

```bash
python main.py
```

---

## 💡 使用示例

### 基础用例

```python
from multi_agents import MultiAgentSystem

# 初始化多智能体系统
system = MultiAgentSystem()

# 配置数据源
system.configure_data_source(
    source_type="api",
    endpoint="https://api.example.com/data",
    params={"key": "your_api_key"}
)

# 执行分析任务
result = system.run_analysis(
    analysis_type="trend_analysis",
    output_format="html"
)

# 生成报告
system.generate_report(
    output_path="./reports/analysis_report.html"
)
```

### 高级配置

```python
from multi_agents import MultiAgentSystem
from multi_agents.agents import DataFetcher, DataAnalyzer, Visualizer

# 自定义智能体配置
system = MultiAgentSystem()

# 配置数据获取智能体
system.add_agent(DataFetcher(
    name="fetcher_1",
    source="database",
    connection_string="postgresql://localhost/mydb"
))

# 配置数据分析智能体
system.add_agent(DataAnalyzer(
    name="analyzer_1",
    methods=["statistical", "ml_prediction"]
))

# 配置可视化智能体
system.add_agent(Visualizer(
    name="visualizer_1",
    template="modern_dashboard",
    interactive=True
))

# 运行工作流
system.execute_workflow()
```

---

## 📊 报告展示

Multi-Agents 系统能够自动生成专业的数据分析报告，包含多种可视化图表和详细的分析结果。以下是实际生成的报告示例：

### 📈 报告功能展示

生成的 HTML 报告包含以下核心模块：

#### 1️⃣ 设备连接成功率趋势分析
- 实时监控多设备连接状态
- 自动识别异常波动
- 对比分析不同设备性能

#### 2️⃣ 设备响应时间分析
- 追踪首帧出图时间
- 性能瓶颈识别
- 优化建议生成

#### 3️⃣ 综合性能对比
- 多维度数据展示
- 柱状图、折线图、雷达图等多种图表
- 交互式数据探索

#### 4️⃣ 智能异常检测
- 自动标记异常数据点
- 生成警告和建议
- 根因分析

### 🎨 报告特点

- ✅ **响应式设计** - 支持桌面端和移动端查看
- ✅ **交互式图表** - 基于 Chart.js，支持缩放、悬停提示等交互
- ✅ **专业配色** - 渐变色设计，视觉效果出色
- ✅ **自动化生成** - 无需人工干预，一键生成完整报告
- ✅ **数据驱动** - 基于真实数据分析，提供可操作的洞察

### 📸 报告界面预览

报告包含以下主要部分：

**报告头部**
- 显示分析时间区间、监控设备、生成日期等关键信息
- 采用渐变色背景，提升视觉吸引力

**数据摘要**
- 关键指标一目了然
- 自动高亮异常数据
- 提供主要发现总结

**可视化图表**
1. **设备连接成功率趋势图** - 折线图展示各设备7天连接率变化
2. **首帧出图时间趋势图** - 追踪设备响应速度
3. **每日性能对比图** - 柱状图对比多设备表现
4. **设备稳定性评分** - 雷达图展示综合评分

**异常分析表格**
- 详细列出每个异常事件
- 包含设备名称、日期、指标值和描述
- 使用颜色标记严重程度

**建议措施**
- 基于分析结果自动生成优化建议
- 分优先级列出改进方案
- 提供具体的执行步骤

### 💾 如何保存图表

生成报告后，您可以通过以下方式保存图表：

1. **截图工具** - 使用系统截图功能保存整个报告或单个图表
2. **浏览器右键** - 在图表上右键选择"保存图片"
3. **打印功能** - 浏览器打印功能导出为PDF
4. **开发者工具** - 使用浏览器开发者工具导出Canvas内容

---

## 📂 项目结构

```
mutli-agents/
│
├── agents/                 # 智能体模块
│   ├── __init__.py
│   ├── coordinator.py      # 协调智能体
│   ├── data_fetcher.py     # 数据获取智能体
│   ├── data_analyzer.py    # 数据分析智能体
│   └── visualizer.py       # 可视化智能体
│
├── utils/                  # 工具函数
│   ├── __init__.py
│   ├── data_processor.py   # 数据处理工具
│   └── html_generator.py   # HTML 生成工具
│
├── templates/              # HTML 模板
│   ├── default.html
│   └── modern_dashboard.html
│
├── config/                 # 配置文件
│   ├── agents_config.yaml
│   └── data_sources.yaml
│
├── examples/               # 示例代码
│   ├── basic_example.py
│   └── advanced_example.py
│
├── reports/                # 生成的报告
│   └── sample_reports/
│
├── tests/                  # 测试文件
│   └── test_agents.py
│
├── requirements.txt        # 项目依赖
├── .env.example           # 环境变量示例
├── main.py                # 主程序入口
└── README.md              # 项目文档
```

---

## 🛠️ 技术栈

- **框架**: Strands Agents
- **语言**: Python 3.8+
- **数据处理**: Pandas, NumPy
- **可视化**: Chart.js, Plotly
- **HTML 生成**: Jinja2
- **异步处理**: asyncio
- **Web 技术**: HTML5, CSS3, JavaScript

---

## 📊 数据分析能力

### 支持的分析类型

- ✅ 趋势分析
- ✅ 异常检测
- ✅ 相关性分析
- ✅ 统计分布
- ✅ 性能监控
- ✅ 预测建模

### 支持的图表类型

- 📈 折线图 (Line Chart)
- 📊 柱状图 (Bar Chart)
- 🎯 雷达图 (Radar Chart)
- 🥧 饼图 (Pie Chart)
- 📉 面积图 (Area Chart)
- 🔥 热力图 (Heatmap)

---

## 🤝 贡献指南

我们欢迎所有形式的贡献！

### 贡献流程

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

### 开发规范

- 遵循 PEP 8 代码规范
- 添加必要的注释和文档
- 编写单元测试
- 更新相关文档

---

## 📝 开发计划

- [ ] 支持更多数据源类型（MongoDB, InfluxDB等）
- [ ] 增加机器学习模型集成
- [ ] 实时数据流处理
- [ ] Web UI 管理界面
- [ ] 分布式部署支持
- [ ] 更多可视化模板
- [ ] 数据导出功能（PDF, Excel）
- [ ] 邮件自动推送报告
- [ ] 多语言支持

---

## 🎯 应用场景

- **IoT 设备监控** - 实时监控设备状态和性能
- **业务数据分析** - 销售、用户行为等数据分析
- **系统性能监控** - 服务器、应用性能追踪
- **质量监控** - 产品质量数据分析
- **运营报表** - 自动生成日报、周报、月报

---

## ❓ 常见问题

### Q: 如何添加新的数据源？
A: 在 `config/data_sources.yaml` 中添加配置，或通过 API 动态注册新数据源。

### Q: 报告生成失败怎么办？
A: 检查日志文件，确认数据格式正确，依赖库已安装。

### Q: 如何自定义报告模板？
A: 在 `templates/` 目录下创建新的 HTML 模板，参考现有模板结构。

### Q: 支持实时数据吗？
A: 当前版本支持定时任务，实时流处理功能正在开发中。

---

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

---

## 👥 作者

- **GitHub**: [@1844909740](https://github.com/1844909740)

---

## 🙏 致谢

- 感谢 [Strands Agents](https://github.com/strands-project/strands-agents) 框架提供的强大支持
- 感谢 [Chart.js](https://www.chartjs.org/) 提供优秀的图表库
- 感谢所有为本项目做出贡献的开发者

---

## 📞 联系方式

如有问题或建议，请通过以下方式联系：

- 💬 提交 [Issue](https://github.com/1844909740/mutli-agents/issues)
- 📧 发送邮件（如果需要可以添加您的邮箱）
- 💼 LinkedIn（如果需要可以添加）

---

## 🔗 相关链接

- [在线文档](https://github.com/1844909740/mutli-agents/wiki)
- [更新日志](https://github.com/1844909740/mutli-agents/releases)
- [问题反馈](https://github.com/1844909740/mutli-agents/issues)
- [讨论区](https://github.com/1844909740/mutli-agents/discussions)

---

<div align="center">

**如果这个项目对您有帮助，请给个 ⭐️ Star 支持一下！**

Made with ❤️ by the Multi-Agents Team

</div>
