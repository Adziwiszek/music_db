from __future__ import annotations
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, ForeignKey, String, Text
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from sqlalchemy import inspect, insert, update, text
from flask import jsonify
import json

class Base(DeclarativeBase):
    pass

class Database():
    def __init__(self):
        self.engine = create_engine('sqlite:///music_database.db', echo=False)
        Base.metadata.create_all(self.engine)
        self.session = Session(self.engine)
    
    def get_table(self, table_name):
        table_mapping = {
        'bands': Band,
        'ratings': Rating,
        'albums': Album,
        }
        if table_name in table_mapping.keys():
            return table_mapping[table_name]
        else:
            return None
        
    def get_table_columns(self, table_name):
        table_mapping = {
            "bands": ['id', 'name'],
            "albums": ['id', 'name', 'release_year', 'band_id'],
            "Ratings": ['id', 'album_id', 'value']
        }
        if table_name in table_mapping.keys():
            return table_mapping[table_name]
        else:
            return print(f'There is no such table, ({table_name})')
    
    def get_entry(self, table_name, id):
        target_table = self.get_table(table_name=table_name)
        if target_table:
            target_entry = self.session.query(target_table).filter_by(id=id).first()
            target_table_cols = self.get_table_columns(table_name=table_name)
            if target_entry:
                target_data = {column: getattr(target_entry, column) \
                    for column in target_table_cols}
                json_data = json.dumps(target_data)
                return json_data
            else:
                return print(f'there is no item with id ({id}) in the database')
        else:
            return print(f'there is no ({table_name}) table in the database')
    
    def display_table(self, table_name, return_json=True):
        print(f'Displaying {table_name} table')
        
        table_name_lower = table_name.lower()
        table = Table(table_name_lower, Base.metadata, autoload_with=self.engine)
        # table = self.get_table(table_name)
        # if table is None:
        #     return f"There is no {table_name} table in the database!!"

        q_all = self.session.query(table).all()

        if not q_all:
            print(f"No records found in {table_name}.")
            return

        json_data_list = []
        columns = table.columns.keys()
        for row in q_all:
            row_data = {column: getattr(row, column) for column in columns}
            json_data_list.append(row_data)
            #print(type(row_data))
            #print(row_data)
        json_data = json.dumps(json_data_list, indent=2)
        if return_json:
            return json_data    
        else:
            return json_data_list
               
    def add_entry(self, table_name, values):
        # Convert the table name to lowercase
        table_name_lower = table_name.lower()

        if values is None:
            return f"Error when adding entry, there are no values"

        # Check if the table exists
        try:
            if self.get_table(table_name) is None:
                return f'Table ({table_name_lower}) does not exist.'       
        except Exception as e:
            return f"Error checking the table existence {e}"
        
        # create a reference to the table
        table = Table(table_name_lower, Base.metadata, autoload_with=self.engine)
        
        # Checking if there are any values missing 
        to_check = self.get_table_columns(table_name)
        to_check.remove('id')
        # if table_name == 'bands':
        #     to_check = Band.get_required_columns()
        # elif table_name == 'albums':
        #     to_check = Album.get_required_columns()
        # elif table_name == 'ratings':
        #     to_check = Rating.get_required_columns()
        for val_key in values.keys():
            if val_key not in to_check:
                return f"Can't add the entry to the database, there's no column {val_key} in table {table_name}"
        
            
        # Automatically determine band_id, used when adding albums
        if 'band_id' in values and 'band_name' in values:
            return "Error: Both 'band_id' and 'band_name' provided. Please provide only one."
        elif 'band_name' in values:
            band_name = values.pop('band_name')
            band = self.session.query(Band).filter_by(name=band_name).first()
            if band:
                values['band_id'] = band.id
            else:
                return f'Band ({band_name}) not found in the database.'
            
        # handle adding rating
        if 'album_name' in values and 'value' in values:
            # I tried having some smart way to go about this 
            # but couldn't figure it out, so I just left the old method here
            return self.add_rating(a_name=values['album_name'],value=values['value'])
        
        # Create and add the entry
        table = Table(table_name_lower, Base.metadata, autoload_with=self.engine)
        stmt = insert(table).values(**values)
        try:
            self.session.execute(stmt)
            self.session.commit()
            return f'Added entry to the ({table_name}) table.'
        except Exception as e:
            self.session.rollback()
            return f'Error adding entry: {e}'
            
    def add_rating(self, a_name, value):
        q_albums = [result[0] for result in self.session.query(Album.name).all()]
        if a_name in q_albums:
            album = self.session.query(Album).filter_by(name=a_name).first()
            rating = Rating(album=album, value=value)
            self.session.add_all([rating])
            self.session.commit()
            return f'added rating of ({value}) for ({a_name}) to the database'
        else:
            return f'There is no album ({a_name}) in the database'
            
    def update_entry(self, table_name, values):
        if not inspect(self.engine).has_table(table_name.lower()):
            print(f'Table ({table_name}) does not exist.')
            return
        table = self.get_table(table_name)
        print(values)
        entry_to_update = self.session.query(table).filter_by(id=values['id']).first()
        
        if entry_to_update:
            for key, value in values.items():
                if value is not None:
                    setattr(entry_to_update, key, value)
            self.session.commit()
            #updated_entry_id = values['id'
            return f"Updated entry in table: {table_name}"
        else:
            return "There is no such entry!!"

    def delete_by_id(self, table_name, del_id):
        table_mapping = {
        'bands': Band,
        'ratings': Rating,
        'albums': Album,
        }
        table_to_find = table_mapping.get(table_name)
        if table_to_find:
            to_delete = self.session.query(table_to_find).filter_by(id=del_id).first()
            if to_delete:
                self.session.delete(to_delete)
                self.session.commit()
                return f"Deleted an entry with id: {del_id} in table ({table_name})"
            else:
                return f"There's no entry with id: {del_id} in table ({table_name})"
        else:
            return f"There's no table ({table_name})"

    def delete_entry(self, table_name, column_name, value_to_delete):
        target_table = self.get_table(table_name)
        if target_table:
            try:
                query = self.session.query(target_table)
                query = query.filter(getattr(target_table, column_name) == value_to_delete)
                
                # Execute the delete operation
                query.delete()

                # Commit changes to the database
                self.session.commit()

                print(f"Entry with {column_name}={value_to_delete} deleted successfully.")
            except Exception as e:
                # Handle exceptions (e.g., SQLAlchemyError, IntegrityError) appropriately
                print(f"Error deleting entry: {e}")
                self.session.rollback()
        else:
            print("Couldn't delete the entry!")

    
