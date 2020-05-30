import speech_recognition as sr
import pandas as pd
from googletrans import Translator 
import xlsxwriter


workbook = xlsxwriter.Workbook('cardiohindi.xlsx')
sheet1 = workbook.add_worksheet()
i=1


cell_format = workbook.add_format({'align': 'center',
                                   'valign': 'vcenter',
                                   'border': 1})
sheet1.write('F1', 'निदान')
sheet1.merge_range('G1:I1', "प्रमुख अभिव्यक्ति", cell_format)
sheet1.merge_range('J1:K1', "मामूली अभिव्यक्ति", cell_format)
sheet1.merge_range('L1:M1', "सहायक साक्ष्य", cell_format)
sheet1.merge_range('N1:P1', "उपचार", cell_format)
sheet1.merge_range('Q1:S1', "जटिलताओं", cell_format)
# add_sheet is used to create sheet. 

sheet1.write('A1', 'नाम') 
sheet1.write('B1', 'उम्र') 
sheet1.write('C1', 'पिता का नाम') 
sheet1.write('D1', 'जिला') 
sheet1.write('E1', 'आधार नंबर')

sheet1.write('G2', 'पॉलीआर्थराइटिस') 
sheet1.write('H2', 'मोनोआर्थराइटिस') 
sheet1.write('I2', 'कार्डाइटिस') 
sheet1.write('J2', 'बुखार') 
sheet1.write('K2', 'बढ़ी हुई डब्ल्यूबीसी')
sheet1.write('L2', 'उठाया एंटीनास') 
sheet1.write('M2', 'उठाया aso titre') 
sheet1.write('N2', 'ऐस अवरोधक') 
sheet1.write('O2', 'Diuretics') 
sheet1.write('P2', 'डिडॉक्स')
sheet1.write('Q2', 'फिब्रिलेशन') 
sheet1.write('R2', 'आमवाती बुखार') 
sheet1.write('S2', 'थ्रोम्बोएम्बोलिज्म')
sheet1.set_column(1, 18, 15)
i=1
j=2
while j<100:
	print("रोगी संख्या",j-1)
	while i<100:
		r = sr.Recognizer()
		#r# .dynamic_energy_thereshold=False
		with sr.Microphone() as source:
			print("कृपया डेटा को हिंदी में कहें")
			#r.adjust_for_ambient_noise(source, duration=1)
			audio = r.listen(source,phrase_time_limit=3)
		print("fetching")
		try:
			x=r.recognize_google(audio,None,"hi").lower()
			y = x.split(' ')[0]
			z = ''
			if len(x.split()) > 2:
				z = x.split(' ')[1]
			q = ''
			if len(x.split()) > 1:
				q = x.split(' ')[1]
			print(x)
			if y == 'नाम':
				print(x.split(' ')[1])
				name=x.split(' ', 1)[1]
				sheet1.write(j, 0, name.capitalize())
			elif y == 'उम्र':
				print(x.split(' ')[1])
				age = x.split(' ')[1]
				sheet1.write(j, 1, age)
			elif y == 'पिता':
				print(x.split(' ')[3])
				fathername = x.split(' ', 3)[3]
				sheet1.write(j, 2, fathername.capitalize()) 
			elif y == 'जिला':
				print(x.split(' ')[1])
				district = x.split(' ')[1]
				sheet1.write(j, 3, district.capitalize()) 
			elif y == 'आधार':
				print(x.split(' ')[2])
				aadhar = x.split(' ')[1]
				sheet1.write(j, 4, aadhar)
			elif y == 'निदान':
				diagnosis = x.split(' ', 1)[1]
				sheet1.write(j, 5, diagnosis.capitalize())
			elif y == 'पॉलीआर्थराइटिस':
				print(x.split(' ')[1])
				polyarthritis = x.split(' ')[1]
				sheet1.write(j, 6, polyarthritis)
			elif y == 'मोनोआर्थराइटिस':
				print(x.split(' ')[2])
				monoarthritis = x.split(' ')[2]
				sheet1.write(j, 7, monoarthritis.capitalize()) 
			elif y == 'कारडाइटिस':
				print(x.split(' ')[1])
				carditis = x.split(' ')[1]
				sheet1.write(j, 8, carditis.capitalize()) 
			elif y == 'बुखार':
				print(x.split(' ')[1])
				fever = x.split(' ')[1]
				sheet1.write(j, 9, fever)
			elif z == 'हुई':
				wbc = x.split(' ')[2]
				sheet1.write(j, 10, wbc.capitalize())
			elif z == 'antidnase':
				print(x.split(' ')[2])
				antidnase = x.split(' ', 2)[2]
				sheet1.write(j, 11, antidnase.capitalize()) 
			elif z == 'aso':
				print(x.split(' ')[3])
				aso = x.split(' ')[3]
				sheet1.write(j, 12, aso.capitalize()) 
			elif y == 'ace':
				print(x.split(' ')[2])
				ace = x.split(' ')[2]
				sheet1.write(j, 13, ace)
			elif y == 'diuretics':
				diuretics = x.split(' ')[1]
				sheet1.write(j, 14, diuretics.capitalize())
			elif y == 'digox':
				print(x.split(' ')[1])
				digox = x.split(' ')[1]
				sheet1.write(j, 15, digox.capitalize()) 
			elif y == 'फिब्रिलेशन':
				print(x.split(' ')[1])
				fibrillation = x.split(' ')[1]
				sheet1.write(j, 16, fibrillation.capitalize()) 
			elif y == 'आमवाती':
				print(x.split(' ')[2])
				rheumatic = x.split(' ')[2]
				sheet1.write(j, 17, rheumatic)
			elif y == 'थ्रोम्बोएम्बोलिज्म':
				thromboemblism = x.split(' ')[1]
				sheet1.write(j, 18, thromboemblism.capitalize())

			elif y == 'फिनिश्ड' or y == 'एग्जिट':
				break;

		except sr.UnknownValueError:
			print("Could not understand audio")
			i=i-1
			continue
		except sr.RequestError as e:
			print("Could not request results from Speech Recognition service; {0}".format(e))
			i=i-1
			continue

		if y == 'फिनिश्ड' or y == 'एग्जिट':
			break
		i=i+1
		
		print("data saved")
	j=j+1
	if y == 'एग्जिट':
		break

workbook.close()

