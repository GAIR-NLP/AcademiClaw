Query:
---

[Query Description]
Based on the provided academic papers, perform a detailed analysis of each paper and generate a professional academic paper analysis PPT.

**Task Requirements:**
1. Read and understand all provided paper PDF files
2. Perform in-depth analysis of each paper, extracting core content
3. **First write a detailed paper analysis summary report** (Markdown format)
4. Based on the analysis summary report, use Python's `python-pptx` library to generate the PPT

**Paper Analysis Summary Report Requirements (papers_summary.md):**
This is the foundation for PPT generation and must be completed first. The report should include:

1. **Overview Section**
   - Research field overview of all papers
   - Relationship analysis between papers (technical evolution, method comparison, complementary relationships, etc.)
   - Overall research trend summary

2. **Detailed Analysis of Each Paper** (in paper order)
   - Paper basic information (title, authors, conference/journal, year)
   - Research background and motivation (field status, existing problems, research objectives)
   - Core contributions (3-5 innovation points, with specific descriptions)
   - Method details (technical approach, model architecture, key algorithms)
   - Experiment analysis (datasets, evaluation metrics, main results, comparison with baselines)
   - Strengths and weaknesses analysis (advantages and limitations of the method)
   - Personal insights (evaluation of the paper, inspirations, potential improvements)

3. **Cross-Paper Comparative Analysis**
   - Method comparison table (horizontal comparison of method characteristics across papers)
   - Performance comparison (if shared datasets exist)
   - Applicable scenario analysis

4. **Summary and Outlook**
   - Key technical points summary
   - Future research direction suggestions

**PPT Content Requirements:**
Based on the paper analysis summary report, each paper's analysis should include the following sections (at least 1 slide per section):
1. **Paper Basic Information**: Title, authors, publication venue/journal, year
2. **Research Background and Motivation**: Field status, existing problems, research motivation
3. **Core Contributions**: Main innovations and contributions of the paper (3-5 points)
4. **Methods/Model Architecture**: Detailed description of core methods or models (may include flowchart illustrations)
5. **Experimental Setup**: Datasets, evaluation metrics, comparison methods
6. **Experimental Results**: Main experimental results (tables recommended for display)
7. **Analysis and Discussion**: Ablation studies, visualization analysis, key findings
8. **Limitations and Future Work**: Paper limitations and future research directions
9. **Summary**: Core takeaways of the paper

**PPT Format Requirements:**
1. **Cover Page**: Include "Multi-Paper Analysis" main title, list of all paper titles, generation date
2. **Table of Contents Page**: Clearly list all papers and their corresponding page ranges
3. **Overview Page**: Cross-paper relationship analysis (based on the summary report's overview section)
4. **Separator Pages**: Add a separator page before each paper's analysis, showing paper title and authors
5. **Comparison Page**: Cross-paper method comparison table (based on the summary report's comparative analysis)
6. **Ending Page**: Include "Thank You" or "Q&A"

**PPT Design Specifications:**
1. Slide dimensions: Widescreen 16:9 (13.333 x 7.5 inches)
2. Color scheme: Use a unified professional color scheme (dark blue theme recommended)
3. Font sizes:
   - Title: 32-40pt, bold
   - Subtitle: 20-24pt
   - Body: 18-20pt
   - Table content: 12-14pt
4. Each page should not have too much content, maintain clarity and readability
5. Appropriate use of bullet points and numbered lists
6. Tables should have clear headers and border styles

**Output Requirements:**
1. **Paper analysis summary report**: `papers_summary.md` (must be completed first)
2. **PPT file**: `papers_analysis.pptx`
3. **Structure file**: `ppt_structure.json`
4. **Code**: `generate_ppt.py`

**ppt_structure.json Format Requirements:**
```json
{
  "title": "PPT main title",
  "total_slides": total_slide_count,
  "total_papers": paper_count,
  "generation_time": "generation time in ISO format",
  "summary_file": "papers_summary.md",
  "papers": [
    {
      "paper_id": 1,
      "title": "paper title",
      "authors": "author list",
      "venue": "publication venue/journal",
      "year": "publication year",
      "start_slide": start_page_number,
      "end_slide": end_page_number,
      "sections": [
        {
          "section_name": "section name",
          "slide_number": page_number,
          "content_summary": "content summary (under 50 words)"
        }
      ]
    }
  ],
  "design_info": {
    "color_scheme": "color scheme description",
    "slide_dimensions": "slide dimensions",
    "font_settings": {
      "title_font_size": "title font size",
      "body_font_size": "body font size"
    }
  }
}
```

[Context]
File list:
- `context/paper1.pdf` (first paper to analyze)
- `context/paper2.pdf` (second paper to analyze)
- `context/paper3.pdf` (third paper to analyze)
- `context/paper4.pdf` (fourth paper to analyze)
- https://python-pptx.readthedocs.io/ (python-pptx official documentation)
