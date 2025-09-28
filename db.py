# app/db.py
last_updated = Column(DateTime, default=datetime.utcnow)


class Screening(Base):
__tablename__ = 'screenings'
id = Column(Integer, primary_key=True)
user_id = Column(Integer)
remitter_json = Column(JSON)
beneficiary_json = Column(JSON)
entity_type = Column(String)
threshold = Column(Integer)
created_at = Column(DateTime, default=datetime.utcnow)
summary = Column(JSON)


class Hit(Base):
__tablename__ = 'hits'
id = Column(Integer, primary_key=True)
screening_id = Column(Integer)
sanctions_entity_id = Column(Integer)
score = Column(Integer)
matched_fields = Column(JSON)
ai_verdict = Column(String)
ai_confidence = Column(Integer)
ai_comment = Column(Text)
human_decision = Column(String)
human_comment = Column(Text)
actioned_by = Column(String)
actioned_at = Column(DateTime)


class Upload(Base):
__tablename__ = 'uploads'
id = Column(Integer, primary_key=True)
filename = Column(String)
uploader_id = Column(Integer)
row_count = Column(Integer)
created_at = Column(DateTime, default=datetime.utcnow)
status = Column(String)


def create_db_and_tables():
Base.metadata.create_all(engine)


def get_session():
return SessionLocal()


# Some simple metrics for dashboard
import pandas as pd


def get_metrics():
s = get_session()
total_screenings = s.query(Screening).count()
total_hits = s.query(Hit).count()
true_matches = s.query(Hit).filter(Hit.human_decision == 'true_match').count()
false_positives = s.query(Hit).filter(Hit.human_decision == 'false_match').count()
recent = s.query(Screening).order_by(Screening.created_at.desc()).limit(10).all()
recent_rows = []
for r in recent:
recent_rows.append({'id': r.id, 'created_at': r.created_at.isoformat(), 'entity_type': r.entity_type})
return {
'screenings': total_screenings,
'hits': total_hits,
'true_matches': true_matches,
'false_positives': false_positives,
'recent_screenings': pd.DataFrame(recent_rows)
}
