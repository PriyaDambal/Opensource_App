# Opensource_App

# Opensource commits
This project helps development team to know the contribution of commits in opensource. 

**Objective**: Analyze the number patches submitted (committed done) by a specific user/development team to Gerrit, Android, GitLab and GitHub Which can be used by high level managers to analyze the performance of employees and teams.
**Big Idea**: 
Opensource contribution helps to reduce the cost and the maintenance by leveraging learnings in the community. Periodically generating such reports helps to understand the development teams’ contributions and align for future corrections. Expanding it to larger organizations and automated dashboards help to reduce manual efforts.

**My Audience** 
Primary
Leadership, customers and opensource communities
Secondary 
Senior management

**Tools Required**
1.	Pycharm


**What does my Audience care about**
Individual contribution to open-source community and tracking of work done. ultiple employees are working in a team contributing across multiple opensource repositories by submitting patches(code commit/merge) in repositories. We need to track the employee performance by analyzing the number of patches submitted and size of code submitted, Number of commits done per month, number of patches approved/Abandoned/merged by reviewer.


**Important questions are**
1. How many commits are done by a specific user/team in each branch?
2.How many changes were approved and merged to the main branch?
3.Most recent commit?
4.How many patches were Abandoned?
5. Trend of commits by month/year?
6. How many patches were Merged and how many are open?


**Approach Followed**
1. Writing the python code in pycharm 
2. Using libraries like streamlit, matplotlib, pandas and numpy.
3. Data from Gerrit, Gitlab, Android and GitHub websites were separately collected from corresponding Web Api URL/End points.
4. Used Python code to hit the URL and get the data for each status (open, merged, Abandoned)
5. The web response was converted to a Data frame and only required columns were selected and stored in a data frame.
6. The dataframes can be seen in the App.
7. The file path from Excel as a source is connected to the Power BI.
9. Created visualizations which help to get insights required from the management. 

**Link to access App**
https://opensourceapp-gfjx4scjxp4liej5frqhbq.streamlit.app/

**Sample UI**

<img width="608" alt="streamlit_app_sample" src="https://github.com/PriyaDambal/Opensource_App/assets/134541646/cbabb551-16c8-4dde-8e0d-2120a0c433a3">


Android and Chromebook are trademarks of Google LLC


