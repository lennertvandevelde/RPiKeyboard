from .Database import Database
import time

cont = True

class DataRepository:
    @staticmethod
    def json_or_formdata(request):
        if request.content_type == 'application/json':
            gegevens = request.get_json()
        else:
            gegevens = request.form.to_dict()
        return gegevens

    @staticmethod
    def read_noten_by_keyid(idkey):
        sql = "SELECT keyName, Leadinst, Backinst, idNote1, idNote2, idNote3, idNote4, idNote5, idNote6, idNote7, idNote8  FROM mydb.key WHERE idkey = %s"
        params = [idkey]
        return Database.get_one_row(sql, params)

    @staticmethod
    def read_played_note_by_id(id):
        sql = "SELECT * from PlayedNotes where id = %s"
        params = [id]
        return Database.get_one_row(sql, params)

    @staticmethod
    def add_played_note(noteduration, idPlaySession, idNotes):
        sql = "INSERT INTO PlayedNotes(noteduration, idPlaySession, idNotes) VALUES(%s,%s,%s)"
        params = [noteduration, idPlaySession, idNotes]
        return Database.execute_sql(sql, params)

    @staticmethod
    def add_new_playsession(trackName, duration, datum, keyId, backtrackInterval, notes):
        sql = "INSERT INTO PlaySession(trackName, duratiion, datum, keyId, backtrackInterval) VALUES(%s,%s,%s,%s,%s)"
        params = [trackName, duration, datum, keyId, backtrackInterval]
        res = Database.execute_sql(sql, params)
        for note in notes:
            DataRepository.add_played_note(notes[note]["noteduration"], res, notes[note]["idNotes"])
        return res

    @staticmethod
    def read_notename_by_id(id):
        sql = "SELECT NoteName from Notes where idNotes = %s"
        params = [id]
        return Database.get_one_row(sql, params)


    @staticmethod
    def get_all_tracks():
        sql = 'SELECT idPlaySession, trackName, duratiion FROM PlaySession WHERE idPlaySession > 1'
        return Database.get_rows(sql)
        
    @staticmethod
    def get_current_track_id():
        sql = 'SELECT Max(idPlaySession) +1 as curtra FROM mydb.PlaySession;'
        return Database.get_one_row(sql)
    
    @staticmethod
    def get_played_notes(idPlaySession):
        sql = 'SELECT idNotes, noteduration from PlayedNotes where idPlaySession = %s'
        params = [idPlaySession]
        return Database.get_rows(sql, params)

    @staticmethod
    def get_lead_by_id(idPlaySession):
        sql = 'SELECT Leadinst FROM mydb.key where idkey IN (SELECT keyID from PlaySession where idPlaySession = %s) '
        params = [idPlaySession]
        return Database.get_one_row(sql, params)

    @staticmethod
    def delete_notes_by_track(idPlaySession):
        sql = 'delete from PlayedNotes where idPlaySession = %s'
        params = [idPlaySession]
        return Database.execute_sql(sql, params)
    
    @staticmethod
    def delete_track(idPlaySession):
        data = DataRepository.delete_notes_by_track(idPlaySession)
        print(data)
        sql = 'delete from PlaySession where idPlaySession = %s'
        params = [idPlaySession]
        return Database.execute_sql(sql, params)
