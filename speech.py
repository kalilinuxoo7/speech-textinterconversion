import speech_recognition as sr

import xlsxwriter


workbook = xlsxwriter.Workbook('cardioenglish.xlsx')
sheet1 = workbook.add_worksheet()


cell_format = workbook.add_format({'align': 'center',
                                   'valign': 'vcenter',
                                   'border': 1})
sheet1.write('F1', 'DIAGNOSIS')
sheet1.merge_range('G1:I1', "MAJOR MANIFESTATION", cell_format)
sheet1.merge_range('J1:K1', "MINOR MANIFESTATION", cell_format)
sheet1.merge_range('L1:M1', "SUPPORTIVE EVIDENCE", cell_format)
sheet1.merge_range('N1:P1', "TREATMENT", cell_format)
sheet1.merge_range('Q1:S1', "COMPLICATIONS", cell_format)
# add_sheet is used to create sheet. 

sheet1.write('A1', 'NAME') 
sheet1.write('B1', 'AGE') 
sheet1.write('C1', 'FATHER NAME') 
sheet1.write('D1', 'DISTRICT') 
sheet1.write('E1', 'AADHAR NUMBER')

sheet1.write('G2', 'Polyarthritis') 
sheet1.write('H2', 'Monoarthritis') 
sheet1.write('I2', 'Carditis') 
sheet1.write('J2', 'Fever') 
sheet1.write('K2', 'Increased WBC')
sheet1.write('L2', 'Raised Antidnase') 
sheet1.write('M2', 'Raised aso titre') 
sheet1.write('N2', 'Ace inhibitors') 
sheet1.write('O2', 'Diuretics') 
sheet1.write('P2', 'Digox')
sheet1.write('Q2', 'Fibrillation') 
sheet1.write('R2', 'Rheumatic Fever') 
sheet1.write('S2', 'Thromboembolism')
sheet1.set_column(1, 18, 15)
i=1
j=2
while j<100:
	print("Details of patient number",j-1)
	while i<100:
		r = sr.Recognizer()
		#r# .dynamic_energy_thereshold=False
		with sr.Microphone() as source:
			print("Say something!")
			#r.adjust_for_ambient_noise(source, duration=1)
			audio = r.listen(source,phrase_time_limit=3)
		print("fetching")
		try:
			x=r.recognize_google(audio).lower()
			y = x.split(' ')[0]
			z = ''
			if len(x.split()) > 2:
				z = x.split(' ')[1]
			q = ''
			if len(x.split()) > 1:
				q = x.split(' ')[1]
			print(x)
			if y == 'name':
				print(x.split(' ')[1])
				name=x.split(' ', 1)[1]
				sheet1.write(j, 0, name.capitalize())
			elif y == 'age':
				print(x.split(' ')[1])
				age = x.split(' ')[1]
				sheet1.write(j, 1, age)
			elif y == 'father':
				print(x.split(' ')[2])
				fathername = x.split(' ', 2)[2]
				sheet1.write(j, 2, fathername.capitalize()) 
			elif y == 'district':
				print(x.split(' ')[1])
				district = x.split(' ')[1]
				sheet1.write(j, 3, district.capitalize()) 
			elif y == 'aadhar':
				print(x.split(' ')[2])
				aadhar = x.split(' ')[1]
				sheet1.write(j, 4, aadhar)
			elif y == 'diagnosis':
				diagnosis = x.split(' ', 1)[1]
				sheet1.write(j, 5, diagnosis.capitalize())
			elif y == 'polyarthritis':
				print(x.split(' ')[1])
				polyarthritis = x.split(' ')[1]
				sheet1.write(j, 6, polyarthritis)
			elif q == 'arthritis':
				print(x.split(' ')[2])
				monoarthritis = x.split(' ')[2]
				sheet1.write(j, 7, monoarthritis.capitalize()) 
			elif y == 'carditis':
				print(x.split(' ')[1])
				carditis = x.split(' ')[1]
				sheet1.write(j, 8, carditis.capitalize()) 
			elif y == 'fever':
				print(x.split(' ')[1])
				fever = x.split(' ')[1]
				sheet1.write(j, 9, fever)
			elif z == 'wbc':
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
			elif y == 'fibrillation':
				print(x.split(' ')[1])
				fibrillation = x.split(' ')[1]
				sheet1.write(j, 16, fibrillation.capitalize()) 
			elif y == 'rheumatic':
				print(x.split(' ')[2])
				rheumatic = x.split(' ')[2]
				sheet1.write(j, 17, rheumatic)
			elif y == 'thromboembolism':
				thromboemblism = x.split(' ')[1]
				sheet1.write(j, 18, thromboemblism.capitalize())

			elif y == 'finished' or y == 'exit':
				break;

		except sr.UnknownValueError:
			print("Could not understand audio")
			i=i-1
			continue
		except sr.RequestError as e:
			print("Could not request results from Speech Recognition service; {0}".format(e))
			i=i-1
			continue

		if y == 'finished' or y == 'exit':
			break
		i=i+1
		
		print("data saved")
	j=j+1
	if y == 'exit':
		break

workbook.close()






