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

class Base(DeclarativeBase):
    pass

class Database():
    def __init__(self):
        self.engine = create_engine('sqlite:///music_database.db', echo=False)
        Base.metadata.create_all(self.engine)
        self.session = Session(self.engine)
    
    def display_table(self, table_name):
        print(f'Displaying {table_name} table')
        # Convert the table name to lowercase
        table_name_lower = table_name.lower()

        # Use the Table class to dynamically create a reference to the table
        table = Table(table_name_lower, Base.metadata, autoload_with=self.engine)

        q_all = self.session.query(table).all()

        if not q_all:
            print(f"No records found in {table_name}.")
            return

        columns = table.columns.keys()
        for row in q_all:
            row_data = {column: getattr(row, column) for column in columns}
            print(row_data)
            
    def add_entry(self, table_name, values):
        # Convert the table name to lowercase
        table_name_lower = table_name.lower()

        # create a reference to the table
        table = Table(table_name_lower, Base.metadata, autoload_with=self.engine)

        # Check if the table exists
        if not inspect(self.engine).has_table(table_name_lower):
            print(f'Table ({table_name}) does not exist.')
            return
        
        # Checking if there are any values missing 
        to_check = []
        if table_name == 'bands':
            to_check = Band.get_required_columns()
        elif table_name == 'albums':
            to_check = Album.get_required_columns()
        elif table_name == 'ratings':
            to_check = Rating.get_required_columns()
        for col in to_check:
            if values[col] == None:
                print(f"Couldn't add entry to the database, ({col}) is missing!")
                return
        
        # Automatically determine band_id, used when adding albums
        if 'band_id' in values and 'band_name' in values:
            print("Error: Both 'band_id' and 'band_name' provided. Please provide only one.")
            return
        elif 'band_name' in values:
            band_name = values.pop('band_name')
            band = self.session.query(Band).filter_by(name=band_name).first()
            if band:
                values['band_id'] = band.id
            else:
                print(f'Band ({band_name}) not found in the database.')
                return
            
        # handle adding rating
        if 'album_name' in values and 'value' in values:
            # I tried having some smart way to go about this 
            # but couldn't figure it out, so I just left the old method here
            self.add_rating(a_name=values['album_name'],value=values['value'])
            return
        
        # Create and add the entry
        table = Table(table_name_lower, Base.metadata, autoload_with=self.engine)
        stmt = insert(table).values(**values)
        try:
            self.session.execute(stmt)
            self.session.commit()
            print(f'Added entry to the ({table_name}) table.')
        except Exception as e:
            self.session.rollback()
            print(f'Error adding entry: {e}')
            
    def add_rating(self, a_name, value):
        q_albums = [result[0] for result in self.session.query(Album.name).all()]
        if a_name in q_albums:
            album = self.session.query(Album).filter_by(name=a_name).first()
            rating = Rating(album=album, value=value)
            self.session.add_all([rating])
            self.session.commit()
            print(f'added rating of ({value}) for ({a_name}) to the database')
        else:
            print(f'There is no album ({a_name}) in the database')
            
    def update_entry(self, table_name, column_name, conditions, new_value):
        if not inspect(self.engine).has_table(table_name.lower()):
            print(f'Table ({table_name}) does not exist.')
            return
        table = Table(table_name.lower(), Base.metadata, autoload_with=self.engine)
        conditions_text = text(" AND ".join([f"{key} = :param_{key}" for key in conditions.keys()]))
        
        stmt = update(table).where(conditions_text).values({column_name: new_value})

        try:
            parameters = {f"param_{key}": value for key, value in conditions.items()}
            parameters[f"param_{column_name}"] = new_value
            self.session.execute(stmt, parameters)
            self.session.commit()
            print(f'Updated entry in the ({table_name}) table.')
        except Exception as e:
            self.session.rollback()
            print(f'Error updating entry: {e}')

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
                print(f"Deleted an entry with id: {del_id} in table ({table_name})")
            else:
                print(f"There's no entry with id: {del_id} in table ({table_name})")
        else:
            print(f"There's no table ({table_name})")

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