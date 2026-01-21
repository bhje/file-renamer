import os
import pandas as pd
from natsort import natsorted


def rename_images(csv_path, images_folder):
    csvfName = pd.read_csv(csv_path, usecols=[3, 4])

    print(len(csvfName))

    for index, row in csvfName.iterrows():
        name = row[0]+row[1]
        nameNoSpace = name.replace(" ", "")
        print(nameNoSpace)
        print(index)
        dir_list = os.listdir(images_folder)
        print(dir_list)
        sortedlist = natsorted(dir_list)
        print(sortedlist)
        if (sortedlist[0] == (str(index) + ".jpg")):
            os.rename("bilder/" + sortedlist[0],"renamedBilder/" + nameNoSpace + ".jpg")
        else:
            print("fucky wucky no worky")



    

csv_path = 'namn.csv'
images_folder = 'bilder'

try:
    rename_images(csv_path, images_folder)
except:
    print("Jippii jag älskar livet numera!")