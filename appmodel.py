import asyncio
import aiomysql

class AppModel:
    def __init__(self):
        self.result = None
        self.conn_host = '127.0.0.1'
        self.conn_port = 3306
        self.conn_user = 'root'
        self.conn_pass = 'fktrc'
        self.conn_db = 'rentdb'

    def doQuery(self,query,insert=False):

        async def exec_rentapp_query(loop,query,insert):
            conn = await aiomysql.connect(host=self.conn_host, port=self.conn_port,
                                        user=self.conn_user, password=self.conn_pass, 
                                        db=self.conn_db, charset='utf8', loop=loop)

            async with conn.cursor() as cur:
                await cur.execute(query)
                r = await cur.fetchall()
                self.result = r
                if insert:
                    await conn.commit()
            conn.close()

        loop = asyncio.get_event_loop()
        loop.run_until_complete(exec_rentapp_query(loop,query,insert))

    def history(self,data):
        query = '''
            SELECT 
                CONCAT(b.brand_name,' ',a.auto_number)
                ,r.renter
                ,DATE_FORMAT(r.rent_beg_date, '%d.%m.%Y') AS rent_beg_date
                ,DATE_FORMAT(r.rent_end_date, '%d.%m.%Y') AS rent_end_date
                ,ps.place_name
                ,pf.place_name
            FROM rent r
            LEFT JOIN auto a ON a.auto_id = r.auto_id
            LEFT JOIN brand b ON a.brand_id = b.brand_id
            LEFT JOIN place ps ON ps.place_id = r.place_start
            LEFT JOIN place pf ON pf.place_id = r.place_finish
        ;'''

        if data['car']:
            query = query[:-1]
            query += ' WHERE a.auto_id='+data['car']+';'

        self.doQuery(query)
        return self.result

    def brand_average(self):

        all_data = list()

        query = ''' SELECT * FROM brand; '''
        self.doQuery(query)
        data = self.result

        for item in data:
            query = ''' 
                SELECT 
                    CAST((SUM(DATEDIFF(r.rent_end_date,r.rent_beg_date)) / COUNT(r.rent_id)) AS DECIMAL(8,2)) as avg 
                FROM brand b
                LEFT JOIN auto a ON b.brand_id = a.brand_id
                LEFT JOIN rent r ON r.auto_id = a.auto_id
                WHERE b.brand_id='''
            query += (str(item[0])+';')
            self.doQuery(query)
            avg = self.result
            avg_c = avg[0][0]
            if avg_c == None:
                avg_c = 0
            all_data.append((item[1],avg_c))

        return all_data

    def place_average(self):

        all_data = list()

        query = ''' SELECT * FROM place; '''
        self.doQuery(query)

        start_places = self.result
        finish_places = self.result

        for start_place in start_places:
            for finish_place in finish_places:

                query = ''' 
                    SELECT 
                        CAST((SUM(DATEDIFF(r.rent_end_date,r.rent_beg_date)) / COUNT(r.rent_id)) AS DECIMAL(8,2)) as avg 
                    FROM rent r
                    WHERE r.place_start='''

                query += (str(start_place[0])+' AND r.place_finish='+str(finish_place[0])+';')
                
                self.doQuery(query)

                avg = self.result
                avg_c = avg[0][0]
                if avg_c == None:
                    avg_c = 0

                all_data.append((start_place[1],finish_place[1],avg_c))

        return all_data

    def add_rent(self,data):

        query = '''
            INSERT INTO rent (
                auto_id,
                renter,
                place_start,
                place_finish,
                rent_beg_date,
                rent_end_date
            ) VALUES (
        '''

        fields = ['Car','Renter','StartPlace','FinishPlace','BegDate','EndDate']
        dates = ['BegDate','EndDate']
        
        for field in fields:
            if data[field]:
                val = data[field] 
                if field in dates:
                    val_arr = val.split('-') 
                    val = (val_arr[2]+'-'+val_arr[1]+'-'+val_arr[0]) 
                query += ("'"+val+"',")
            else:
                query += "NULL,"

        query = query[:-1]
        query += ');'

        self.doQuery(query,True)

        return query

    def add_auto(self,data):

        query = '''
            INSERT INTO auto (
                brand_id,
                auto_number
            ) VALUES (
        '''

        fields = ['Brand','AutoNumber']
        
        for field in fields:
            if data[field]:
                query += ("'"+data[field]+"',")
            else:
                query += "NULL,"

        query = query[:-1]
        query += ');'

        self.doQuery(query,True)

        return query

    def get_auto(self):
        query = '''
            SELECT 
                a.auto_id,
                CONCAT(b.brand_name,' ',a.auto_number) AS auto_name
            FROM auto a
            LEFT JOIN brand b ON b.brand_id = a.brand_id
        ;'''
        self.doQuery(query)
        return self.result

    def get_place(self):
        query = "SELECT place_id,place_name FROM place;"
        self.doQuery(query)
        return self.result

    def get_brand(self):
        query = "SELECT brand_id,brand_name FROM brand;"
        self.doQuery(query)
        return self.result
