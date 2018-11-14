from backend.lib.Config import Config
import MySQLdb
from warnings import filterwarnings

class UserDatabase:
	conn = None
	filterwarnings('ignore', category = MySQLdb.Warning)

	def connect(self):
		config = Config().getConfig()
		self.conn = MySQLdb.connect(
			host=config['mysql']['host'],
			port=config['mysql']['port'],
			user=config['mysql']['user'],
			passwd=config['mysql']['pass'],
			db=config['mysql']['db']
			)
		self.conn.autocommit(True)
		self.conn.set_character_set('utf8')

	def query(self, sql, args=None):
		try:
			cursor = self.conn.cursor()
			cursor.execute(sql,args)
		except:
			self.connect()
			cursor = self.conn.cursor()
			try:
				cursor.execute(sql,args)
			except MySQLdb.Error as e:
				print(e)
		return cursor

	def queryMany(self, sql, args=None):
		try:
			cursor = self.conn.cursor()
			cursor.executemany(sql,args)
		except:
			self.connect()
			cursor = self.conn.cursor()
			cursor.executemany(sql,args)
		return cursor