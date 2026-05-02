# Query 5: Personalized 30-Day Data Analysis Interview Study Plan

## [Task Description]

Design a **30-day personalized study plan** targeting **data analysis job interviews** for an **intermediate Python learner**. The plan should comprehensively consider the user's current skill level, target job requirements, daily available study time, and learning style preferences, generating a structured daily learning task schedule to help the user systematically prepare for interviews.

## [Task Background]

Data analysis is a popular career direction today, with job requirements spanning SQL data querying, Python data processing (Pandas/NumPy), data visualization, statistics fundamentals, machine learning introduction, and other skills. For learners preparing to switch careers or job hunt, systematically mastering these skills within limited time is a major challenge.

Traditional study plans often lack personalization and struggle to adapt to different learners' foundation levels and schedules. This task requires designing an intelligent study plan generation system that automatically generates a customized 30-day learning path based on user profiles (current level, target position, available time, learning preferences), with optional calendar file output for reminders.

## [User Profile]

- **Current Skill Level**: Intermediate Python learner
  - Already mastered: Python basic syntax, basic data structures (list/dict/tuple), function definitions, file I/O
  - To improve: Data processing libraries (Pandas/NumPy), SQL, data visualization, statistics, machine learning
- **Target Position**: Data Analyst / Data Analysis role
  - Job requirements: SQL proficiency, Python data processing, data visualization, statistics fundamentals, basic machine learning knowledge
- **Daily Available Study Time**: 2-3 hours (adjustable based on actual availability)
- **Learning Style Preference**: Video instruction + hands-on practice + reading documentation (comprehensive learner)

## [Objectives]

1. **Generate daily learning task schedule**: Including learning topics, recommended resource links, and practice exercises
2. **Dynamically adjust difficulty and pace**: From basics to advanced, step by step
3. **Output in interactive calendar format (.ics file)**: Importable into Google Calendar/Outlook for reminder setup

## [Output Requirements]

### 1. **Markdown Study Plan** (Required)

Suggested filename: `data_analysis_interview_30day_study_plan.md`

**Structure Requirements:**

```markdown
# Data Analysis Interview 30-Day Study Plan

## User Profile
- Current skills: Intermediate Python
- Target position: Data Analyst
- Daily study time: 2-3 hours
- Learning preference: Video + hands-on + reading

---

## Week 1: SQL Fundamentals & Data Querying (Day 1-7)

### Weekly Objective
Master basic SQL syntax, able to perform single-table queries, multi-table joins, aggregate statistics

### Day 1: SQL Introduction - SELECT Basic Queries
**Learning Topics:**
- SQL basic concepts: database, table, row, column
- SELECT statement: querying single table data
- WHERE clause: conditional filtering
- ORDER BY: sorting

**Learning Resources:**
1. [Video] SQL Tutorial for Beginners - freeCodeCamp (YouTube, first 1 hour)
   Link: https://www.youtube.com/watch?v=HXV3zeQKqGY
2. [Reading] W3Schools SQL Tutorial - SELECT Statement
   Link: https://www.w3schools.com/sql/sql_select.asp
3. [Practice] SQLBolt - Interactive SQL Lessons (Lesson 1-3)
   Link: https://sqlbolt.com/

**Practice Tasks:**
- Complete all exercises in SQLBolt Lessons 1-3
- Exercise: Query specific conditions in a sample database (e.g., "find all orders with sales > 1000")

**Estimated Time:** 2.5 hours

---

### Day 2: SQL Advanced - JOIN Multi-table Connections
**Learning Topics:**
- INNER JOIN
- LEFT JOIN / RIGHT JOIN
- Multi-table join practice

**Learning Resources:**
1. [Video] SQL Joins Explained - Programming with Mosh (YouTube, 15 min)
2. [Practice] SQLBolt - Lesson 6-7 (Joins)
3. [Reading] Mode Analytics SQL Tutorial - Joins
   Link: https://mode.com/sql-tutorial/sql-joins/

**Practice Tasks:**
- Complete SQLBolt JOIN exercises
- Hands-on: Join orders table and customers table, calculate total order amount per customer

**Estimated Time:** 2.5 hours

---

(Day 3-7 continued...)

---

## Week 2: Python Data Processing - Pandas & NumPy (Day 8-14)

### Weekly Objective
Proficiently use Pandas for data cleaning, transformation, aggregation; master NumPy array operations

### Day 8: Pandas Introduction - DataFrame Basics
...

---

## Week 3: Data Visualization & Statistics (Day 15-21)

### Weekly Objective
Master Matplotlib/Seaborn charting; understand descriptive statistics, probability distributions, hypothesis testing

### Day 15: Matplotlib Basic Charting
...

---

## Week 4: Machine Learning Introduction & Comprehensive Projects (Day 22-30)

### Weekly Objective
Understand basic machine learning concepts; complete 1-2 end-to-end data analysis projects

### Day 22: Machine Learning Overview & sklearn Introduction
...

### Day 28-30: Comprehensive Project Practice
**Project 1: E-commerce User Behavior Analysis**
- Dataset: Kaggle - E-commerce Data
- Tasks: User profiling, purchase behavior prediction, visualization report
- Skills integration: SQL data extraction + Pandas cleaning + visualization + simple modeling

**Project 2: Financial Data Analysis (Optional)**
- Dataset: Yahoo Finance stock data
- Tasks: Trend analysis, correlation analysis, risk assessment

---

## Appendix: Recommended Learning Resources Summary

### Online Courses
- Coursera: "Data Analysis with Python" (IBM)
- DataCamp: "Data Analyst with Python Career Track"
- Kaggle Learn: Free Pandas/SQL/visualization tutorials

### Recommended Books
- "Python for Data Analysis" - Wes McKinney
- "SQL in 10 Minutes" - Ben Forta

### Practice Platforms
- LeetCode Database problems (SQL practice)
- Kaggle Datasets (real dataset practice)
- HackerRank SQL/Python challenges

---

## Study Tips

1. **Daily review**: Review previous day's key points before starting each day (15 min)
2. **Practice-focused**: 70% time on hands-on practice, 30% on theory
3. **Project-driven**: From Week 3, try small projects on Kaggle
4. **Interview prep**: Last week, organize common interview questions, simulate interview scenarios
5. **Take notes**: Use Notion/GitHub to record daily study notes and code

```

