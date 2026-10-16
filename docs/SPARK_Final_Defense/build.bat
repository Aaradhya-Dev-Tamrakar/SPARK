@echo off
setlocal
pushd "%~dp0"
latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error main.tex
set "thesis_exit=%ERRORLEVEL%"
popd
exit /b %thesis_exit%
