# 简历格式转换器

上传你的 PDF 简历和一份喜欢的模板简历，AI 自动将你的简历排版为模板的视觉风格。

## 架构

三阶段流水线，代码与 LLM 各司其职：

| 阶段 | 执行者 | 任务 |
|------|--------|------|
| Phase 1 | **PyMuPDF (代码)** | 精确提取模板 PDF 的排版参数（字号、边距、行高、颜色、分割线等），生成确定性 CSS |
| Phase 2 | **Kimi LLM** | 理解用户简历的语义结构（哪些是标题、公司名、日期、列表项），输出结构化 JSON |
| Phase 3 | **代码** | 将 Phase 1 的 CSS 和 Phase 2 的内容 JSON 组装为 HTML，Playwright 转 PDF |

核心原则：**代码做测量，LLM 做理解**。格式参数全部由代码精确提取，LLM 不参与任何排版决策。

## 安装

```bash
pip install -r requirements.txt
playwright install chromium
```

## 使用

```bash
python app.py
```

打开 http://localhost:8080 ，上传简历和模板即可。

## 技术栈

- **后端**: Flask + PyMuPDF + OpenAI SDK (Kimi API)
- **PDF 生成**: Playwright (headless Chromium)
- **前端**: 原生 HTML/CSS/JS
