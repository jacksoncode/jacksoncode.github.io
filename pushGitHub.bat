@echo off
cd /d %cd%

git add *
git commit -m "commit file throug Batch"
git push origin master

REM pause