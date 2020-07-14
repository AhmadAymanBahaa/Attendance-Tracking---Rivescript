import xlsxwriter

workbook = xlsxwriter.Workbook('attendance.xlsx')
worksheet = workbook.add_worksheet()

def export(name,id):
    worksheet.write(0,0,name)
    worksheet.write(0,1,id)
    workbook.close()
