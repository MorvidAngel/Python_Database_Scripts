check_offline_db="""
                SELECT
                      name AS [DatabaseName]
                FROM
                      master.sys.databases 
                WHERE
                    state_desc = 'OFFLINE'
                AND
                  name not in ('master', 'model', 'msdb', 'tempdb', 'distribution')
                """