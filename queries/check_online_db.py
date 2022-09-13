check_online_db="""
                SELECT
                      name AS [DatabaseName]
                FROM
                      master.sys.databases 
                WHERE
                    state_desc = 'ONLINE'
                AND
                  name not in ('master', 'model', 'msdb', 'tempdb', 'distribution')
                """