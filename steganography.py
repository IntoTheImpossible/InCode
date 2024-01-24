import os
from PIL import Image,ImageDraw
import random
import cryptography.fernet as fernet

def check(imagePath):
    if not os.path.exists(imagePath):
        return "File not found"
    if os.path.split(imagePath)[1].split('.')[1] != 'png':
        return "File format not supported"
    return True


def encryption(imagePath, word, imageName,encryptedDir):
    if check(imagePath) != True:
        return check(imagePath)
    
    img = Image.open(imagePath)
    draw = ImageDraw.Draw(img)
    width,height = img.size
    max_pixels = width*height
    
    # list of keys 
    encryptionKeys = [] 

    # generate key
    hashEncryptionKey = fernet.Fernet.generate_key()
    # create object for encrypt
    f=fernet.Fernet(hashEncryptionKey)
    # encrypt text
    token = f.encrypt(word.encode("utf-8")) 
    word = token.decode("utf-8") 



    #if size of hashed text is biger than quantity of pixels exist 
    if(len(word)>max_pixels):
        return "What with size?"

    #transfrom to list of char in ASCII from words
    bin_word = []
    for char in word:
        temp = ord(char)
        bin_word.append(temp)
 
    def rand():#generate positions of pixel on the map
  
        for ordChar in bin_word:
      
            min = ordChar - 20
            max = ordChar + 20
            def generator():
                x = random.randint(0,width-1)
                y = random.randint(0,height-1)

                if ((x,y) in encryptionKeys):
                    generator()
                else:
                    rgb = img.getpixel((x,y))
                    result = None

                    for index,color in enumerate(rgb):#check how close to char from text
                        if(min  <= color <= max):
                            result = (x,y, index)###* result = ((x,y), index)
                            break
                        
                    if(result != None): #add key if passed
                        encryptionKeys.append(result)
                        data = list(rgb)
                        data[result[2]] = ordChar
                        data = tuple(data)
                        draw.point((x,y),data)

                    else:#recursion
                        generator()    
            generator()
    
    try:
        rand()
    except RecursionError:
        return "Something is wrong. Try again"
    # save encrypted image
    img.save(encryptedDir+imageName)


    #! remove original image from folder 'uploads'
    os.remove(imagePath)
  

    return Key.keyTransformation(Key.encryptor(encryptionKeys)), hashEncryptionKey.decode("utf-8")


def decode(imagePath, stringOfKeys, key):
    if check(imagePath) != True:
        return check(imagePath)
    

    decodeKeys = Key.decryptor(Key.textTransformation(stringOfKeys))
    decodedPhrase = []
    img = Image.open(imagePath)

    for xyz in decodeKeys:
        x = xyz[0]
        y = xyz[1]
        z = xyz[2]
        rgb = img.getpixel((x,y))
        decodedPhrase.append(chr(rgb[z]))
    
    decodedPhrase="".join(decodedPhrase)
    
    # create object for encrypt
    f=fernet.Fernet(key.encode("utf-8"))
    # decrypt text
    decodedPhrase = f.decrypt(decodedPhrase.encode("utf-8")).decode("utf-8")
    # decode text


    return decodedPhrase

class Key():
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
                if 0 <= j < 9:
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