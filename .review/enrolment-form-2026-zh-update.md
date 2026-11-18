# 2026 Enrolment Form — Chinese copy update

**Prepared:** 18 November 2026  
**Live form:** https://docs.google.com/forms/d/e/1FAIpQLSc4h9NOCLBLf8G6lmnj0pzDVODr76V0cF7ongSGhw8dcCBpgw/viewform  
**Printable form:** `enrolment-form-2026.pdf` (repository root)

**The rule for this job:** change Chinese only. Do not change English, question order, question types, required settings, validation rules, option order, page breaks, response settings, or the form URL. Do not delete and recreate questions — that changes their IDs and can break existing response data.

---

## 0. How to use this document

1. **Section 1** is the final Chinese copy. It is the source of truth. Paste from here.
2. **Section 2** is the change log. Use the English labels to find each item in Google Forms, then replace only the Chinese part.
3. **Section 3** is the Google Form procedure.
4. **Section 4** is the printable PDF procedure.
5. **Section 5** is the QA checklist.
6. **Section 6** lists points to confirm with the school before publishing.

If Section 1 and Section 2 ever differ, **use Section 1**.

The website copy is already aligned (`日校`, `维州学生编号`, `居留身份`, `邮箱`, `预备班`). This job is the Google Form and the printable PDF only; do not edit `index.html`.

Allow about 45–60 minutes for the Google Form, plus time to find and edit the PDF source. If a Section 6 point blocks you, email the school office at `office@caseychinese.org`.

---

## 1. Final Chinese copy (paste-ready)

**Form title:** `报名表` (no change; the bilingual title is `Enrolment Form 报名表`).

### 1.1 Form intro — first screen

```text
每名学生填写一份报名表，约需 10 分钟。标有 * 的问题为必填项。如暂时没有孩子的维州学生编号（VSN），可先留空，之后通过确认邮件中的链接补充。
```

### 1.2 Page 1 — 学生信息

**Section heading**

```text
学生信息
```

**Section description**

```text
注意：学生信息必须与孩子在日校入学时登记的信息完全一致。请用大写英文字母填写。
```

**Fields**

```text
姓氏
名字
中间名
其他常用名
中文姓名
出生日期
性别：女／男／其他
家庭用语
就读日校名称及校区
日校年级：幼儿园／预备班／一年级／二年级／三年级／四年级／五年级／六年级／七年级／八年级／九年级／十年级／十一年级／十二年级／其他／尚未入学
维州学生编号（VSN）
孩子以前是否在其他中文学校学过中文？ 是／否
如果是，请填写学校名称
学生居留身份
澳大利亚公民／永久居民
全额付费国际学生
其他（Other）
```

**VSN description**

```text
维州学生编号为 9 位数字，预备班至 12 年级的学生需要填写；尚未入读日校的孩子可以留空。可向孩子就读的日校查询；暂时没有的可以先留空，之后通过确认邮件中的链接补充。
```

**Residency description**

```text
如选择“其他”（Other），请注明签证类别和编号。
```

### 1.3 Page 2 — 健康信息

**Section heading**

```text
健康信息
```

**Questions**

```text
孩子是否有任何疾病（如哮喘、癫痫、过敏等）？ 是／否
如果选择“是”，请具体说明
孩子目前是否在服用任何药物？ 是／否
如果选择“是”，请具体说明
```

**Medical-plan description (first “If Yes”)**

```text
如果选择“是”，还请提供医生出具的医疗方案（如哮喘、过敏性休克等），并在孩子第一节课时交一份复印件。
```

### 1.4 Page 3 — 家庭信息

**Section heading**

```text
家庭信息
```

**Fields**

```text
住址
区
邮编
家长／监护人联系方式（主要）
家长／监护人姓名
与学生关系
手机号码
邮箱
家长／监护人／紧急联系人（备用）
紧急联系人姓名
紧急联系人与学生关系
紧急联系人手机号码
紧急联系人邮箱
```

**Emergency-contact description**

```text
如与上面的主要联系人不同，请填写。
```

### 1.5 Page 4 — 隐私通知与声明

**Section heading**

```text
隐私通知与声明
```

**Chinese privacy heading**

