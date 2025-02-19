import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy import render_er
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    def serialize(self): 
        return {"id":self.id,"email":self.email,"password":self.password,}

class Planet(db.Model): 
    __tablename__ = 'planet' 
    id = Column(Integer, primary_key=True)  
    planet_name=Column(String(15),nullable=False) 
    planet_climate=Column(String(15),nullable=False) 
    planet_residents=Column(Integer,nullable=False) 
    def serialize(self): 
        return {"id":self.id,"planet_name":self.id,"planet_climate":self.planet_climate,"planet_residents":self.planet_residents}

class Character(db.Model): 
    __tablename__ = 'character' 
    id = Column(Integer, primary_key=True)  
    birth_year=Column(String(25),nullable=False) 
    character_name=Column(String(25),nullable=False) 
    species=Column(String(25),nullable=False) 
  

    
    def serialize(self):
        return {"id":slef.id,"birth_year":self.birth_year,"character_name":self.character_name,"species":self.species} 
   
class Favorite(db.Model):  
    __tablename__ = 'favorite' 
    id = Column(Integer, primary_key=True) 
    planet_id=Column(Integer,ForeignKey('planet.id')) 
    character_id=Column(Integer,ForeignKey('character.id')) 
    user_id=Column(Integer,ForeignKey('user.id'))
     
    def serialize(self):
        return {"id":self.id,"planet_id":self.planet_id,"character_id":self.character_id,"user_id":self.user_id}

 

  

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        } 
   