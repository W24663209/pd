import openpyxl


def xlsx(path):
    # 打开Excel文件
    workbook = openpyxl.load_workbook(path)
    # 选择要读取的工作表
    sheet = workbook.active
    # 读取单元格数据示例
    # cell_value = sheet['A1'].value
    # print("Value in cell A1:", cell_value)
    # 遍历行示例
    index = 0
    rows = sheet.iter_rows(values_only=True)
    max_row = rows.gi_frame.f_locals['max_row']
    for row in rows:
        if index >= 17 and max_row-4 >= index:
            print(row)
        index += 1
    # 关闭Excel文件
    workbook.close()


if __name__ == '__main__':
    xlsx('../../src/download/STATEMENT.xlsx')