```text
隐私收集通知——保护隐私与信息共享
```

**Chinese privacy body**

```text
通过本报名表收集到的有关您的孩子和家庭的信息，仅会提供给因工作需要而必须知悉的学校工作人员，以便社区语言学校和教育与培训部（以下简称“该部”）开展教学、支持您的孩子，或履行法律义务，包括注意义务、反歧视法和职业健康与安全法。未经您同意，所收集的信息不会向该部以外的任何一方披露，法律另有规定的除外。有关信息共享和隐私的更多信息，请参阅该部的隐私政策：
```

**Keep the existing privacy-policy link after the colon.** The code block stops at the colon on purpose; do not delete the URL that follows it in the form.

`http://www.education.vic.gov.au/Pages/privacy.aspx`

**Chinese consent heading**

```text
家长／监护人隐私同意与声明
```

**Chinese consent body**

```text
我确认本报名表所填信息真实、准确，并已知悉且同意本报名表所附的报名条款和条件。我同意：

• 社区语言学校收集孩子的健康和个人信息；

• 社区语言学校将本报名表中孩子的个人信息披露给教育与培训部，用于核实数据和申请资助；

• 在校长或负责教师无法联系到我的情况下，由校长或教师实施其认为合理必要的急救，包括在医疗紧急情况下向专业医护人员及机构披露孩子的个人和健康信息。
```

**Declaration checkbox**

```text
我确认以上声明，并给予上述同意。
```

### 1.6 Page 5 — 年度影像使用同意书与签名

**Section heading**

```text
年度影像使用同意书
```

**Chinese photo-consent heading**

```text
年度影像使用同意书
```

**Chinese photo-consent body**

```text
学年期间，学校工作人员可能会在很多场合和活动中为学生拍照、录像或录音，记录学生参与活动的情况。我们这样做，既是为了肯定学生的参与和成绩，也是为了与家长和学校社区沟通。

本通知适用于学校收集、使用和披露的学生照片、视频或录音。家长／监护人及学校社区其他成员在学校活动（如音乐会、运动会等）中为学生拍照、录像或录音时，请尊重学生并注意安全；未经相关家长／监护人同意，不得公开发布学生的照片、视频或录音（以下统称“影像”），例如发布到社交媒体。

如对本通知有任何疑问，或希望讨论您的顾虑，请联系社区语言学校。

我同意学校拍摄或录制孩子参加课堂及学校活动的影像，并用于以下用途：

• 与学校其他家庭分享：这些影像只会发送给孩子所在班级的其他家长。

• 在学校通讯中发布。

• 在学校网站、CFCS 宣传材料及 CFCS 社交媒体上发布。
```

**Photo-consent question heading**

```text
请选择一项：
```

**Photo-consent question description**

```text
您可以随时撤回同意。但请注意，学校可能无法修改已发布的材料，也无法撤回已公开的影像。
```

**Photo-consent options**

```text
我同意社区语言学校按上述说明使用孩子的照片、视频或录音。
我不同意社区语言学校按上述说明使用孩子的照片、视频或录音。
```

**Signature heading**

```text
签名
```

**Signature description**

```text
在下方填写您的全名并提交本表，即视为您的电子签名。学校会保存一份带时间戳的签署副本，您也会通过邮箱收到一份填写内容副本。如希望在纸质表格上签字，请联系学校。
```

**Signature fields**

```text
家长／监护人姓名
家长／监护人签名——请填写全名
日期
```

**Electronic signature heading and help text**

```text
电子签名
请勾选以下两项。
```

**Electronic-signature options**

```text
我是该学生的家长或法定监护人，有权为其办理报名。
我同意以电子方式签署并接收本报名表，并确认上方填写的全名即为我的签名。
```

### 1.7 Confirmation screen — after submission

```text
谢谢！我们已收到您的报名表，稍后会与您联系。如需修改填写内容或补充孩子的维州学生编号，请使用确认邮件中的编辑链接。

Casey 中文学校校委会
```

---

## 2. Change log — current → new

Google Forms shows bilingual titles in one line, e.g. `Family name (姓氏)`. Replace only the Chinese side. Where the English and Chinese are separate blocks (privacy and photo consent), edit the block whose heading starts in Chinese.

