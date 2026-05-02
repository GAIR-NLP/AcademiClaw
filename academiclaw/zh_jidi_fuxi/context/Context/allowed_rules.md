# Allowed Rules & Constraints  
 
The assistant MUST follow all rules below. 
 
--- 
 
## 1) Knowledge Source Restriction (No External Search) 
 
### Allowed 
- Use ONLY the provided course PDFs (converted to text) in the Context. 
- You may perform reasoning and synthesis based on the provided PDFs. 
 
### Forbidden 
- Any information not contained in the provided PDFs. 
 
 
**If a concept is not found in the PDFs**, you must write: 
> “该信息未在提供的课件中出现，无法确认。” 
 
--- 
 
## 2) No Hallucination / No Fabrication 
 
The assistant must not invent: 
- Terms, definitions, scientific mechanisms, or data not present in the PDFs. 
- Page numbers or slide references that do not exist. 
- “Fake diagrams” or “fake citations”. 
 
If uncertain, the assistant must either: 
- explicitly state uncertainty, or 
- mark it as "Not found in slides". 
 
--- 
 
## 3) Mandatory Evidence Citation (PDF + Page) 
 
All key factual statements MUST be supported by citations with: 
- **PDF filename** 
- **page number or page range** 
- optional short evidence excerpt (≤ 20 words) 
 
### Required citation format (must match exactly) 
 
Use this format: 
 
- **【来源：<PDF文件名>，第 <页码> 页】** 
- or for ranges: 
- **【来源：<PDF文件名>，第 <起始页>-<结束页> 页】** 
 
Examples: 
- 【来源：走进极地2025-第10节.pdf，第 12 页】 
- 【来源：第十三课-极地资源与治理.pdf，第 4-6 页】 
 
### Citation Coverage Requirements 
- The mock exam must cite source for every question (file + page range). 
 
--- 
 
## 4) Output Structure MUST Follow output_format.md 
 
The assistant must strictly follow: 
- file outputs required 
- section headers 
- JSON schema if required 
- question counts & exam structure 
 
Any missing section will be penalized in grading. 
 
--- 
 
## 5) Language and Style Requirements 
- Use Chinese (zh-CN) as default. 
- Keep explanations exam-oriented: 
  - concise, structured, clear, easy to memorize 
  - include key terms and typical answer templates 
- Avoid overly long narrative paragraphs. 
- Use bullet lists and tables where appropriate. 
 
--- 
 
## 6) Integrity Rules (Exam Question Quality) 
- Questions must be solvable from the PDFs. 
- For each question: 
  - Must provide **standard answer** 
  - Must provide **reasoning/analysis** 
  - Must cite **source PDF + page** 
 
If any question cannot be supported by the PDFs, it must be removed or revised. 
 
--- 
 
## Summary Checklist 
Before finalizing, check: 
- [ ] No external facts introduced 
- [ ] Every key statement has valid citation 
- [ ] All sections exist and are complete 
- [ ] Each exam question has answer + explanation + citation 
- [ ] Output follows output_format.md strictly 
