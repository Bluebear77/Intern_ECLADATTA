@Bluebear77 ➜ /workspaces/Intern_ECLADATTA/Dataset/LOGICNLG & ToTTo & QTSumm (main) $ wc -l ToTTo-Orignial-URLs.csv | awk '{print $1}'
136162
@Bluebear77 ➜ /workspaces/Intern_ECLADATTA/Dataset/LOGICNLG & ToTTo & QTSumm (main) $ wc -l ToTTo-Page-ID-URLs.csv | awk '{print $1}'

123543
@Bluebear77 ➜ /workspaces/Intern_ECLADATTA/Dataset/LOGICNLG & ToTTo & QTSumm (main) $ echo $(($(wc -l < ToTTo-Orignial-URLs.csv) - $(wc -l < ToTTo-Page-ID-URLs.csv)))
12619