The `#` column is the 1-based position in the form, counting section headers. It is for reference only; use the English label to find the item.

### 2.1 Form intro

| Location | Current Chinese | New Chinese |
|---|---|---|
| Form description (top of page 1) | 每名学生请填写一份报名表，约需 10 分钟。带 * 的问题为必填项。如暂时没有孩子的 VSN 号码，可先留空，之后通过确认邮件中的链接补充。 | 见 §1.1 |

### 2.2 Page 1 — 学生信息

| # | English label | Current Chinese | New Chinese | Note |
|---|---|---|---|---|
| 1 | Student Details | 学生信息 | — | No change |
| 2 | Family name | 姓氏 | — | No change |
| 3 | First name(s) | 名字 | — | No change |
| 4 | Middle name(s) | 中间名 | — | No change |
| 5 | Other chosen name(s) | 别称 | 其他常用名 | Preferred/chosen name, not an alias |
| 6 | Other name in Chinese | 中文姓名 | — | No change |
| 7 | Date of birth | 生日 | 出生日期 | Date of birth, not birthday |
| 8 | Gender | 性别；女／男／其他 | — | No change |
| 9 | Home Language | 家庭用语 | — | No change |
| 10 | Mainstream school name, campus | 在读日校名称、所在校区 | 就读日校名称及校区 | Natural word order |
| 11 | Mainstream year level | 日校年级 | — | No change |
| 11a | Year-level option | 其他／未入学 | 其他／尚未入学 | More natural |
| 12 | VSN | 维州学生号码 | 维州学生编号 | VSN already means “number”; write only `维州学生编号`. |
| 13 | Prior community language school | 有没有曾经在其他中文学校学习过中文？ | 孩子以前是否在其他中文学校学过中文？ | The old sentence was ungrammatical |
| 14 | If Yes, which school? | 如果有，请填写该学校名称 | 如果是，请填写学校名称 | Natural |
| 15 | Residency status | 居澳签证类别 | 学生居留身份 | Residency status is broader than visa class |
| 15a | Residency option 1 | 澳洲公民/永居 | 澳大利亚公民／永久居民 | Formal, unambiguous |
| 15b | Residency option 2 | 全费国际学生 | 全额付费国际学生 | Natural |
| 15c | Residency description | 其它签证类别；请注明签证编号 | 如选择“其他”（Other），请注明签证类别和编号。 | 其他, not 其它 |

**VSN label**

In the bilingual form, write only `维州学生编号` — the English title already contains `(VSN)`. The standalone Chinese copy in §1.2 shows `（VSN）` only so it reads correctly on its own. Do not add `（VSN）` to the form title.

**Student-details description**

- Current: `注意：学生的详细信息必须与学生在主流学校注册时提供的信息完全相同。请用正楷大写英文字母填写。`
- New: `注意：学生信息必须与孩子在日校入学时登记的信息完全一致。请用大写英文字母填写。`
- Why: `主流学校` → `日校`; remove redundant `详细`; `注册时提供的信息` → `入学时登记的信息`; plain instruction for both online and paper.

**VSN description**

- Current: `VSN 为 9 位数字编号，1–12 年级学生需要填写 VSN 号码。可向孩子就读的日校查询。暂时没有可先留空，之后通过确认邮件中的链接补充。`
- New: see §1.2.
- Why: `VSN 号码` is redundant; `1–12 年级` excludes Prep; add the “not yet at school” case.

**VSN validation message**

- Current: `VSN 为 9 位数字。`
- New: `维州学生编号为 9 位数字。`

**Uppercase validation message (Family name, First name, Middle name, Other chosen name)**

- Current: `请用正楷大写英文字母填写。`
- New: `请用大写英文字母填写。`

**Built-in “Other” option (residency)**

Google’s built-in “Other” option cannot be renamed. Do **not** delete it and add a new option. Leave the option itself as `Other`; put the Chinese explanation in the question description (§1.2). If the current third option was added manually rather than as Google’s built-in “Other”, rename it to `其他`.

### 2.3 Page 2 — 健康信息

