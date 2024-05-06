import openpyxl

# 打开Excel文件
workbook = openpyxl.load_workbook('src/download/STATEMENT.xlsx')

# 选择要读取的工作表
sheet = workbook.active

# 读取单元格数据示例
cell_value = sheet['A1'].value
print("Value in cell A1:", cell_value)

# 遍历行示例
for row in sheet.iter_rows(values_only=True):
    print(row)

# 关闭Excel文件
workbook.close()