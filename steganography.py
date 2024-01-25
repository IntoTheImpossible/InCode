import os
from PIL import Image,ImageDraw
import random
from hash import Hash


def check(imagePath):
    "Check does file exist"
    if not os.path.exists(imagePath):
        return "File not found"
    return True


def encryption(imagePath,phrase,encryptedDir, password):
    """ encryption function takes an image, a phrase, and a password and returns an encrypted image and a key"""
    # check does file exist
    if check(imagePath) != True:
        return check(imagePath)
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
            max = ordChar + 20
            def generator():

                #generate random coordinates
                x = random.randint(0,width-1)
                y = random.randint(0,height-1)

                if((x,y) not in encryptionKeys):
                    rgb = img.getpixel((x,y))
                    
                    for index,color in enumerate(rgb):
                        if(min <= color <= max):
                            encryptionKeys.append((x,y,index)) ###* result = ((x,y), index)
                            data = list(rgb)
                            data[0] = ordChar
                            data = tuple(data)
                            draw.point((x,y),data)
                        else:
                            generator()

    positionGenerator()
    # save encrypted image
    img.save(encryptedDir+img.filename.split('/')[1])
    #remove original image from uploads
    os.remove(imagePath)
    #Encrypt key by Key class
    encryptedKeys = Key.keyTransformation(Key.encryptor(encryptionKeys))
    #save keys amd password to text file
    with open(f'textfiles/{img.filename.split('/')[1].strip('.png')}.txt', 'w') as file:
        file.write('Key: '+str(encryptedKeys))
        file.write('\n'*4)
        file.write('Password: '+password)
    return encryptedKeys


def decode(imagePath, stringOfKeys, password):
    """ decode function takes an image, a key, and a password and returns a decoded phrase"""
    if check(imagePath) != True:
        return check(imagePath)
    
    #decode key by Key class
    decodeKeys = Key.decryptor(Key.textTransformation(stringOfKeys))
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
class Key():
    """Key class for encrypting and decrypting keys and transforming them to strings and vice versa"""
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
    