| # | English label | Current Chinese | New Chinese | Note |
|---|---|---|---|---|
| 17 | Medical condition? | 是否患有任何疾病？（如哮喘、癫痫、过敏等）？ | 孩子是否有任何疾病（如哮喘、癫痫、过敏等）？ | Removes the double question mark |
| 18 | If Yes, please specify | 若“是”，请注明 | 如果选择“是”，请具体说明 | Natural |
| 19 | Currently on medication? | 目前是否正在服用任何药物？ | 孩子目前是否在服用任何药物？ | Plain Chinese |
| 20 | If Yes, please specify | 若“是”，请注明 | 如果选择“是”，请具体说明 | Same as above |

**Medical-plan description**

- Current: `若“是”，请提供医生制定的应急处理方案（如哮喘、过敏等），并在孩子第一次上课时带来一份副本。`
- New: `如果选择“是”，还请提供医生出具的医疗方案（如哮喘、过敏性休克等），并在孩子第一节课时交一份复印件。`
- Why: `应急处理方案` is narrower than “medical plan”; `anaphylaxis` is `过敏性休克`, not just `过敏`; `副本` → `复印件`; `第一次上课` → `第一节课`.

### 2.4 Page 3 — 家庭信息

| # | English label | Current Chinese | New Chinese | Note |
|---|---|---|---|---|
| 22 | Home Address | 住址 | — | No change |
| 23 | Suburb | 区 | — | No change |
| 24 | Postcode | 邮编 | — | No change |
| 25 | Parent/Guardian Contact | 主要联系方式 | 家长／监护人联系方式（主要） | Keeps the people named |
| 26 | Name of Parent/Guardian | 亲属/监护人姓名 | 家长／监护人姓名 | A relative is not necessarily a guardian |
| 27 | Relationship to student | 其与学生之关系 | 与学生关系 | Modern, plain Chinese |
| 28 | Mobile phone | 联络电话 | 手机号码 | The field is a mobile |
| 29 | Email | 电邮地址 | 邮箱 | Matches the website |
| 30 | Parent/Guardian/Emergency Contact | 次要/紧急联系方式 | 家长／监护人／紧急联系人（备用） | Natural |
| 31 | Emergency contact: name | 亲属/监护人姓名 | 紧急联系人姓名 | Avoids repeating “Parent/Guardian” awkwardly |
| 32 | Emergency contact: relationship | 其与学生之关系 | 紧急联系人与学生关系 | Natural |
| 33 | Emergency contact: mobile | 联络电话 | 紧急联系人手机号码 | Clear |
| 34 | Emergency contact: email | 电邮地址 | 紧急联系人邮箱 | Clear |

**Validation messages**

- `请填写有效的联络电话。` → `请填写有效的手机号码。` (both mobile fields)
- `请填写有效的电邮地址。` → `请填写有效的邮箱地址。` (both email fields)
- `请填写 4 位邮编。` — no change.

**Emergency-contact description**

- Current: `如与上述主要联系方式不同，请填写。`
- New: `如与上面的主要联系人不同，请填写。`

### 2.5 Page 4 — 隐私通知与声明

| # | Location | Current Chinese | New Chinese |
|---|---|---|---|
| 37 | Chinese privacy heading | 隐私收集通知——保护您的隐私并共享信息 | 隐私收集通知——保护隐私与信息共享 |
| 39 | Chinese consent heading | 家长/监护人隐私同意和声明 | 家长／监护人隐私同意与声明 |
| 40 | Declaration checkbox | 我确认上述声明并给予上述同意。 | 我确认以上声明，并给予上述同意。 |

**Chinese privacy body — replace the whole paragraph with the “Chinese privacy body” block in §1.5.**

Key changes, for review:

- `您的子女` → `您的孩子` — consistent with the website and the rest of the form.
- `教育培训部（以下简称“教育培训部”）` → `教育与培训部（以下简称“该部”）` — the abbreviation was defined as itself.
- `照顾责任` → `注意义务` — standard legal term for “duty of care”. **Verify against the Department’s Chinese template** (see §6).
- `除非这种披露是合法的` → `法律另有规定的除外` — natural legal Chinese.
- `专业第三方` → `专业医护人员及机构` — plain, specific Chinese for the medical-emergency context.
- `我承认并同意` → `已知悉且同意` — natural for terms and conditions.
- `以用于数据核实和资助目的` → `用于核实数据和申请资助`.
- `本报名表上所提供的信息真实无误` → `本报名表所填信息真实、准确`.

