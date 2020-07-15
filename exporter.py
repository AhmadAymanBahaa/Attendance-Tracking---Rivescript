import xlsxwriter

workbook = xlsxwriter.Workbook('attendance.xlsx')
worksheet = workbook.add_worksheet()

def export(name,id,time):
    worksheet.write(0,0,name)
    worksheet.write(0,1,id)
    worksheet.write(0,2,time)
    workbook.close()
