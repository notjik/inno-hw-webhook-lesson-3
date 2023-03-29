import sqlite3

from typing import Any, List, AnyStr, Dict
from text_utils import ansi_color, ansi_effect, add_brackets


class Database:
    def __init__(self,
                 db_name: AnyStr,
                 db_template: Dict[AnyStr, List[Dict[AnyStr, AnyStr]]] | AnyStr) -> None:
        """
        Creating a database object and connecting to her
        :param db_name: string name database
        :param db_template: dictionary database template in the format "Dict[AnyStr, List[Dict[AnyStr, AnyStr]]]", where the first element is the name of the table, and the second element are the columns of your table; OR in the format "AnyStr" with the path to the SQL file
        """
        self.conn = sqlite3.connect(db_name)
        self.cur = self.conn.cursor()
        if isinstance(db_template, dict):
            for key in db_template.keys():
                try:
                    self.cur.execute(
                        'CREATE TABLE IF NOT EXISTS {}(\n'.format(
                            key,
                        )
                        +
                        ',\n'.join(
                            '{} {}'.format(row['name'], row['desc']) for row in db_template[key])
                        +
                        '\n)')
                except sqlite3.OperationalError as err:
                    print('{}Command skipped: {}{}{}'.format(
                        ansi_color['red']['text'],
                        ansi_effect['bold'],
                        err,
                        ansi_effect['break']
                    ))
        elif isinstance(db_template, str):
            with open(db_template, 'r') as sqlfile:
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
        """
        Add row in your table
        :param table: string table name
        :param elems: dictionary with a key in the form of a column name and a value in the form of a row value
        :return: None
        """
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
        """
        Delete row in your table
        :param table: string table name
        :param conjunction: dictionary with keys in the form of a column name and a value in the form of a row value that will need to be intersect
        :param disjunction: dictionary with keys in the form of a column name and a value in the form of a string value that will need to be integrate
        :return: None
        """
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
        """
        Deleting an object and closing a database connection
        :return: None
        """
        self.cur.close()
        self.conn.close()
        return None
