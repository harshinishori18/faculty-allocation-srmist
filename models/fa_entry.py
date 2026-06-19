from config import db

class FAEntry(db.Model):
    __tablename__ = 'fa_entries'

    id               = db.Column(db.Integer, primary_key=True, autoincrement=True)
    year             = db.Column(db.String(10),  nullable=False)
    specialization   = db.Column(db.String(50),  nullable=False)
    section          = db.Column(db.String(10),  nullable=False)
    student_count    = db.Column(db.Integer,      nullable=False)
    faculty_advisor  = db.Column(db.String(100), nullable=False)
    academic_advisor = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {
            'id':               self.id,
            'year':             self.year,
            'specialization':   self.specialization,
            'section':          self.section,
            'student_count':    self.student_count,
            'faculty_advisor':  self.faculty_advisor,
            'academic_advisor': self.academic_advisor
        }