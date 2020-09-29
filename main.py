import PyQt5.QtWidgets as qt
import sys
from connect_db import db_connect
from query import make_query

# подключение к базе данных
link = db_connect("database.db")


def foo():
    # print("foo()")
    pass


def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False


def get_number_of_columns():
    res = 5  # количество полей в таблице (пока так)
    return res


def get_number_of_rows():
    res = make_query(link, "SELECT COUNT(*) FROM game")
    return res[0][0]  # возвращает количество записей в базе


def fill_table():
    table.clear()  # очистка таблицы
    col_num = get_number_of_columns()
    row_num = get_number_of_rows()
    table.setColumnCount(col_num)  # количество столбцов
    column_widths = [35, 130, 400, 140, 80]  # значания для ширины столбцов
    for i in range(len(column_widths)):
        table.setColumnWidth(i, column_widths[i])  # установка ширины столбцов
    table.setRowCount(row_num)  # количество строк
    for i in range(row_num):
        table.setRowHeight(i, 100)  # установка высоты строк

    table.setHorizontalHeaderLabels(["ID", "Название", "Описание", "Категория", "Цена"])  # заголовки столбцов

    # table.horizontalHeaderItem(0).setToolTip("column 1")
    # table.horizontalHeaderItem(1).setToolTip("column 2")
    # table.horizontalHeaderItem(2).setToolTip("column 3")

    for i in range(row_num):
        for j in range(col_num):
            res = make_query(link, "SELECT * FROM game")
            table.setItem(i, j, qt.QTableWidgetItem(str(res[i][j]) if j != 4 else str(float(res[i][j])) + " руб."))


def add_row():
    add_win = qt.QDialog(widget)
    add_win.setModal(True)
    add_win.resize(400, 100)
    add_win.setWindowTitle("Добавление")

    lbl1 = qt.QLabel("Название:")
    inp1 = qt.QLineEdit()
    lbl2 = qt.QLabel("Описание:")
    inp2 = qt.QTextEdit()
    lbl3 = qt.QLabel("Категория:")
    inp3 = qt.QLineEdit()
    lbl4 = qt.QLabel("Цена:")
    inp4 = qt.QLineEdit()
    btn = qt.QPushButton("Добавить")

    grid2 = qt.QVBoxLayout(add_win)
    grid2.addWidget(lbl1, 0)
    grid2.addWidget(inp1, 1)
    grid2.addWidget(lbl2, 2)
    grid2.addWidget(inp2, 3)
    grid2.addWidget(lbl3, 4)
    grid2.addWidget(inp3, 5)
    grid2.addWidget(lbl4, 6)
    grid2.addWidget(inp4, 7)
    grid2.addWidget(btn, 8)

    def add_to_db():
        err_msg_list = []  # список для хранения текстов об ошибках
        # проверка введенных пользователем полей
        if inp1.text() == "":
            err_msg_list.append("Необходимо ввести название!<br>")
        if inp2.toPlainText() == "":
            err_msg_list.append("Необходимо ввести описание!<br>")
        if inp3.text() == "":
            err_msg_list.append("Необходимо выбрать категорию!<br>")
        if inp4.text() == "":
            err_msg_list.append("Необходимо указать цену!<br>")
        elif not is_float(inp4.text()):
            err_msg_list.append("Цена должна быть числовой!<br>")
        # Если были ошибки при вводе -> оповещение пользователя об этом
        if len(err_msg_list) != 0:
            err_msg = qt.QErrorMessage()
            err_msg.setWindowTitle("Ошибка!")
            err_msg.setModal(True)
            err_msg.showMessage("".join(err_msg_list))
            err_msg.exec_()
        else:
            make_query(link,
                       "INSERT INTO game (game_name, description, category, price) values('{}', '{}', '{}', '{}')".format(
                           inp1.text(), inp2.toPlainText(), inp3.text(), inp4.text()))
            fill_table()
            add_win.close()

    btn.clicked.connect(add_to_db)  # привязка функции к кнопке "добавить"

    add_win.exec_()


