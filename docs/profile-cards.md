# 横幅与统计卡

视觉取自 [麻薯ta爸的博客](https://blog.mashutaba.best/)：黑白底色、粉色点缀、混合点阵、玻璃胶囊和大字排版。图形在本仓库内生成，无第三方统计图片服务。

横幅使用 SVG 内的 CSS 动画，呈现缓慢扫光和电光点缀；系统设置减少动态效果时停用动画。GitHub README 不支持博客里的 WebGPU、鼠标交互或自定义页面脚本，因此这里是适配后的独立图形。

统计来源为 GitHub REST API 的公开仓库、用户和仓库语言接口：

- 公开仓库：本人拥有的全部公开仓库，包含 fork 和主页仓库。
- 原创项目：排除 fork 和与用户名同名的主页仓库。
- 项目 Stars：上述原创项目的 Stars 总和。
- 关注者：GitHub 用户资料中的 followers。
- 代码语言：上述原创项目的默认分支语言字节数之和，前四种单列，其余合并为 Other。采用 GitHub Linguist 口径，不代表熟练程度或投入时间。

只保留汇总值、原创公开仓库名称和 UTC 更新日期，详见 [数据快照](../data/public-stats.json)。不读取私有仓库。

GitHub Actions 每天 UTC 02:17（北京时间 10:17）尝试更新，也可手动运行。GitHub 可能延迟计划任务；卡片是最后一次成功生成的快照，日期显示在公开足迹卡片中。公开仓库的计划任务可能在长期无活动后被 GitHub 停用。

本地更新需要已认证的 GitHub CLI 和 Python 3：

```sh
python3 scripts/render_profile.py
```

工作流使用平台自动提供的短期 GITHUB_TOKEN，只给当前主页仓库 contents: write 以提交生成的图形，不需要个人访问令牌。数据接口只访问公开资源。
