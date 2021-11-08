mkdir "%PREFIX%\etc\conda\activate.d"
COPY "%RECIPE_DIR%\activate.bat" "%PREFIX%\etc\conda\activate.d\vs%YEAR%_compiler_vars.bat"
pushd "%PREFIX%\etc\conda\activate.d"
sed -i 's/@YEAR@/%YEAR%/g' vs%YEAR%_compiler_vars.bat
sed -i 's/@VER@/%VER%/g' vs%YEAR%_compiler_vars.bat
sed -i 's/@cross_compiler_target_platform@/%cross_compiler_target_platform%/g' vs%YEAR%_compiler_vars.bat
popd
