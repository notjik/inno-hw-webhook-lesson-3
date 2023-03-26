import sqlite3

from typing import Any
from text_utils import ansi_color, ansi_effect


class Database:
    def __init__(self,
                 db_name: str,
                 table_template: dict[str, list[dict[str, str]]] | str) -> None:
        self.conn = sqlite3.connect(db_name)
        self.cur = self.conn.cursor()
        if isinstance(table_template, dict):
            for key in table_template.keys():
                try:
                    self.cur.execute(
                        'CREATE TABLE IF NOT EXISTS {}(\n'.format(
                            key,
                        )
                        +
                        ',\n'.join(
                            '{} {}'.format(row['name'], row['desc']) for row in table_template[key])
                        +
                        '\n)')
                except sqlite3.OperationalError as err:
                    print('{}Command skipped: {}{}{}'.format(
                        ansi_color['red']['text'],
                        ansi_effect['bold'],
                        err,
                        ansi_effect['break']
                    ))
        elif isinstance(table_template, str):
            with open(table_template, 'r') as sqlfile:
                commands = sqlfile.read().split(';')
            for command in commands:
                try:
                    self.cur.execute(command)
                except sqlite3.OperationalError as err:
                    print('{}Command skipped: {}{}{}'.format(
                        ansi_color['red']['text'],
                        ansi_effect['bold'],
                        err,
                        ansi_effect['break']
                    ))
        else:
            exit('Enter the correct table template')
        self.conn.commit()

    def add(self,
            table: str,
            elems: dict[str, Any]) -> None:
        elems = elems.items()
        print("{}INSERT OR REPLACE INTO {}({}) values({}){}".format(
            ansi_color['turquoise']['text'] + ansi_effect['italic'],
            table,
            ', '.join(i[0] for i in elems),
            ', '.join("'" + str(i[1]) + "'" for i in elems),
            ansi_effect['break']))
        self.cur.execute("INSERT OR REPLACE INTO {}({}) values({})".format(
            table,
            ', '.join(i[0] for i in elems),
            ', '.join('?' * len(elems))), [i[1] for i in elems])
        self.conn.commit()
        return None

    def __del__(self) -> None:
        self.cur.close()
        self.conn.close()
        return None
