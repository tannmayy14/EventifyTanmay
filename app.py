import os
import mysql.connector,sys
import datetime
from mysql.connector import Error
from flask import Flask, flash, request, jsonify, render_template,redirect, url_for,session
from flask_mail import Mail,Message
from random import randint
from PIL import Image, ImageDraw, ImageFont
import json

app = Flask(__name__)
app.secret_key = 'eventify123secretkey@'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Your SMTP server
app.config['MAIL_PORT'] = 465  # SMTP port (often 587 for TLS,SSL 465)
app.config['MAIL_USE_SSL'] = True  # Use TLS
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_SUPPRESS_SEND']=False
app.config['MAIL_USERNAME'] = 'eventify35@gmail.com'  # Your email
app.config['MAIL_PASSWORD'] = 'usbp jcsg pywp hwcy'  # Your email account password
app.config['MAIL_DEFAULT_SENDER'] = 'eventify35@gmail.com'  # Default sender email address

mail = Mail(app)


@app.route('/',methods=['GET', 'POST'])
def renderLoginPage():
    events = runQuery("SELECT * FROM events")
    branch =  runQuery("SELECT * FROM branch")
    if request.method == 'POST':
        Name = request.form['FirstName'] + " " + request.form['LastName']
        Mobile = request.form['MobileNumber']
        Branch_id = request.form['Branch']
        Event = request.form['Event']
        Email = request.form['Email']

        if len(Mobile) != 10:
            return render_template('loginfail.html',errors = ["Invalid Mobile Number!"])

        if Email[-4:] != '.com':
            return render_template('loginfail.html', errors = ["Invalid Email!"])

        if len(runQuery("SELECT * FROM participants WHERE event_id={} AND mobile={}".format(Event,Mobile))) > 0 :
            return render_template('loginfail.html', errors = ["Student already Registered for the Event!"])

        if runQuery("SELECT COUNT(*) FROM participants WHERE event_id={}".format(Event)) >= runQuery("SELECT participants FROM events WHERE event_id={}".format(Event)):
            return render_template('loginfail.html', errors = ["Participants count fullfilled Already!"])

        runQuery("INSERT INTO participants(event_id,fullname,email,mobile,college,branch_id) VALUES({},\"{}\",\"{}\",\"{}\",\"COEP\",\"{}\");".format(Event,Name,Email,Mobile,Branch_id))

        return render_template('index.html',events = events,branchs = branch,errors=["Succesfully Registered!"])

    return render_template('index.html',events = events,branchs = branch)
    


@app.route('/loginfail',methods=['GET'])
def renderLoginFail():
    return render_template('loginfail.html')


@app.route('/admin', methods=['GET', 'POST'])
def renderAdmin():
    if request.method == 'POST':
        UN = request.form['username']
        PS = request.form['password']

        cred = runQuery("SELECT * FROM admin")
        print(cred)
        for user in cred:
            if UN==user[0] and PS==user[1]:
                session['admin_logged_in'] = True
                return redirect('/eventType')

        return render_template('admin.html',errors=["Wrong Username/Password"])

    return render_template('admin.html')    



@app.route('/eventType',methods=['GET','POST'])
def getEvents():
    eventTypes = runQuery("SELECT *,(SELECT COUNT(*) FROM participants AS P WHERE T.type_id IN (SELECT type_id FROM events AS E WHERE E.event_id = P.event_id ) ) AS COUNT FROM event_type AS T;") 

    events = runQuery("SELECT event_id,event_title,(SELECT COUNT(*) FROM participants AS P WHERE P.event_id = E.event_id ) AS count FROM events AS E;")

    types = runQuery("SELECT * FROM event_type;")

    location = runQuery("SELECT * FROM location")
    if not session.get('admin_logged_in'):  # Check if admin is logged in
        return redirect(url_for('renderAdmin')) 

    if request.method == "POST":
        try:
            Name = request.form["newEvent"]
            fee=request.form["Fee"]
            participants = request.form["maxP"]
            Type=request.form["EventType"]
            Location = request.form["EventLocation"]
            Date = request.form['Date']
            runQuery("INSERT INTO events(event_title,event_price,participants,type_id,location_id,date) VALUES(\"{}\",{},{},{},{},\'{}\');".format(Name,fee,participants,Type, Location,Date))

        except:
            EventId=request.form["EventId"]
            runQuery("DELETE FROM events WHERE event_id={}".format(EventId))

    return render_template('events.html',events = events,eventTypes = eventTypes,types = types,locations = location) 


