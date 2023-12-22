import argparse
import db_operations
from tests import test_client 

server_url = "http://localhost:5000/"

def add_entry(values, table, db):
    db.add_entry(table_name=table,values=values)
    
def show_entries(table, db):
    res = db.display_table(table)
    print(res)

def get_entry(table, db, id):
    res = db.get_entry(table,id)
    print(res)

def delete_entry(table, db, column, value):
    db.delete_entry(table_name=table, column_name=column, value_to_delete=value)

def update_entry(db, table, column_name, new_value,conditions):
    db.update_entry(table_name=table, column_name=column_name, 
                    new_value=new_value, conditions=conditions)

def main():
    parser = argparse.ArgumentParser(description='There are 3 tables currently \
        bands, albums, ratings ')
    db = db_operations.Database()

    parser.add_argument('table', nargs=1, type=str)
    subparsers = parser.add_subparsers(title='Actions', dest='action', 
                                       required=True, help='Available actions')  
    parser.add_argument('--api', help='specifies if user wants to use api or not', \
        action='store_true')
    parser_add = subparsers.add_parser('add', help='add an entry')
    parser_add.add_argument('--ryear', type=str, help='release year of an album (in str format)')
    parser_add.add_argument('--band_name', type=str, help='name of a band')
    parser_add.add_argument('--album_name', type=str, help='name of an album')
    parser_add.add_argument('--rating', type=int, help='rating of an album, form 0 to 100')
    
    parser_update = subparsers.add_parser('update', help='update a value in a row \
                                          if has some value that matches that of condition_val in condition_col')
    parser_update.add_argument('--column', type=str, help='name of a column whose row will be updated')
    parser_update.add_argument('--new_value', help='this is the value that will replace the old one')
    parser_update.add_argument('--condition_col', type=str, help='column in which condition_val will be looked for')
    parser_update.add_argument('--condition_val', help='row with this value in condition_col will have its value replaced')
    
    parser_delete = subparsers.add_parser('delete', help='delete an entry (currently only by giving its id)')
    parser_delete.add_argument('--id', type=int, help='id used for deleting an entry')  
    parser_delete.add_argument('--column', help='entries with given values in this column will be deleted')
    parser_delete.add_argument('--value', help='entries with this value in specified column will be deleted')
    
    parser_show = subparsers.add_parser('show', help='displays a table')
    parser_show.add_argument('--id', help='id of an entry', type=int)
    
    args = parser.parse_args()
    
    tab = args.table[0]
    if args.action == '--help':
        print('asgvjhbk')
    if args.action == 'add':
        # setting values dictionary for add method
        values = {}
        if tab == 'bands':
            values = {'name':args.band_name}
        elif tab == 'albums':
            values = {'name':args.album_name, 
                    'release_year':args.ryear, 
                    'band_name':args.band_name}
        elif tab == 'ratings':
             values = {'value': args.rating, 
                    'album_name':args.album_name}
        else:
            print(f"There's no table {tab}!")
        # executing the add function
        if args.api:
            test_client.api_add_entry(base_url=server_url, values=values, table_url=tab) 
        else:
            add_entry(values=values,table=tab,db=db)         
    elif args.action == 'show':
        if args.id is not None:
            if args.api:
                test_client.api_get_by_id(base_url=server_url,id=args.id)
            else:
                get_entry(table=tab, db=db, id=args.id)
        else:
            if args.api:
                test_client.api_get_table(base_url=server_url, table_name=tab)
            else:
                show_entries(table=tab, db=db)
    elif args.action == 'delete':
        if args.api:
            test_client.api_delete_entry_by_id(base_url=server_url, table_url=tab, id=args.id)
        else:
            delete_entry('bands', column_name=args.column, value_to_delete=args.value)    
    elif args.action == 'update':
        conditions = {args.condition_col:args.condition_val}
        update_entry(db=db, table=tab,
                     column_name=args.column, 
                     new_value=args.new_value,
                     conditions=conditions)
    else:
        print(f"There's no such action as {args.action}!!")
    db.session.close()

if __name__ == '__main__':
    main()
