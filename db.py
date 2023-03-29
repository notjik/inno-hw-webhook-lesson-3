import sqlite3

from typing import Any, List, AnyStr, Dict
from text_utils import ansi_color, ansi_effect, add_brackets


class Database:
    def __init__(self,
                 db_name: AnyStr,
                 table_template: Dict[AnyStr, List[Dict[AnyStr, AnyStr]]] | AnyStr) -> None:
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
            table: AnyStr,
            elems: Dict[AnyStr, Any]) -> None:
        elems = elems.items()
        str_operation = "INSERT OR REPLACE INTO {}({}) values({})".format(
            table,
            ', '.join(i[0] for i in elems),
            ', '.join('?' * len(elems)))
        print(ansi_color['white']['text'] + ansi_effect['italic'] + str_operation + ansi_effect['break'])
        self.cur.execute(str_operation, [i[1] for i in elems])
        self.conn.commit()
        return None

    def delete(self,
               table: AnyStr,
               *,
               conjunction: Dict[AnyStr, Any] = {},
               disjunction: Dict[AnyStr, Any] = {}) -> None:
        conjunction = conjunction.items()
        disjunction = disjunction.items()
        if conjunction == disjunction == {}:
            print(ansi_color['red']['text'] + ansi_effect['bold'] +
                  "Incorrect data transmitted for the operation."
                  + ansi_effect['break'])
        str_conjunction = " AND ".join("{} = ?".format(i[0]) for i in conjunction)
        str_disjunction = " OR ".join("{} = ?".format(i[0]) for i in disjunction)
        str_operation = "DELETE FROM {} WHERE ".format(table) + \
                        " AND ".join(filter(lambda x: x != '',
                                            [add_brackets(str_conjunction) if len(
                                                conjunction) > 1 else str_conjunction,
                                             add_brackets(str_disjunction) if len(
                                                 disjunction) > 1 else str_disjunction]))
        print(ansi_color['white']['text'] + ansi_effect['italic'] + str_operation + ansi_effect['break'])
        self.cur.execute(str_operation, [i[1] for i in conjunction] + [i[1] for i in disjunction])
        self.conn.commit()
        return None

    def __del__(self) -> None:
        self.cur.close()
        self.conn.close()
        return None
