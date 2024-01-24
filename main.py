from flask import Flask, request, render_template, redirect, send_file, url_for,session
from flask_mail import Mail, Message
import steganography 
import secrets
import string
import os

# Generate a random password with a length of * characters
def generate_random_key(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    random_key = ''.join(secrets.choice(characters) for _ in range(length))
    return random_key


app = Flask(__name__)
# Generate a random password with a length of 32 characters
app.secret_key = generate_random_key(32)

# !Config for mail
#todo uncomment this for config mail
# app.config['MAIL_SERVER'] = ''  # Replace with your SMTP server
# app.config['MAIL_PORT'] = 0  # Replace with the SMTP port
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USERNAME'] = ''  # Replace with your email address
# app.config['MAIL_PASSWORD'] = ''  # Replace with your email password

# mail = Mail(app)
# !=====================
# index get request
@app.route("/")
def index():
    return render_template("index.html")

#download file
@app.route('/download/<path:filename>', methods=['POST'])
def download(filename):
    if request.method == 'POST' and session.get('_imgname')==filename:
        return send_file('encrypted/'+filename, as_attachment=True, download_name=filename)
    else:
        return render_template('error.html', error = 'No file for downloading' )

#upload file
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return render_template('error.html', error ='No file uploaded' )
    file = request.files['file']
    try:
        process = request.form["selectedOption"]
    except:
        return render_template("error.html", error="You didn`t select option")
    
    if file.filename == '':
        return render_template('error.html', error = 'No selected file')
    # if file.filename.endswith('.txt'):     enother one method for one type check
    # if file and allowed_file(file.filename):
    # Process the file upload
    file.save('uploads/' + file.filename)
        # return 'File uploaded successfully'
    if os.path.splitext(file.filename)[1] != ".png":
        os.remove('uploads/' + file.filename)
        return render_template('error.html', error = 'Invalid file format')
    session['_imgname'] = file.filename
    # redirects from radiobuttons
    if process == "encr":
        return redirect(url_for("encrypt"))
    if process == "dec":
        return redirect(url_for("decode"))

#process of decoding
@app.route("/decode",methods=["GET","POST"])
def decode():
    if request.method == 'POST':
        password = request.form.get('password')
        if password is None or password.strip() == "":
            return render_template('error.html', error =  "Some problem with your password")
        else:
            session['_password'] = request.form.get("password")
            session['_key'] = request.form.get("key")
            return redirect(url_for('decoded'))
    else:
        return render_template('decode.html')

#result of decoding process 
@app.route("/decoded",methods=['GET'])
def decoded():
    fileName = session.get('_imgname')
    password = session.get('_password')
    key = session.get('_key')
    
    text = steganography.decode(("uploads/"+fileName),password,key)
    os.remove(("uploads/"+fileName))
    return render_template('decoded.html',decoded_phrase=text)

#process of encryption
@app.route('/encrypt',methods=["GET","POST"])
def encrypt():
    if request.method == "POST":  
        text = request.form.get('text')
        if text is None or text.strip() == "":
            return render_template('error.html', error = "You haven`t written the text")
        else:
            session['_text'] = request.form.get("text")
            return redirect(url_for("encrypted"))    
    else:
        return render_template('encrypt.html')
      
#result of encryption process
@app.route('/encrypted',methods=['GET'])
def encrypted():
    name = session.get('_imgname')
    text = session.get('_text')
    password, key = steganography.encryption(('uploads/'+str(name)),text,name,'encrypted/')
    return render_template('encrypted.html',ret_paswd=password, name=name, key=key)
#!===================== uncomment this for config mail
# @app.route('/email', methods=["POST"])
# def sendMail():
#     if request.method == 'POST':
#         name = session.get('_imgname')
#         email = request.form['email']
#         # File path
#         filename = 'uploads/'+ name
#                  #!add sender ""
#         msg = Message('Sending File', sender='', recipients=[email])
#         msg.body = 'Your encrypted image'
#         with app.open_resource(filename) as fp:
#             msg.attach(filename, 'application/octet-stream', fp.read())

#         mail.send(msg)
#         os.remove(filename)
#         return render_template('end.html', result ='Email sent successfully')
# !=====================

if __name__ == '__main__':
    app.run(debug=True)
    # app.run()

