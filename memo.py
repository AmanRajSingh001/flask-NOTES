from flask import Flask , render_template,redirect,request,url_for
from flask_sqlalchemy import SQLAlchemy
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///notes.db"
db=SQLAlchemy(app)
class Notes(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(50))
    content=db.Column(db.String(300))
    important=db.Column(db.Boolean, default=False)
@app.route('/')
def home():
    all_notes=Notes.query.all()
    return render_template('my_notes.html', memos=all_notes)
@app.route('/add' , methods=["POST"])
def add_notes():
    user_input=request.form.get('notes_name')
    user_2_input=request.form.get('about_notes')
    new_note=Notes(name=user_input , content=user_2_input)
    db.session.add(new_note)
    db.session.commit()
    return redirect(url_for('home'))
@app.route('/delete/<int:note_id>', methods=["POST"] )
def delete_notes(note_id):
    note_to_delete=Notes.query.get(note_id)
    db.session.delete(note_to_delete)
    db.session.commit()
    return redirect(url_for('home'))
@app.route('/mark_important/<int:note_id>' , methods=['POST'])
def star_notes(note_id):
    note_to_mark=Notes.query.get(note_id)
    note_to_mark.important=not note_to_mark.important
    db.session.commit()
    return redirect(url_for('home'))
if __name__=='__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)