table_template = {
    'users': [
        {
            'name': 'id',
            'desc': 'INT',
        },
        {
            'name': 'name',
            'desc': 'TEXT',
        },
        {
            'name': 'eee',
            'desc': 'BOOLEAN',
        }
    ]
}
unique = []
for key in table_template.keys():
    print(
        'CREATE TABLE IF NOT EXISTS {}(\n'.format(
            key,
        )
        +
        ',\n'.join(
            '{} {}'.format(row['name'], row['desc']) for row in table_template[key])
        +
        ('Unique({})'.format(', '.join(unique)) if unique else '')
        +
        '\n)')
    print('\n')
