#!/usr/bin/env python3
"""coze-guize-V1 引用有效性校验。

检查全仓 Markdown / 模板中对相对路径（checklists|workflows|references|core|templates|docs）的
反引号引用是否存在，用于守护「唯一权威源 + 索引引用」：文件重命名/删除后，
靠本脚本在提交或 CI 前发现失效引用，避免人工同步遗漏造成死链。

用法：
    python3 scripts/verify-references.py [仓库根目录，默认当前目录]

退出码：0 = 全部有效；1 = 存在死链。
"""
import os
import re
import sys
import glob

PROJECT_ROOT = sys.argv[1] if len(sys.argv) > 1 else "."

# 项目运行时产物、非本仓库文件，但模板已覆盖：引用合法，跳过存在性检查
RUNTIME_ARTIFACT_PREFIXES = ("docs/",)

# 引用形如 `checklists/交付前检查.md` / `templates/执行计划.md.template`
REF_RE = re.compile(r"`(?P<p>(?:checklists|workflows|references|core|templates|docs)/[^\s`]+?\.md(?:\.template)?)`")

ALLOWED_EXTS = (".md", ".template")

def main() -> int:
    files = []
    for ext in ALLOWED_EXTS:
        files += glob.glob(os.path.join(PROJECT_ROOT, "**", "*" + ext), recursive=True)
    # 排除 git / cozeproj 内部与前缀点目录
    excluded = (os.path.join(PROJECT_ROOT, ".git"), os.path.join(PROJECT_ROOT, "assets"))
    files = [
        f for f in files
        if not any(f.startswith(ex) for ex in excluded) and not f.startswith(PROJECT_ROOT + os.sep + ".codegraph")
    ]

    refs = []
    for file in files:
        try:
            with open(file, encoding="utf-8") as fh:
                txt = fh.read()
        except (OSError, UnicodeDecodeError):
            continue
        for m in REF_RE.finditer(txt):
            refs.append((os.path.relpath(file, PROJECT_ROOT), m.group("p")))

    broken = []
    for src, ref in sorted(set(refs)):
        if ref.startswith(RUNTIME_ARTIFACT_PREFIXES):
            continue  # 运行时产物，模板已覆盖，不强制存在
        if not os.path.exists(os.path.join(PROJECT_ROOT, ref)):
            broken.append((src, ref))

    if broken:
        print("❌ 发现死链 %d 条：" % len(broken))
        for src, ref in broken:
            print("   ", src, "->", ref)
        print("\n修复：恢复被引用文件，或更新引用为真实路径。")
        return 1

    print("✅ 全部 %d 条相对路径引用均有效，无死链（docs/ 运行时产物已按模板覆盖豁免）。" % len(refs))
    return 0

if __name__ == "__main__":
    sys.exit(main())