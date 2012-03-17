from shotwelldb.utils import id_to_thumb, regexp
import sqlite3

class Library:
    """
    Instance of shotwell library
    """
    def __init__(self, dbfile=None):
        self.db = {}
        if dbfile:
            self.open(dbfile)
        
    def open(self, dbfile):
        self.db = sqlite3.connect(dbfile)
        self.db.create_function('regexp', 2, regexp)

    def photo_dir_match(self, pattern):
        """
        List of ids for all photos in the database with a path matching
        pattern.
        """
        c = self.db.cursor()
        c.execute("SELECT id FROM PhotoTable WHERE REGEXP(?,filename)", 
                  [pattern])
        return [photo[0] for photo in c.fetchall()]

    def get_tag(self, name):
        """
        Get id and members for tag "name"
        """
        c = self.db.cursor()
        c.execute("SELECT id,photo_id_list FROM TagTable WHERE name=?", 
                  [name])
        return c.fetchone()

    def get_event(self, name):
        """
        Get id of event "name"
        """
        c = self.db.cursor()
        c.execute("SELECT id FROM EventTable WHERE name=?", [name])
        return c.fetchone()[0]

    def get_eventid(self, id):
        """
        Get name of event with specified id
        """
        c = self.db.cursor()
        c.execute("SELECT id,name FROM EventTable WHERE id=?", id)
        return c.fetchone()

    def tag_exists(self, tag):
        """
        Check whether tag with name "tag" exists
        """
        return self.get_tag(tag) is not None

    def event_exists(self, event):
        """ 
        Check whether event with name "event" exists
        """
        return self.get_event(event) is not None

    def tag_hasphoto(self, tag, photoid):
        """
        Check if photo is already marked with specified tag
        """
        if not self.tag_exists(tag):
            return False
        photos = self.get_tag(tag)[1]
        if photos is None:
            return False
        return id_to_thumb(photoid) in photos.split(",")

    def photo_hastags(self, photoid):
        """
        Check tags for specified photo
        """
        c = self.db.cursor()
        c.execute("SELECT id,name FROM TagTable WHERE name LIKE ? ",
                  ["%%%s%%" % id_to_thumb(photoid)])
        return c.fetchall()

    def add_event(self, event):
        c = self.db.cursor()
        c.execute("INSERT INTO EventTable (name) VALUES (?)", [event])
        self.db.commit()
        return c.lastrowid

    def set_photo_eventid(self, photoid, eventid):
        self.db.execute("UPDATE PhotoTable SET event_id=? WHERE id=?",
                        [eventid,photoid])
        self.db.commit()

    def add_tag(self, tag, photoids):
        c = self.db.cursor()
        c.execute("""
            INSERT INTO TagTable (name, photo_id_list) VALUES (?,?)""", 
                  [tag, ",".join([id_to_thumb(photoid) 
                                  for photoid in photoids])])
        self.db.commit()
        return c.lastrowid

    def add_tag_photoid(self, tag, photoid):
        tagentry = self.get_tag(tag)
        if tagentry[1] is None:
            photos = []
        else:
            photos = tagentry[1].split(",")
        assert id_to_thumb(photoid) not in photos
        photos.append(id_to_thumb(photoid))
        self.db.execute("UPDATE TagTable SET photo_id_list=? WHERE id=?",
                        [",".join(photos),tagentry[0]])
        self.db.commit()

    def add_tag_photolist(self, tag, photoids):
        tagentry = self.get_tag(tag)
        if tagentry[1] is None:
            photos = []
        else:
            photos = tagentry[1].split(",")
        for photo in [id_to_thumb(photoid) for photoid in photoids]:
            if photo not in photos:
                photos.append(photo)

        self.db.execute("UPDATE TagTable SET photo_id_list=? WHERE id=?",
                        [",".join(photos),tagentry[0]])
        self.db.commit()