**Chinese consent body — replace the whole block with the “Chinese consent body” block in §1.5.**

Key changes:

- `本报名表上所提供的信息` → `本报名表所填信息`.
- `我承认并同意` → `已知悉且同意`.
- `我孩子的` → `孩子的`.
- `向……披露……，以用于数据核实和资助目的` → `将……披露给……，用于核实数据和申请资助`.
- `校长或教师（在校长或负责教师无法与本人取得联系的情况下）在其认为合理必要的情况下对我的孩子进行急救` → `在校长或负责教师无法联系到我的情况下，由校长或教师实施其认为合理必要的急救`.
- `专业第三方` → `专业医护人员及机构`.

### 2.6 Page 5 — 年度影像使用同意书与签名

| # | Location | Current Chinese | New Chinese |
|---|---|---|---|
| 41 | Page-break section heading | 影像使用同意书 | 年度影像使用同意书 |
| 43 | Chinese photo heading | 影像使用同意书 | 年度影像使用同意书 |
| 44 | Photo question heading | 请从两个选项中选择一个 | 请选择一项： |
| 46 | Name of Parent/Guardian | 亲属/监护人姓名 | 家长／监护人姓名 |
| 47 | Signature of Parent/Guardian | 亲属/监护人签名——请键入全名 | 家长／监护人签名——请填写全名 |
| 49 | Electronic signature help text | 请两项都勾选。 | 请勾选以下两项。 |

**Chinese photo-consent body — replace the whole block with the “Chinese photo-consent body” block in §1.6.**

Key changes:

- `本学年的许多场合和活动中` → `学年期间`.
- `教职员工可能会` → `学校工作人员可能会`.
- `庆祝学生的参与和成就` → `肯定学生的参与和成绩`.
- `家长/看护人` → `家长／监护人`.
- `（“图像”）` → `（以下统称“影像”）` — defines the term once, then uses it consistently.
- `与学校其他家庭分享，这些照片或录音/录像将只发送给我孩子所在班级的学校家庭。` → `与学校其他家庭分享：这些影像只会发送给孩子所在班级的其他家长。`
- `CFCS 营销` → `CFCS 宣传材料`.
- `录音/录像` → `视频或录音`.

**Photo-consent description**

- Current: `您可以随时撤销同意，但请注意，学校可能无法修改过去的出版物或撤销已进入公共领域的图像。`
- New: `您可以随时撤回同意。但请注意，学校可能无法修改已发布的材料，也无法撤回已公开的影像。`
- Why: `撤回同意` is the standard term; `已进入公共领域` is a copyright concept and not what the English says.

**Photo-consent options**

- Current: `我同意社区语言学校使用我孩子的上述照片、录像或录音。`
- New: `我同意社区语言学校按上述说明使用孩子的照片、视频或录音。`
- Current: `我不同意社区语言学校使用我孩子的上述照片、录像或录音。`
- New: `我不同意社区语言学校按上述说明使用孩子的照片、视频或录音。`

**Signature description**

- Current: `在下方键入您的全名并提交本表，即视为您的电子签名。学校会保存一份带时间戳的已签署副本，您也会通过电邮收到一份答案副本。如您希望签署纸质表格，请联系学校。`
- New: see §1.6.
- Why: `键入` → `填写`; `答案副本` → `填写内容副本`; `电邮` → `邮箱`; `已签署副本` → `签署副本`.

**Electronic-signature options**

- Current: `我是该学生的家长或法定监护人，有权为其报名。`
- New: `我是该学生的家长或法定监护人，有权为其办理报名。`
- Current: `我同意以电子方式签署和接收本报名表，并确认上方键入的全名即为我的签名。`
- New: `我同意以电子方式签署并接收本报名表，并确认上方填写的全名即为我的签名。`

### 2.7 Confirmation screen

