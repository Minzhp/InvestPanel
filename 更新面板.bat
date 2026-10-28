@echo off
cd /d "%~dp0"

echo [1/3] Building invest-publish ...
python build_publish.py || goto :err

echo [2/3] Loading credentials ...
set /p CLOUDFLARE_API_TOKEN=<cf_token.txt
set /p CLOUDFLARE_ACCOUNT_ID=<cf_account.txt

echo [3/3] Deploying to Cloudflare Pages ...
call npx.cmd --yes wrangler@3 pages deploy .\invest-publish --project-name=your-project-name --branch main || goto :err

echo.
echo ============================================
echo  Done! Live in 1-2 min:
echo  https://your-domain.example
echo ============================================
pause
exit /b 0

:err
echo.
echo FAILED. Send me a screenshot of the error above.
pause
exit /b 1
