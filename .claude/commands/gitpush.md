# Git Push Skill

自动完成 git add、commit、push 三步操作，将当前目录的变更推送到远程仓库。

## 执行步骤

1. 检查当前 git 仓库状态：`git status`
2. 如果没有变更，直接告知用户，不继续执行
3. 暂存所有变更：`git add -A`
4. 分析变更内容，生成简洁的 commit message（中文）
5. 提交：`git commit -m "<自动生成的提交信息>"`
6. 推送到远程：`git push`，如果没有上游分支则使用 `git push -u origin main`（或 master）

## 执行规则

- commit message 自动根据 `git diff --cached --stat` 的内容生成，格式：`[类型] 简要描述变更内容`
- 类型参考：新增、更新、修复、删除
- 推送完成后，输出本次提交的文件数量、commit 信息和推送结果

## 示例输出

```
✓ 已暂存 3 个文件
✓ 提交：[更新] 会议记录 2026-06-27 及相关文档
✓ 推送成功 → origin/main
```

$ARGUMENTS
