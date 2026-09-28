from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# engine = create_engine("sqlite:///./tasks.db",
#                      connect_args={"check_same_thread":False})
engine = create_engine("mysql+mysqlconnector://root:MySql%402026!@localhost:3306/movie_booking")


#Database_url
#connection arguments - A dictionary of arguments
LocalSession = sessionmaker(bind=engine,
                            autoflush=True) #returns a class
Base = declarative_base()
#This returns base class