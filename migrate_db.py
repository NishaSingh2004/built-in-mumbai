from app import app, db
from sqlalchemy import text

with app.app_context():
    try:
        db.session.execute(text('ALTER TABLE mentor ADD COLUMN approach TEXT;'))
        db.session.execute(text('ALTER TABLE mentor ADD COLUMN mentorship_details TEXT;'))
    except Exception as e:
        print(f"Mentor alter failed (might exist): {e}")
        db.session.rollback()

    try:
        db.session.execute(text('ALTER TABLE founder ADD COLUMN approach TEXT;'))
        db.session.execute(text('ALTER TABLE founder ADD COLUMN mentorship_details TEXT;'))
    except Exception as e:
        print(f"Founder alter failed (might exist): {e}")
        db.session.rollback()

    try:
        db.session.execute(text('ALTER TABLE event ADD COLUMN next_stage_journey TEXT;'))
    except Exception as e:
        print(f"Event alter failed (might exist): {e}")
        db.session.rollback()

    try:
        db.session.execute(text('ALTER TABLE event_registration ADD COLUMN expectation TEXT;'))
    except Exception as e:
        print(f"EventRegistration alter failed: {e}")
        db.session.rollback()

    db.session.commit()
    print("Migration complete.")
