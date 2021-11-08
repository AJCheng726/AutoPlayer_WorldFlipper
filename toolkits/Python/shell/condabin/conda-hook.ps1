$Env:CONDA_EXE = "C:/Users/Administrator/Documents/Python Scripts/auto_player/toolkits/Python\Scripts\conda.exe"
$Env:_CE_M = ""
$Env:_CE_CONDA = ""
$Env:_CONDA_ROOT = "C:/Users/Administrator/Documents/Python Scripts/auto_player/toolkits/Python"
$Env:_CONDA_EXE = "C:/Users/Administrator/Documents/Python Scripts/auto_player/toolkits/Python\Scripts\conda.exe"
$CondaModuleArgs = @{ChangePs1 = $True}

Import-Module "$Env:_CONDA_ROOT\shell\condabin\Conda.psm1" -ArgumentList $CondaModuleArgs
Remove-Variable CondaModuleArgs