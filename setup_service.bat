call nssm.exe install mis_rpc_gen_hrs "%cd%\run_server.bat"
call nssm.exe set mis_rpc_gen_hrs AppStdout "%cd%\logs\mis_rpc_gen_hrs.log"
call nssm.exe set mis_rpc_gen_hrs AppStderr "%cd%\logs\mis_rpc_gen_hrs.log"
call sc start mis_rpc_gen_hrs