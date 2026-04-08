# 使用说明

## 最简单的用法

1. 把参考专利 PDF 放到 `workspaces/default/intake/samples/`
2. 可选地把调研总结放到 `workspaces/default/intake/research-notes/`
3. 在项目根目录运行：

```sh
sh ./scripts/prepare_patent_workspace.sh
```

4. 打开 `workspaces/default/prompt-for-model.txt`
5. 把里面的提示词粘贴给大模型

## 这个脚本会自动完成什么

1. 在当前 Python 环境安装依赖
2. 检查并补齐默认 workspace 结构
3. 检查 `samples/` 下是否已有 PDF
4. 生成 `manifest.json`
5. 抽取 PDF 文本到 `temp/extracted-text/`
6. 生成最终给大模型使用的 `prompt-for-model.txt`

## 目录约定

```text
workspaces/default/
  intake/
    samples/            # 参考专利 PDF
    research-notes/     # 可选的调研总结
    notes/              # 任务补充说明
  temp/
    extracted-text/     # 脚本自动生成
  output/
    10-guides/
    15-selected-direction/
    30-patent-package/
    40-domain-accelerator/
```

## 手动执行底层脚本

```powershell
python ./skills/patent-copilot/scripts/bootstrap_workspace.py --root ./workspaces/default
python ./skills/patent-copilot/scripts/build_manifest.py --source ./workspaces/default
python ./skills/patent-copilot/scripts/extract_pdf_text.py --input-dir ./workspaces/default/intake/samples --output-dir ./workspaces/default/temp/extracted-text --force
```

## 给大模型的目标

脚本最终生成的提示词，要求大模型：

1. 读取本地 PDF 和可选调研总结
2. 自主选择一个合理且具备结构创新点的实用新型方向
3. 直接完成交底书起草、附图提示词、审核报告和审核后修订稿
4. 仅在确有必要时生成陌生领域加速页