**Content Key Points:**
- Organized by week/day, 30 days total
- Each day includes: Learning topics, resources (video/article/book links), practice tasks, estimated time
- Each week sets a theme objective
- Last week includes comprehensive practice project(s)

### 2. **.ics Calendar File** (Optional)

Suggested filename: `study_plan_calendar.ics`

**Requirements:**
- Importable into Google Calendar, Outlook, Apple Calendar and other major calendar applications
- Create one calendar event per day, titled with the day's learning topic
- Event description includes learning task summary and resource links
- Set reminders (e.g., every day at 9:00 AM or 7:00 PM)

**Example .ics format:**
```
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Data Analysis Study Plan//EN
BEGIN:VEVENT
DTSTART:20260207T090000Z
DTEND:20260207T110000Z
SUMMARY:Day 1: SQL Introduction - SELECT Basic Queries
DESCRIPTION:Learn SQL basic syntax\nResources: SQLBolt Lesson 1-3\nExercise: Complete basic query exercises
BEGIN:VALARM
TRIGGER:-PT15M
ACTION:DISPLAY
DESCRIPTION:SQL study starts in 15 minutes
END:VALARM
END:VEVENT
...
END:VCALENDAR
```

### 3. **Content Requirements**

1. **Fit within 30-day time limit**: Arrange 2-3 hours of learning content per day, moderate content volume
2. **Reasonable difficulty progression**: From SQL basics -> Python data processing -> visualization & statistics -> ML introduction
3. **Cover core skills**:
   - SQL: Queries, joins, aggregation, subqueries
   - Python: Pandas (data cleaning/transformation/aggregation), NumPy (array operations)
   - Visualization: Matplotlib, Seaborn
   - Statistics: Descriptive statistics, probability distributions, hypothesis testing
   - Machine Learning: Linear regression, logistic regression, decision trees (introductory level)
4. **Real, usable learning resources**: Recommended videos, articles, and book links must actually exist and be high quality
5. **Include practice projects**: Last week arrange 1-2 comprehensive projects integrating learned skills
6. **Strong executability**: Clear task descriptions, easily accessible resources, reasonable time arrangements


## [Hints]

### Skill System Planning
- **Week 1**: SQL data query fundamentals (single table, multi-table, aggregation)
- **Week 2**: Python data processing (Pandas, NumPy)
- **Week 3**: Data visualization (Matplotlib, Seaborn) + statistics fundamentals
- **Week 4**: Machine learning introduction + comprehensive project practice

### Learning Resource Recommendations
- **SQL**: SQLBolt (interactive exercises), Mode Analytics Tutorial, LeetCode Database
- **Python/Pandas**: Kaggle Learn, DataCamp, "Python for Data Analysis"
- **Visualization**: Matplotlib official tutorials, Seaborn Gallery
- **Statistics**: Khan Academy Statistics, "Statistical Learning Methods"
- **Machine Learning**: Coursera Machine Learning, Scikit-learn documentation

### Practice Project Suggestions
- Data analysis projects from Kaggle Datasets (e.g., Titanic, House Prices)
- Real business scenario simulations (e-commerce user analysis, financial data analysis)

### .ics File Generation
- Python library: `icalendar`
- Online tools: iCalendar.org, ICS File Generator

### Personalization Adjustment Suggestions
- Adjust task volume based on user's daily available time
- Adjust resource type ratio based on learning preference (video/reading/hands-on)
- Adjust focus based on target position specific requirements (e.g., emphasis on business analytics or technical analytics)

