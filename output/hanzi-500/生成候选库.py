from pathlib import Path
from collections import Counter
import json

ROOT = Path(__file__).resolve().parent
priority = '乖回慢名让错等家不妈女胖钱闲租独饭窗老友玩糖雨试赢字人好长乐'
rows = []
groups = []
for line in (ROOT / '候选原稿.txt').read_text(encoding='utf-8').splitlines():
    if line.startswith('@'):
        group_id, topic, audience = line[1:].split('|')
        groups.append({'编号': group_id, '主题': topic, '人群': audience, '条目': []})
    elif line.strip():
        char, anchor, angle = line.split('|')
        row = {'编号': len(rows) + 1, '字': char, '主题': topic, '共鸣人群': audience,
               '词语入口': anchor, '切入角度': angle,
               '试写优先级': '优先试写' if char in priority else '常规候选',
               '字典核验': '正式写作前核对版本、读音与具体义项'}
        rows.append(row)
        groups[-1]['条目'].append(row)

assert len(rows) == 500
assert len({r['字'] for r in rows}) == 500
assert len(groups) == 20 and all(len(g['条目']) == 25 for g in groups)
assert all(len(r['字']) == 1 and '\u4e00' <= r['字'] <= '\u9fff' for r in rows)
assert all(all(str(v).strip() for v in r.values()) for r in rows)
assert len(priority) == len(set(priority)) == 30
assert set(priority) <= {r['字'] for r in rows}

intro = '''# 每天一个字：500字候选库

整理日期：2026年10月14日。共500个不重复的简体汉字，分20个主题，每组25字。编号是检索编号，不是365天发布顺序。

## 选字逻辑与小红书受众

沿用六项标准：具体人群、真实场景、理解变化、与字有关、新的观察、一个核心问题。每条提供一个词语入口及一条选题切口，供选题会使用；它们是编辑建议，不是字典释义或已经验证的读者反馈。

面向小红书，优先考虑年轻人在求学、工作、离家、独住、恋爱与友情中的经验，并加强女性身份、外貌评价、家庭分工和自我表达；同时保留男性、父母和不同年龄读者能参与的生活入口。快乐、食物、兴趣、自然和语言趣味贯穿其中，避免全年只围绕焦虑与委屈。

参考材料为千瓜2025年公开报告，属于第三方行业观察，不当作2026年平台全体用户的精确画像，也不能证明某个选题必然获得高互动。上面的受众选择是基于这些材料作出的编辑判断。

- [千瓜：2025活跃用户研究报告，2025-04-24](https://www.qian-gua.com/information/detail/3149)：作为年轻用户及家居、食物、运动、养育等生活场景的参考。
- [千瓜：2025女性营销研究数据报告，2025-03-13](https://www.qian-gua.com/Home/ArticleDetail?id=3107)：作为女性身体感受、身份变化和代际互助选题的参考。

## 使用边界

这是一轮候选筛选，不是500篇定稿，也不是500条已核验的《新华字典》释义。尚未指定字典版本。正式写作时逐字核对字头、读音、义项及页码，再区分“字典怎么解释”“自己经历过什么”“自己的延伸理解”。词语入口未必都是字典收录词条。多音字要按实际用词核对读音；字源和拆字解释须另查可靠依据，不能凭字形编造。

童年场景是供作者回忆、采访或征集真实故事的提示，不能直接冒充个人经历。相似主题要轮换发布，并用不同核心问题区分；候选库不等于已实证达成9分门槛，不虚填字义核验分或传播评分。

## 优先试写的30字

'''
lookup = {r['字']: r for r in rows}
parts = [intro, '、'.join(priority), '\n\n这些字兼顾校园、家庭、独立生活、小快乐和语言趣味，优先级是编辑判断。可先选其中10—15字试写，以有内容的评论和读者补充的真实故事判断共鸣，再决定365天的最终排期。\n']
for g in groups:
    parts.append(f"\n## {g['编号']}｜{g['主题']}（25字）\n\n共鸣人群：{g['人群']}。\n\n")
    parts.append(' '.join(r['字'] for r in g['条目']) + '\n\n')
    parts.append('| 编号 | 字 | 词语入口 | 切入角度 | 试写 |\n|---|---|---|---|---|\n')
    for r in g['条目']:
        parts.append(f"| {r['编号']:03d} | **{r['字']}** | {r['词语入口']} | {r['切入角度']} | {'★' if r['字'] in priority else '—'} |\n")
parts.append('''
## 从500字到365天

500字先作为储备，保留135个替换空间。先确认作者手头有哪些真实故事，再核对字典并写出10—15篇样稿。日更排期跨主题轮换：相邻几天避免都讲顺从、受伤或告别，也不连续发布语义过近的字。多音字趣味篇可穿插在较重的情绪篇之间。

对“乖、懂、听、让、忍”，分别守住“奖励机制、过早承担、听见自己、分配公平、如何判断忍耐”五个问题；对“回、归、乡、家”，分别守住“回去的行动、到家的感受、故乡的来处、归属的日常”。如果写成同一篇换一个字，保留最扎实的一篇，其余重做切口或由候选字替换。

入选最终365字前，每篇填完：这个字讲给谁／哪件真实小事／小时候怎么理解／后来有什么变化／字典义项支点／这篇只回答什么。字典事实或真实场景缺失的篇目先不排期。
''')
(ROOT / '500字候选库.md').write_text(''.join(parts), encoding='utf-8')
(ROOT / '500字候选库.json').write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding='utf-8')
index = ['# 500字总览\n\n共500字，已做单字和全库去重检查。详细切入角度见同目录《500字候选库.md》。\n']
for g in groups:
    index.append(f"\n{g['编号']}. **{g['主题']}**：" + '、'.join(r['字'] for r in g['条目']) + '\n')
(ROOT / '500字总览.md').write_text(''.join(index), encoding='utf-8')
report = {'条目数': len(rows), '唯一汉字数': len(set(r['字'] for r in rows)),
          '主题数': len(groups), '每组条目数': {g['主题']: len(g['条目']) for g in groups},
          '优先试写数': sum(r['试写优先级'] == '优先试写' for r in rows),
          '检查范围': '结构、数量、去重、字段完整性；不代表字典义项或受众效果已经核验'}
(ROOT / '校验结果.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(report, ensure_ascii=False, indent=2))