def edit():
    try:
        edit_id = table.selectedItems()[0].text()  # сохранение id товара выбранной строки
    except IndexError:
        err_msg = qt.QErrorMessage()
        err_msg.setWindowTitle("Ошибка!")
        err_msg.setModal(True)
        err_msg.showMessage("Необходимо выбрать строку для редактирования!")
        err_msg.exec_()
    else:
        edit_win = qt.QDialog(widget)
        edit_win.setModal(True)
        edit_win.resize(400, 100)
        edit_win.setWindowTitle("Редактирование")

        lbl1 = qt.QLabel("Название:")
        inp1 = qt.QLineEdit()
        inp1.setText(table.selectedItems()[1].text())
        lbl2 = qt.QLabel("Описание:")
        inp2 = qt.QTextEdit()
        inp2.setText(table.selectedItems()[2].text())
        lbl3 = qt.QLabel("Категория:")
        inp3 = qt.QLineEdit()
        inp3.setText(table.selectedItems()[3].text())
        lbl4 = qt.QLabel("Цена:")
        inp4 = qt.QLineEdit()
        inp4.setText(table.selectedItems()[4].text()[:-5])  # обрезка " руб." в конце цены
        btn = qt.QPushButton("Сохранить")

        grid2 = qt.QVBoxLayout(edit_win)
        grid2.addWidget(lbl1, 0)
        grid2.addWidget(inp1, 1)
        grid2.addWidget(lbl2, 2)
        grid2.addWidget(inp2, 3)
        grid2.addWidget(lbl3, 4)
        grid2.addWidget(inp3, 5)
        grid2.addWidget(lbl4, 6)
        grid2.addWidget(inp4, 7)
        grid2.addWidget(btn, 8)

        def edit_in_db():
            err_msg_list = []  # список для хранения текстов об ошибках
            # проверка исправленных пользователем полей
            if inp1.text() == "":
                err_msg_list.append("Необходимо ввести название!<br>")
            if inp2.toPlainText() == "":
                err_msg_list.append("Необходимо ввести описание!<br>")
            if inp3.text() == "":
                err_msg_list.append("Необходимо выбрать категорию!<br>")
            if inp4.text() == "":
                err_msg_list.append("Необходимо указать цену!<br>")
            elif not is_float(inp4.text()):
                err_msg_list.append("Цена должна быть числовой!<br>")
            # Если были ошибки при вводе => оповещение пользователя об этом
            if len(err_msg_list) != 0:
                err_msg = qt.QErrorMessage()
                err_msg.setWindowTitle("Ошибка!")
                err_msg.setModal(True)
                err_msg.showMessage("".join(err_msg_list))
                err_msg.exec_()
            else:
                make_query(link,
                           "UPDATE game SET game_name='{}', description='{}', category='{}', price='{}' WHERE id='{}'".format(
                               inp1.text(), inp2.toPlainText(), inp3.text(), inp4.text(), edit_id))
                fill_table()
                edit_win.close()

        btn.clicked.connect(edit_in_db)  # привязка функции к кнопке "сохранить"

        edit_win.exec_()


def delete():
    try:
        del_id = table.selectedItems()[0].text()  # сохранение id товара выбранной строки
    except IndexError:
        err_msg = qt.QErrorMessage()
        err_msg.setWindowTitle("Ошибка!")
        err_msg.setModal(True)
        err_msg.showMessage("Необходимо выбрать строку для удаления!")
        err_msg.exec_()
    else:
        del_win = qt.QMessageBox(widget)  # создается окно подтверждения
        del_win.setModal(True)
        del_win.setStandardButtons(qt.QMessageBox.Yes | qt.QMessageBox.Cancel)  # 2 стандартные кнопки
        del_win.setText("Вы действительно хотите удалить выбранную запись?\n\nYes - подтвердить\nCancel - отменить")
        del_win.setWindowTitle("Удаление")

        choise = del_win.exec_()  # сохранение выбора пользователя

        if choise == qt.QMessageBox.Yes:  # при подтверждении удаление записи
            make_query(link, "DELETE FROM game WHERE id='{}'".format(del_id))
            fill_table()  # заполнение таблицы заново


if __name__ == "__main__":
    app = qt.QApplication([])
    widget = qt.QWidget()
    widget.setWindowTitle("Лаба АСОИУ")
    widget.resize(830, 500)  # задать размер окна

    table = qt.QTableWidget()  # таблица
    # table.setMaximumSize(400, 200)  # задать максимальный размер самой таблицы
    table.setEditTriggers(qt.QAbstractItemView.NoEditTriggers)  # запрет на редактирование данных
    table.setSelectionBehavior(qt.QAbstractItemView.SelectRows)  # выделят вместо одной ячейки всю строку
    table.verticalHeader().sectionClicked.connect(foo)  # отлов клика по вертикальному хэдеру (номер строки)
    table.clicked.connect(foo)  # отлов клика строки по ячейке таблицы

    fill_table()
    # создание кнопок пот таблицей и привязывание функций для отклика
    add_btn = qt.QPushButton("Добавить")
    add_btn.clicked.connect(add_row)
    edit_btn = qt.QPushButton("Редактировать")
    edit_btn.clicked.connect(edit)
    del_btn = qt.QPushButton("Удалить")
    del_btn.clicked.connect(delete)

    # расположение элементов по сетке
    grid = qt.QGridLayout(widget)
    grid.addWidget(table, 0, 0, 1, 0)
    grid.addWidget(add_btn, 1, 0)
    grid.addWidget(edit_btn, 1, 1)
    grid.addWidget(del_btn, 1, 2)

    widget.show()

    sys.exit(app.exec_())