- Current: `谢谢！我们已收到您的报名表，稍后会与您联系。如需修改答案或补充孩子的 VSN 号码，请使用发送到您邮箱的确认邮件中的编辑链接。`
- New: see §1.7.
- Why: `修改答案` → `修改填写内容`; `VSN 号码` → `维州学生编号`; the sentence about the email is shorter and natural.
- Sign-off: `Casey中文学校 校委会` → `Casey 中文学校校委会` (space after Casey, no space before 校委会). Keep the English `Casey Chinese School Committee` after the `·`.

---

## 3. Google Form — edit procedure

### 3.1 Before editing

1. Sign in to the Google account that **owns** the form. If you see “Edit” but the form is view-only, ask the owner for Editor access.
2. **Make a backup copy first:** in the form editor, `More (⋮) → Make a copy`. Name it `Enrolment Form 2026 — backup — 2026-11-18`. Do not edit the copy; it is only a rollback.
3. Edit the **live form**, not the copy. The website links to the live form’s URL; a copy has a different URL.
4. Keep the form open in one tab and this document in another.

### 3.2 Edit the text

Work from page 1 to page 5. For each item:

1. Click the **question title** or **section heading**.
2. Select only the Chinese text. Do not select the English.
3. Paste the new Chinese from Section 1.
4. Click outside the field. Google Forms saves automatically.
5. For descriptions, click the description text under the title, select the whole Chinese paragraph, and paste the new paragraph. Keep blank lines and `•` bullets. Do not paste HTML tags such as `<br>`; use normal line breaks.
6. For multiple-choice options, click each option and replace only the Chinese half after the English, e.g. `Yes 是` → keep `Yes`, change `是` only if needed.

**Important structural rules**

- Do **not** change a question’s type (short answer, paragraph, multiple choice, dropdown, date, checkbox).
- Do **not** toggle “Required” on or off.
- Do **not** change response validation (the 9-digit VSN rule, the 4-digit postcode rule, the phone and email rules).
- Do **not** reorder questions or options.
- Do **not** delete and recreate a question. Delete/recreate changes the question ID and can disconnect existing responses.
- Do **not** change the form title, page breaks, or the form URL.
- Do **not** edit the English-only privacy and photo-consent blocks (items 36, 38 and 42 in the form order). Edit the **Chinese** block below each English block.

### 3.3 Where the less obvious settings live

| What | Where |
|---|---|
| Form intro / first-screen description | Click the form title area at the top of page 1; the description is directly below the title. |
| Section description (e.g. student-details note) | Click the section heading, then the description field. |
| Validation error message | Open the question’s `⋮` menu → `Response validation`; edit the Chinese half of the error text. |
| Confirmation message | `Settings → Presentation → Confirmation message`. Edit the Chinese half only. |
| Required toggle | The `Required` switch at the bottom-right of the question card. Leave it as it is. |

### 3.4 Preview and test

1. Click the **eye icon** (Preview) at the top right.
2. Check every page on desktop width and on a phone. Long privacy/photo paragraphs are the most likely to look cramped.
3. Check that:
   - every Chinese question still has its English counterpart;
   - no `？？`, `。。`, or stray half-width punctuation remains;
   - the “Other” option on residency still opens a text box;
   - the VSN field still accepts 9 digits and still allows blank;
   - the phone and email fields still validate;
   - the photo-consent question still has exactly two options and is required.
4. Submit a **test response** with dummy data. Check the confirmation screen Chinese and the confirmation email. Use the edit link in the email once. Then delete the test response from the `Responses` tab.
5. Open the live URL in a private/incognito window to confirm the published form shows the new text.

### 3.5 If you have API access (optional, not required)

Manual editing is safer for this job. If the school has a Google Workspace admin who prefers a scripted update, the Forms API can batch-update item titles and descriptions, but it must preserve item IDs. Do not use a script that deletes and recreates items. For a one-off text update, manual editing is the lower-risk option.

---

## 4. Printable PDF — edit procedure

### 4.1 What is wrong with the current file

`enrolment-form-2026.pdf` is a **3-page, image-only PDF**. It has no text layer, so you cannot reliably edit it with a PDF text tool. Patching text into the image will produce mismatched fonts, spacing and punctuation. The PDF must be changed in its **original editable source** and re-exported.

The PDF uses the same Chinese text as the Google Form, with these differences:

