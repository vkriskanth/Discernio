select* from activity x
where x.quarter='Q2 2026'
and x.action='add'
order by pct_of_portfolio desc