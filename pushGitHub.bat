@echo off
cd /d %cd%

git add *
git commit -m "通过脚本提交文件"
git push origin master
pause