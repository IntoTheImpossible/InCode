from flask import Flask, request, render_template, redirect, send_file, url_for,session
#TODO uncommnet for mail 
# from flask_mail import Mail, Message
# import webbrowser as web_br
from PIL import Image
from steganography import Steganography
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
#TODO uncomment this for config mail
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

#download image
@app.route('/download/<path:filename>', methods=['POST'])
def download(filename):
    if request.method == 'POST' and session.get('_imgname')==filename:
        return send_file('encrypted/'+filename, as_attachment=True, download_name=filename)
    else:
        return render_template('error.html', error = 'No file for downloading' )
#download keys
@app.route('/download-keys/<path:filename>', methods=['POST'])
def download_keys(filename):
    if request.method == 'POST' and session.get('_imgname')==filename:
        filename=filename.replace(".png", "")+".txt"
        return send_file('textfiles/'+filename, as_attachment=True, download_name=filename)
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
    # Process the file upload
    file.save('uploads/' + file.filename)
    #check file type
    if os.path.splitext(file.filename)[1] != ".png":
        os.remove('uploads/' + file.filename)
        return render_template('error.html', error = 'Invalid file format')
    #check file size
    if Image.open('uploads/' + file.filename).size[0] <= 1000 or Image.open('uploads/' + file.filename).size[1] <= 1000:
        return render_template('error.html', error = 'Image size must be more than 1000x1000')
    #set name of file to session
    session['_imgname'] = file.filename
    # redirects from radiobuttons
    if process == "encr":
        return redirect(url_for("encrypt"))
    if process == "dec":
        return redirect(url_for("decode"))

#process of decoding
@app.route("/decode",methods=["GET","POST"])
def decode():
    if request.method == 'POST' and session.get('_imgname') is not None:
        key = request.form.get('key')
        userPassword = request.form.get('password')
        if key is None or key.strip() == "":
            return render_template('error.html', error = "Some problem with your key")
        elif userPassword is None or userPassword.strip() == "":
            return render_template('error.html', error =  "Some problem with your password")
        else:
            session['_password'] = request.form.get("password")
            session['_key'] = request.form.get("key")
            return redirect(url_for('decoded'))
    else:
        if session.get('_imgname') is None:
            return render_template('error.html', error = "You haven`t uploaded the image")
        return render_template('decode.html')

#result of decoding process 
@app.route("/decoded",methods=['GET'])
def decoded():
    if session.get('_imgname') is None:
        return render_template('error.html', error = "You haven`t uploaded the image")
    fileName = session.get('_imgname')
    userPassword = session.get('_password')
    userKey = session.get('_key')

    try:
        userText = Steganography.decode(("uploads/"+fileName),stringOfKeys=userKey,password=userPassword)
    except:
        return render_template('error.html', error = "Something is wrong with your key or password. Try again")
    # remove uploaded file
    os.remove(("uploads/"+fileName))
    return render_template('decoded.html',decoded_phrase=userText)

#process of encryption
@app.route('/encrypt',methods=["GET","POST"])
def encrypt():
    if request.method == "POST" and session.get('_imgname') is not None:  
        userText = request.form.get('text')
        userPassword = request.form.get('password')
        if userText is None or userText.strip() == "":
            return render_template('error.html', error = "You haven`t written the text")
        elif userPassword is None or userPassword.strip() == "":
            return render_template('error.html', error = "You haven`t written the password")
        else:
            session['_text'] = request.form.get("text")
            session['_password'] = request.form.get("password")
            return redirect(url_for("encrypted"))    
    else:
        if session.get('_imgname') is None:
            return render_template('error.html', error = "You haven`t uploaded the image")
        return render_template('encrypt.html')
      
#result of encryption process
@app.route('/encrypted',methods=['GET'])
def encrypted():
    if session.get('_imgname') is None:
        return render_template('error.html', error = "You haven`t uploaded the image")
    userPassword = session.get('_password')
    userText = session.get('_text')
    imageName = session.get('_imgname')
    try:
        userPassword = Steganography.encryption(('uploads/'+str(imageName)),userText,'encrypted/',userPassword)
    except:
        return render_template('error.html', error = "Something is wrong with your image. Try again with another image")
    
        
    return render_template('encrypted.html',ret_paswd=userPassword, name=imageName)
#TODO uncomment this for config mail
#!===================== uncomment this for config mail
# @app.route('/email', methods=["POST"])
# def sendMail():
#     if request.method == 'POST' and session.get('_imgname') is not None:
#         imageName = session.get('_imgname')
#         email = request.form['email']
#         # File path
#         filename = 'uploads/'+ imageName
#                  #!add sender ""
#         msg = Message('Sending File', sender='', recipients=[email])
#         msg.body = 'Your encrypted image'
#         with app.open_resource(filename) as fp:
#             msg.attach(filename, 'application/octet-stream', fp.read())

#         mail.send(msg)
#         # remove file after sending
#         # os.remove(filename)
#         return web_br.open_new_tab('end.html', result ='Email sent successfully')
# !=====================

if __name__ == '__main__':
    app.run()

