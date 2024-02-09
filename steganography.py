import os
from PIL import Image,ImageDraw
import random
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from base64 import urlsafe_b64encode, urlsafe_b64decode

class Steganography:

    def check(imagePath):
        "Check does file exist"
        if not os.path.exists(imagePath):
            return "File not found"
        return True

    def encryption(imagePath,phrase,encryptedDir, password):
        """ encryption function takes an image, a phrase, and a password and returns an encrypted image and a key"""
        # check does file exist
        if Steganography.check(imagePath) != True:
            return Steganography.check(imagePath)
        #open image and get data, create object Image
        img = Image.open(imagePath)
        draw = ImageDraw.Draw(img)
        width,height = img.size
        max_pixels = width*height
        # list of keys 
        encryptionKeys = [] 

        #encode hash
        phrase = Hash.encrypt(phrase, password)
        #if size of hashed text is biger than quantity of pixels exist 
        if(len(phrase)>max_pixels):
            return "sizeError"

        #transfrom to list of char in ASCII from words
        bin_word = []
        for char in phrase:
            temp = ord(char)
            bin_word.append(temp)
    
        def positionGenerator():
            """generate random coordinates and check how close to char from text. A key is added if passed"""
            for ordChar in bin_word:
                #accuracy of color
                min = ordChar - 25
                max = ordChar + 25

                def generator():

                    #generate random coordinates
                    x = random.randint(0,width-1)
                    y = random.randint(0,height-1)

                    if((x,y) not in encryptionKeys):


                        
                        rgb = img.getpixel((x,y))
                        
                        for index,color in enumerate(rgb):


                            if (min <= color <= max) and index != None:
                                encryptionKeys.append((x,y,index)) ###* result = ((x,y), index)
                                data = list(rgb)
                                data[0] = ordChar
                                data = tuple(data)
                                draw.point((x,y),data)
                            else:
                                generator()
                            break
                                    
                generator()
        positionGenerator()
        # save encrypted image
        img.save(encryptedDir+img.filename.split('/')[1])
        #remove original image from uploads
        os.remove(imagePath)
        #Encrypt key by KeyMixer class
        encryptedKeys = KeyMixer.keyTransformation(KeyMixer.encryptor(encryptionKeys))
        #save keys amd password to text file
        with open(f'textfiles/{img.filename.split("/")[1].replace(".png", "")}.txt', 'w') as file:
            file.write('Keys: '+str(encryptedKeys))
            file.write('\n'*4)
            file.write('Password: '+password)
        return str(encryptedKeys)


    def decode(imagePath, stringOfKeys, password):
        """ decode function takes an image, a key, and a password and returns a decoded phrase"""
        if Steganography.check(imagePath) != True:
            return Steganography.check(imagePath)
        
        #decode key by KeyMixer class
        decodeKeys = KeyMixer.decryptor(KeyMixer.textTransformation(stringOfKeys))

        decodedPhrase = []

        #open image and get data, create object Image
        img = Image.open(imagePath)

        #decode phrase by keys
        for xyz in decodeKeys:
            x = xyz[0]
            y = xyz[1]
            z = xyz[2]
            rgb = img.getpixel((x,y))
            decodedPhrase.append(chr(rgb[z]))

        #convert list to string
        decodedPhrase="".join(decodedPhrase)
        decodedPhrase=str(decodedPhrase)
        #Tdecode hash
        decodedPhrase = Hash.decrypt(decodedPhrase, password)

        return decodedPhrase
