import pywt
import random
import csv
import os


dir_name = ['open', 'dondon']
dir_i = 1
dir_path = 'C:\\Users\\NakagawaMasafumi\\Documents\\data\\'+dir_name[dir_i]+'\\'
out_dir_path = 'C:\\Users\\NakagawaMasafumi\\Documents\\data\\'+dir_name[dir_i]+'_wavelet\\'
files = os.listdir(dir_path)

for file in files:
    for fi in range(0,36):
        f = open(dir_path+file, 'r')

        acc_list = [[], [], []]
        pos = random.randint(0,175000)
        index = 0
        for line in f:
            if index >= pos + 5000:
                break
            if index >= pos:
                #print (line)
                values = line.strip().split(',')
                acc_list[0].append(int(values[1]))
                acc_list[1].append(int(values[2]))
                acc_list[2].append(int(values[3]))

            index = index + 1

        f.close()

        #print(acc_list)
        f = open(out_dir_path+file[0:len(dir_name[dir_i])+1]+'_'+str(fi)+'.csv', 'w')
        csvWriter = csv.writer(f)
        for i in range(0,3):
            coeffs = pywt.wavedec(acc_list[i], 'db1', level=10)
            csvWriter.writerow(coeffs[0])

        f.close()

"""f = open(dir_path+'dondon1.csv', 'r')

acc_list = [[], [], []]
pos = 0#random.randint(0,175000)
index = 0
for line in f:
    if index >= pos + 10:
        break
    if index >= pos:
        #print (line)
        values = line.strip().split(',')
        acc_list[0].append(int(values[1]))
        acc_list[1].append(int(values[2]))
        acc_list[2].append(int(values[3]))

    index = index + 1

f.close()"""

#coeffs = pywt.wavedec([5,6,11,12,8,9], 'db1', level=1)
#print(coeffs[0])
#cA2, cD5, cD4, cD3, cD2, cD1 = coeffs
#print (cA2)
#[ 2.12132034  4.94974747  7.77817459]
#print (cD1)
#[-0.70710678 -0.70710678 -0.70710678]
#print (cD5)
