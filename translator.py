def translator(phrase):
    newPhrase = ""
    for letter in phrase:
        if letter in "AEIOUaeiou" and letter.isupper():
            letter = "G"
        elif letter in "AEIOUaeiou" and letter.islower():
            letter = "g"
        newPhrase += letter
    return(newPhrase)


print(translator(input("Enter a phrase to translate into G language: ")))