#class for mixing keys
class KeyMixer():
    """KeyMixer class for encrypting and decrypting keys and transforming them to strings and vice versa"""
        #encryptor function takes a key and encrypts it by applying a series of transformations
    def encryptor(key):
        """
        Encrypts the given key by applying a series of transformations.

        Parameters:
        key (list of tuples): The key to be encrypted.

        Returns:
        list of tuples: The encrypted key.
        """
        endedKey= []
        for i in range(len(key)):
            timelist = []
            for j in key[i]:
                
                if 0<=j+5<10:
                    j+=5
                    timelist.append(j)
                    
                elif 10<=j+10<500:
                    j+=10
                    timelist.append(j)
                elif 500<=j+15<1000:
                    j+=15
                    timelist.append(j)
                elif 1000<=j+20<1500:
                    j+=20
                    timelist.append(j)
                elif 1500<=j+25<2000:
                    j+=25
                    timelist.append(j)
                elif 2000<=j+30<2500:
                    j+=30
                    timelist.append(j)
                elif 2500<=j+35<3000:    
                    j+=35
                    timelist.append(j)
                elif 3000<=j+40<3500:
                    j+=40
                    timelist.append(j)
                elif 3500<=j+45<4000:
                    j+=45
                    timelist.append(j)
                elif 4000<=j+50<4500:
                    j+=50
                    timelist.append(j)
                elif 4500<=j+55<5000:    
                    j+=55
                    timelist.append(j)
                elif 5000<=j+60<5500:
                    j+=60
                    timelist.append(j)
                elif 5500<=j+65<6000:
                    j+=65
                    timelist.append(j)
                elif 6000<=j+70<6500:
                    j+=70
                    timelist.append(j)
                elif 6500<=j+75<7000:
                    j+=75
                    timelist.append(j)
                elif 7000<=j+80<8000:
                    j+=80
                    timelist.append(j)
                elif 8000<=j+85<9000:
                    j+=85
                    timelist.append(j)
                elif 9000<=j+90<10000:
                    j+=90
                    timelist.append(j)
                elif 10000<=j+95:
                    j+=100
                    timelist.append(j)
            endedKey.append(tuple(timelist))
        return endedKey
    #decryptor function takes an encrypted key and decrypts it by reversing the applied transformations
    def decryptor(encrypted_key):
        """
        Decrypts the given encrypted key by reversing the applied transformations.

        Parameters:
        encrypted_key (list of tuples): The encrypted key to be decrypted.

        Returns:
        list of tuples: The decrypted key.
        """
        original_key = []
        for i in range(len(encrypted_key)):
            timelist = []
            for j in encrypted_key[i]:
                if 0 <= j < 10:
                    j -= 5
                    timelist.append(j)
                elif 10 <= j < 500:
                    j -= 10
                    timelist.append(j)
                elif 500 <= j < 1000:
                    j -= 15
                    timelist.append(j)
                elif 1000 <= j < 1500:
                    j -= 20
                    timelist.append(j)
                elif 1500 <= j < 2000:
                    j -= 25
                    timelist.append(j)
                elif 2000 <= j < 2500:
                    j -= 30
                    timelist.append(j)
                elif 2500 <= j < 3000:
                    j -= 35
                    timelist.append(j)
                elif 3000 <= j < 3500:
                    j -= 40
                    timelist.append(j)
                elif 3500 <= j < 4000:
                    j -= 45
                    timelist.append(j)
                elif 4000 <= j < 4500:
                    j -= 50
                    timelist.append(j)
                elif 4500 <= j < 5000:
                    j -= 55
                    timelist.append(j)
                elif 5000 <= j < 5500:
                    j -= 60
                    timelist.append(j)
                elif 5500 <= j < 6000:
                    j -= 65
                    timelist.append(j)
                elif 6000 <= j < 6500:
                    j -= 70
                    timelist.append(j)
                elif 6500 <= j < 7000:
                    j -= 75
                    timelist.append(j)
                elif 7000 <= j < 8000:
                    j -= 80
                    timelist.append(j)
                elif 8000 <= j < 9000:
                    j -= 85
                    timelist.append(j)
                elif 9000 <= j < 10000:
                    j -= 90
                    timelist.append(j)
                elif 10000 <= j:
                    j -= 100
                    timelist.append(j)
            original_key.append(tuple(timelist))
        return original_key
    #keyTransformation function takes a key and converts it to a string
    def keyTransformation(key):
        message = []
        for i in range(len(key)):
            for j in key[i]:            
                message.extend(str(j))
                message.append('-')
        result = "".join(str(x) for x in message)
        return result
    #textTransformation function takes a string and converts it to a key
    def textTransformation(result):
        answer = []
        splited = result.split('-')
        splited.pop()  # Remove last element '' from list
        while len(splited) > 0:
            tempTuple =splited[0:3]
            for i in range(len(tempTuple)):
                tempTuple[i] = int(tempTuple[i])    
            answer.append(tuple(tempTuple))
            del splited[0:3]
        return answer
    
class Hash:
    """Hash class for hashing and verifying passwords"""
    def derive_key_and_iv(password, length=32):
        """Derive a secret key and an IV from a given password"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            #TODO add salt if needed
            salt=b'',  #! Empty salt
            iterations=100000,
            length=length * 2  # Double the length for both key and IV
        )
        key_iv = kdf.derive(password.encode())
        key, iv = key_iv[:length], key_iv[length:length+16]  # Assuming a 16-byte IV for AES
        return key, iv

    def encrypt(plaintext, password):
        """Encrypt plaintext using AES-256 CFB mode"""
        key, iv = Hash.derive_key_and_iv(password)
        cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(plaintext.encode()) + encryptor.finalize()
        return urlsafe_b64encode(iv + ciphertext).decode('utf-8')

    def decrypt(ciphertext:str, password):
        """Decrypt ciphertext using AES-256 CFB mode"""
    
        data = urlsafe_b64decode(ciphertext)
    
        iv = data[:16]  # Extract the IV (16 bytes)

        ciphertext = data[16:]
    
        key, _ = Hash.derive_key_and_iv(password)
        cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_text = decryptor.update(ciphertext) + decryptor.finalize()
        return decrypted_text.decode()