- It has no electronic-signature block and no `Declaration` checkbox. That is expected for a paper form; do not add them.
- The VSN footnote is shorter: it does not mention leaving the field blank or adding the number later.
- The medical note is shorter: it does not mention bringing a copy of the medical plan to the first class.
- The residency “Other” is a checkbox line, not Google’s built-in option.
- The signature block uses `Name of Parent/Guardian`, `Signature of Parent/Guardian`, `Date`.
- The PDF’s form title is English-only (`Enrolment Form`); the Google Form says `Enrolment Form 报名表`. This is a consistency choice, not a language error. Do not add `报名表` to the PDF title unless the school asks.

### 4.2 Find the source

1. Ask the school office for the original Word / InDesign / Publisher / Canva file used to produce the 2026 form. Check shared drives, the office computer, and email attachments from the person who made the form.
2. The website repository does **not** contain the source. Do not try to reconstruct it from the PDF unless the source is genuinely lost.
3. If the source is found, open it and use Find to replace each Chinese string from Section 2. Keep all English and the layout unchanged.

### 4.3 PDF-specific wording

Use Section 1 for the main text, with these adjustments:

**Student-details note** — same as the “Section description” block in §1.2.

**VSN footnote** — use the shorter PDF version:

```text
（维州学生编号为 9 位数字，预备班至 12 年级的学生需要填写；尚未入读日校的孩子可以留空）
```

**Medical note** — use the PDF’s existing shorter structure:

```text
如果选择“是”，请具体说明，并提供医生出具的医疗方案（如哮喘、过敏性休克等）。
```

If the school wants the PDF to match the Google Form exactly, add `并在孩子第一节课时交一份复印件` to the end. Do not add it silently; confirm first.

**Privacy consent body** — the Chinese runs across the page 2–3 break. Replace the whole Chinese block, including the third bullet at the top of page 3; do not leave the old bullet behind.

**Residency “Other” line**

```text
其他（请注明签证类别和编号）：
```

**Photo-consent question heading**

```text
请选择一项：
```

**Signature block**

```text
家长／监护人姓名：
家长／监护人签名：
日期：
```

### 4.4 Re-export and replace

1. Keep A4, 3 pages, the existing margins, logo, grey section bars, table borders, checkbox squares and signature lines.
2. Use a Simplified Chinese font with all the required glyphs. Match the current sans-serif look (e.g. Noto Sans CJK SC / Source Han Sans SC / Microsoft YaHei). Check that `／`, `——`, `“”`, `•` and `VSN` render correctly.
3. Export a **text-based** PDF, not a scan or image. The file should be searchable.
4. Save as `enrolment-form-2026.pdf` — keep the exact file name. The website’s download link and `download` attribute depend on it.
5. Replace the file in the repository root. If you do not have repository access, send the new PDF to the school office and stop here; do not edit the website.
6. From the repository root, run:

```bash
python3 scripts/check-links.py
```

7. Open the PDF at 100% and check:
   - all three pages present;
   - no Chinese text overflows a cell or runs off the page;
   - the Chinese is vertically aligned with the English as before;
   - checkbox squares and signature lines are intact;
   - page 1 ends after Medical; page 2 starts with Family Details; page 3 starts with the third consent bullet;
   - the Chinese punctuation is full-width and consistent.

### 4.5 If the source is lost

Rebuild the form in Word or Google Docs using the current PDF as the visual reference and Section 1 as the text. Match the three-page structure:

- **Page 1:** logo/header, Student Details, fields, VSN, prior-school question, residency, Medical Information.
- **Page 2:** Family Details, parent/guardian contacts, emergency contact, privacy notice, privacy consent.
- **Page 3:** final consent bullet, annual photo consent, signature and date.

Do not add the electronic-signature block or the `Declaration` checkbox to the paper form. Export as a text-based PDF and follow §4.4.

---

## 5. QA checklist

### Chinese language