class Rating(Base):
    __tablename__ = 'ratings'
    id = Column(Integer, primary_key=True)
    album_id = Column(Integer, ForeignKey('albums.id'))
    album = relationship('Album', uselist=False, back_populates='ratings')
    value = Column(Integer)
    def get_required_columns():
        return ['value', 'album_name']

class Band(Base):
    __tablename__ = "bands"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    albums = relationship('Album', back_populates='band')
    def get_required_columns():
        return ['name']
    
class Album(Base):
    __tablename__ = "albums"
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    release_year = Column(String)
    band_id = Column(Integer, ForeignKey('bands.id'))
    band = relationship('Band', back_populates='albums')
    ratings = relationship('Rating', back_populates='album')
    def get_required_columns():
        return ['name', 'release_year', 'band_name']

# Example:          
# #db.add_band('The Beatles')
# db.add_entry('bands', {'name': 'The Strokes'})
# #db.add_band('The Strokes')
# db.add_entry('bands', {'name': 'The Beatles'})
# db.add_entry('albums', {'name': 'Abbey Road', 'release_year':'1969', 'band_name':'The Beatles'})
# db.add_entry('albums', {'name': 'Rubber Soul', 'release_year':'1966', 'band_name':'The Beatles'})
# db.add_entry('ratings', {'value':96, 'album_name':'Abbey Road'})
# db.add_entry('ratings', {'value':60, 'album_name':'Rubber Soul'})
# db.display_table('ratings')
# db.display_table('bands')
# db.display_table('albums')
# db.update_entry('albums', column_name='release_year',conditions={'name':'Abbey Road'}, new_value='2004')
# db.display_table('albums')