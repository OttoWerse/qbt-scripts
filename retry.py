import json
from subprocess import check_output

'''Set to "True" to have Missing files automatically rechecked (restarts download from the beginning)'''
RECHECK_MISSING_FILES = False

'''QBT CLI settings'''
qbt_use_system_config = False #Set to True to use QBT CLI settings, otherwise use settings below
qbt_username = 'admin'
qbt_password = 'adminadmin'
qbt_url = 'http://localhost:8080'


if __name__ == '__main__':
    try:
        if qbt_use_system_config:
            qbt_get_command = f'qbt torrent list --format json --filter errored'
        else:
            qbt_get_command = f'qbt torrent list --username {qbt_username} --password {qbt_password} --url {qbt_url} --format json --filter errored'

        qbt_get_result = check_output(qbt_get_command)
        qbt_json = json.loads(qbt_get_result)

        for qbt_entry in qbt_json:
            qbt_entry_name = qbt_entry['name']
            qbt_entry_hash = qbt_entry['hash']
            qbt_entry_state = qbt_entry['state']

            try:
                if qbt_entry_state == 'missingFiles':
                    if RECHECK_MISSING_FILES:
                        if qbt_use_system_config:
                            qbt_recheck_command = f'qbt torrent check {qbt_entry_hash}'
                        else:
                            qbt_recheck_command = f'qbt torrent check --username {qbt_username} --password {qbt_password} --url {qbt_url} {qbt_entry_hash}'

                        qbt_recheck_result = check_output(qbt_recheck_command)
                        print(f'Missing Files Rechecked for "{qbt_entry_name}" ({qbt_entry_hash})')
                    else:
                        print(f'Missing Files ignored for "{qbt_entry_name}" ({qbt_entry_hash})')
                else:
                    if qbt_use_system_config:
                        qbt_resume_command = f'qbt torrent resume {qbt_entry_hash}'
                    else:
                        qbt_resume_command = f'qbt torrent resume --username {qbt_username} --password {qbt_password} --url {qbt_url} {qbt_entry_hash}'

                    qbt_resume_result = check_output(qbt_resume_command)
                    print(f'Resumed "{qbt_entry_name}" ({qbt_entry_hash})')
            except KeyboardInterrupt:
                pass
            except Exception as e:
                print(e)

    except Exception as e:
        print(e)