- [ ] No `答案` in a form context; use `填写内容` / `填写内容副本`.
- [ ] No `主流学校`; use `日校`.
- [ ] No `亲属/监护人`; use `家长／监护人`.
- [ ] No `电邮`; use `邮箱`.
- [ ] No `联络电话`; use `手机号码`.
- [ ] No `其与学生之关系`; use `与学生关系`.
- [ ] No `维州学生号码` or `VSN 号码`; use `维州学生编号`.
- [ ] No `居澳签证类别`; use `居留身份`.
- [ ] No `其它`; use `其他`.
- [ ] No `全费国际学生`; use `全额付费国际学生`.
- [ ] No `学前班`; use `预备班`.
- [ ] No double punctuation (`？？`, `。。`, `，，`).
- [ ] Full-width Chinese punctuation: `，。；：？（）“”`; use `／` for the slash in `家长／监护人`.
- [ ] Spaces around Latin terms where they help readability: `VSN`, `CFCS`.
- [ ] Consistent terms: `孩子` in parent-facing sentences, `学生` in field labels and headings.
- [ ] The Chinese matches the website’s enrolment section (`index.html` → `#enrol`): `日校`, `维州学生编号`, `居留身份`, `邮箱`, `预备班`.

### Google Form

- [ ] All 5 pages still present.
- [ ] English text unchanged, including English-only privacy and photo blocks.
- [ ] Question order, types, required settings, validation and option order unchanged.
- [ ] The residency “Other” option still works.
- [ ] The VSN field accepts 9 digits and still allows blank.
- [ ] Phone and email validation still work.
- [ ] The photo-consent question still has exactly two options and is required.
- [ ] Test response submitted; confirmation screen and email checked; test response deleted.
- [ ] Live URL opens in incognito and shows the new text.

### PDF

- [ ] 3 A4 pages.
- [ ] Text-based, searchable; not a scan.
- [ ] No text overflow or misalignment.
- [ ] Chinese font renders all glyphs.
- [ ] Checkbox squares, signature lines and section bars intact.
- [ ] English unchanged.
- [ ] File name unchanged: `enrolment-form-2026.pdf`.
- [ ] `python3 scripts/check-links.py` passes.

---

## 6. Confirm with the school before publishing

These are the main points where the Chinese involves a judgement call or a fact that should be checked. Do not block the whole update on them; flag them to the school and use the recommended wording unless told otherwise.

1. **`注意义务` (duty of care).** This is the standard legal term, but the Department may use a different term in its official Chinese template (e.g. `照管义务` or `照顾责任`). Confirm with the school’s legal/privacy contact. If they prefer another term, use it consistently in both the privacy body and any other legal text.
2. **`专业医护人员及机构` (professional third parties).** The English is broader than “medical staff”. If the school’s consent wording is meant to cover other professionals (e.g. therapists, emergency services), use `相关专业机构及人员` instead.
3. **VSN range.** The new text says `预备班至 12 年级`. Confirm this is correct for 2026 and that kindergarten / not-yet-at-school applicants may leave it blank. The old text said `1–12 年级`, which excluded Prep.
4. **Residency categories.** Confirm `全额付费国际学生` is the school’s preferred term, and that a visa number is required for every applicant who is not an Australian citizen or permanent resident.
5. **`其他常用名`.** Confirm this field means the name the child prefers to be called, not a legal alias. If it is a legal alias, use `其他姓名`.
6. **Department name.** The English still says `Department of Education and Training`. The Chinese uses `教育与培训部`. If the Department has been renamed, do not change the English in this job; flag it to the school for a separate update.
7. **Photo-consent purposes.** Confirm that `CFCS 宣传材料` covers the school’s marketing use, `学校通讯` covers the newsletter, and `CFCS 社交媒体` covers social media. Confirm the withdrawal-of-consent wording with the school’s policy.
8. **PDF content differences.** Confirm whether the PDF should keep its shorter VSN and medical notes, or match the Google Form exactly. Do not add the “bring a copy” sentence or the “leave blank” sentence to the PDF without approval.

---

## 7. What to send back

When the update is done, send the school:

1. A link to the live form and a screenshot of each of the 5 pages.
2. Confirmation that a test response was submitted and deleted.
3. The re-exported `enrolment-form-2026.pdf`.
4. A one-line note for each item in Section 6 that the school confirmed or changed.
5. The backup copy name, in case a rollback is needed.

---

*Chinese copy prepared for Casey Chinese School. English text is out of scope for this update.*
