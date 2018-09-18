-- Send alarm data to Automic Event Engine for automated remediation
aee_alarm = alarm.get ()
aee_command = 'C:\\Scripts\\aee\\aee_command.exe -d ' .. aee_alarm.hostname .. ' -n ' .. aee_alarm.nimid .. ' -s ' .. aee_alarm.severity
aee_command = aee_command .. ' -m \"' .. aee_alarm.message .. '\" -t "' .. aee_alarm.nimts .. '"'
action.command (aee_command)