@app.route('/eventinfo')
def rendereventinfo():
    events=runQuery("SELECT *,(SELECT COUNT(*) FROM participants AS P WHERE P.event_id = E.event_id ) AS count FROM events AS E LEFT JOIN event_type USING(type_id) LEFT JOIN location USING(location_id);")

    return render_template('events_info.html',events = events)

@app.route('/participants',methods=['GET','POST'])
def renderParticipants():
    
    events = runQuery("SELECT * FROM events;")

    if request.method == "POST":
        Event = request.form['Event']

        participants = runQuery("SELECT p_id,fullname,mobile,email FROM participants WHERE event_id={}".format(Event))
        return render_template('participants.html',events = events,participants=participants)

    return render_template('participants.html',events = events)


@app.route('/send_participation_email', methods=['POST'])
def send_participation_email():
    pemail = request.form.get('par_email')
    participant_name = request.form.get('participant_name')
    event_name = request.form.get('event_name')
    
    email_body = f"""
    Hello {participant_name},

    Thank you for registering for {event_name}. This email confirms your participation in the event. We're excited to have you with us!

    Best,
    Eventify Team
    """
    try:
        msg = Message(f"Confirmation for {event_name}",
                      recipients=[pemail])
        msg.body = email_body
        mail.send(msg)
        flash('Email sent successfully!', 'success')
    except Exception as e:
        flash(f'Error sending email: {e}', 'danger')

    return redirect(url_for('renderParticipants'))

@app.route('/generate_certificate', methods=['POST'])
def generate_certificate():
    participant_email = request.form.get('par_email')
    participant_name = request.form.get('participant_name')
    event_name = request.form.get('event_name')
    
    # Load a background image for the certificate
    # Note: Use os.path.join for platform-independent path handling
    background = Image.open("static/images/certificate_template.png")  # Use forward slashes or os.path.join for compatibility

    # Create a Drawing context
    drawn = ImageDraw.Draw(background)

    # Load a font
    # Ensure the font path is correct. You might need to provide an absolute path if the relative path doesn't work
    font_for_participant = ImageFont.truetype("static//Kollektif-Bold.ttf", size=96)  # Larger font size for participant name
    font_for_event = ImageFont.truetype("static//Kollektif-Bold.ttf", size=48)
    # Calculate text size and position for participant name
    text_width= drawn.textlength(participant_name, font=font_for_participant)
    x = 925
    y = 650  # Adjust Y coordinate as needed

    # Draw text for participant name
    drawn.text((x, y), participant_name, fill="black", font=font_for_participant)

    # Calculate text size and position for event name
    event_text_width = drawn.textlength(event_name, font=font_for_event)
    event_x =1150
    event_y = 920  # Adjust Y coordinate as needed

    # Draw text for event name
    drawn.text((event_x, event_y), event_name, fill="black", font=font_for_event)

    # Save the generated image
    # Use underscores or dashes in file names to avoid issues with spaces in URLs
    certificate_path = f"static/output/{participant_name.replace(' ', '_')}_{event_name.replace(' ', '_')}_certificate.png"
    background.save(certificate_path)

    msg = Message("Your Certificate of Participation",
                  recipients=[participant_email])
    msg.body = f"Dear {participant_name},\n\nPlease find attached your certificate of participation in {event_name}."
    with app.open_resource(certificate_path) as cert:
        msg.attach(filename=os.path.basename(certificate_path), content_type="image/png", data=cert.read())
    mail.send(msg)

    flash('Certificate sent successfully!', 'success')
    return redirect(url_for('renderParticipants'))  # Redirect to a confirmation page or back to the form
    

def runQuery(query):

    try:
        db = mysql.connector.connect( host='localhost',database='Eventify',user='root',password='seitaroot123@')

        if db.is_connected():
            print("Connected to MySQL, running query: ", query)
            cursor = db.cursor(buffered = True)
            cursor.execute(query)
            db.commit()
            res = None
            try:
                res = cursor.fetchall()
            except Exception as e:
                print("Query returned nothing, ", e)
                return []
            return res

    except Exception as e:
        print(e)
        return []

    db.close()

    print("Couldn't connect to MySQL")
    return None

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/admin')
if __name__ == "__main__":
    app.run(debug=True) 
    
