from tkinter import *
from tkinter import filedialog


class ListEntry:
    next = None
    prev = None
    rank = 0
    contents = 'dummy'


def ranklist(first_entry, save_flag, pathway, list_size):
    while True:
        instruc = input("Input Command:>")
        command = instruc.split()

        if command[0] == "save":
            new_file = Tk()
            new_file.filename = filedialog.asksaveasfile(mode='w', defaultextension=".txt")
            pathway = new_file.filename.name
            save_flag = True
            new_file.destroy()
            del new_file
            print("\n")
            print_list(first_entry, save_flag, pathway)
            print("\n")
            save_flag = False

        elif command[0] == "help":
            print('"add" <content> will add a new entry to the bottom of the list.\n'
                  '"insert <content> @ <ranknum> will add a new entry to a specified '
                  'location.\n'
                  '"remove" <content> OR "remove" <ranknum> will remove an entry at '
                  'the specified location.\n'
                  '"move" <content> @ <ranknum> OR "move" <ranknum> @ <ranknum2> '
                  'will move the entry to the specified location.\n'
                  '"save" outputs the current list to a txt file.\n'
                  '"openfile" allows you to open an existing properly formatted list '
                  'for further manipulation.\n'
                  '"quit" exits the application.\n')

        item = ""
        target_rank = 0
        if command[len(command) - 2] == "@":
            for i in range(1, len(command) - 2):
                if i == 1:
                    item = item + command[i]
                else:
                    item = item + " " + command[i]
                target_rank = command[len(command) - 1]
        else:
            for i in range(1, len(command)):
                if i == 1:
                    item = item + command[i]
                else:
                    item = item + " " + command[i]

        if command[0] == "add":
            if len(command) == 1:
                pass
            else:
                if list_size == 0:
                    first_entry = setup_list(item)
                else:
                    next_entry = ListEntry()
                    next_entry.rank = list_size + 1
                    next_entry.contents = item
                    add(first_entry, next_entry)
                    del next_entry
                list_size += 1
                print("\n")
                print_list(first_entry, save_flag, pathway)
                print("\n")

        elif command[0] == "insert":
            if len(command) < 3:
                pass
            else:
                if list_size == 0:
                    first_entry = setup_list(item)
                else:
                    this_entry = ListEntry()
                    this_entry.rank = int(target_rank)
                    this_entry.contents = item
                    rank_range = (list_size + 1) - int(target_rank)
                    if this_entry.rank == list_size + 1:
                        add(first_entry, this_entry)
                    elif (int(target_rank)) <= list_size + 1:
                        insert(first_entry, this_entry, rank_range)
                        first_entry = check_first(first_entry)
                list_size += 1
                print("\n")
                print_list(first_entry, save_flag, pathway)
                print("\n")

        elif command[0] == "remove":
            if list_size == 0:
                print("nothing found")
            else:
                target = item
                remove(first_entry, target, list_size)
                first_entry = check_first(first_entry)
                list_size -= 1
                print("\n")
                print_list(first_entry, save_flag, pathway)
                print("\n")

        elif command[0] == "move":
            if len(command) < 3:
                pass
            else:
                t_rank = int(target_rank)
                target_contents = item
                try:
                    target_contents = int(target_contents)
                except TypeError:
                    pass
                if t_rank <= list_size + 1:
                    move(first_entry, target_contents, t_rank)
                    first_entry = check_first(first_entry)
                    print("\n")
                    print_list(first_entry, save_flag, pathway)
                    print("\n")

        elif command[0] == "edit":
            if len(command) < 2:
                pass
            else:
                new_content = input("What would you like to change this entry to?\n")
                t_rank = int(target_rank)
                target_contents = item
                try:
                    target_contents = int(target_contents)
                except ValueError:
                    pass
                if t_rank <= list_size + 1:
                    edit(first_entry, target_contents, new_content)
                    first_entry = check_first(first_entry)
                    print("\n")
                    print_list(first_entry, save_flag, pathway)
                    print("\n")
        elif command[0] == "quit":
            first_entry = None
            return(first_entry)


def print_list(curr_entry, save_flag, pathway):
    if save_flag:
        file2write = open(pathway, "a+")
        if curr_entry.next is not None:
            file2write.write(str(curr_entry.rank) + ": " + curr_entry.contents + "\n")
        else:
            file2write.write(str(curr_entry.rank) + ": " + curr_entry.contents)
        file2write.close()
    print(str(curr_entry.rank) + ": " + curr_entry.contents)
    if curr_entry.next is not None:
        this_entry = curr_entry.next
        print_list(this_entry, save_flag, pathway)


def setup_list(content):
    first_entry = ListEntry()
    first_entry.prev = None
    first_entry.rank = 1
    first_entry.contents = content
    return first_entry


def add(curr_entry, new_entry):
    if curr_entry.next is not None:
        this_entry = curr_entry.next
        add(this_entry, new_entry)
    else:
        curr_entry.next = new_entry
        new_entry.prev = curr_entry


def remove(curr_entry, target, list_size):
    if (str(curr_entry.rank) != target) and (curr_entry.contents != target):
        this_entry = curr_entry.next
        remove(this_entry, target, list_size)
    else:
        rank_range = list_size - curr_entry.rank
        if curr_entry.prev is not None:
            if curr_entry.next is not None:
                curr_entry.prev.next = curr_entry.next
                curr_entry.next.prev = curr_entry.prev
                refactor(curr_entry.next, rank_range, 2)
            elif curr_entry.next is None:
                curr_entry.prev.next = None
        if curr_entry.rank == 1:
            curr_entry.next.prev = None
            refactor(curr_entry.next, rank_range, 2)
            curr_entry.rank = 0
        elif curr_entry.rank == list_size:
            curr_entry.prev.next = None


def insert(curr_entry, new_entry, rank_range):
    if curr_entry.rank != new_entry.rank:
        this_entry = curr_entry.next
        insert(this_entry, new_entry, rank_range)
    else:
        new_entry.next = curr_entry
        if curr_entry.prev is not None:
            new_entry.prev = curr_entry.prev
            curr_entry.prev.next = new_entry
        curr_entry.prev = new_entry
        refactor(curr_entry, rank_range, 0)


def move(curr_entry, content, rank):
    shift_entry = None
    target_entry = None

    while curr_entry is not None:
        if curr_entry.contents == content or curr_entry.rank == content:
            target_entry = curr_entry
        if curr_entry.rank == rank:
            shift_entry = curr_entry
        curr_entry = curr_entry.next

    if target_entry.rank > rank:
        if target_entry.next is not None:
            target_entry.prev.next = target_entry.next
            target_entry.next.prev = target_entry.prev
        else:
            target_entry.prev.next = None
        target_entry.next = shift_entry
        target_entry.prev = shift_entry.prev
        if shift_entry.prev is not None:
            shift_entry.prev.next = target_entry
        shift_entry.prev = target_entry
        rank_range = target_entry.rank - rank
        target_entry.rank = rank
        refactor(target_entry.next, rank_range, 0)
    else:
        if target_entry.prev is not None:
            target_entry.prev.next = target_entry.next
            target_entry.next.prev = target_entry.prev
        else:
            target_entry.next.prev = None
        target_entry.prev = shift_entry
        if shift_entry.next is not None:
            target_entry.next = shift_entry.next
            shift_entry.next.prev = target_entry
        else:
            target_entry.next = None
        shift_entry.next = target_entry
        rank_range = rank - target_entry.rank
        target_entry.rank = rank
        refactor(target_entry, rank_range, 1)


def edit(curr_entry, target, new_content):
    if (curr_entry.rank != target) and (curr_entry.contents != target):
        this_entry = curr_entry.next
        edit(this_entry, target, new_content)
    else:
        curr_entry.contents = new_content


def check_first(curr_entry):
    if curr_entry.rank == 0:
        return curr_entry.next
    if curr_entry.prev is not None:
        if curr_entry.prev.rank == 1:
            return curr_entry.prev
    while curr_entry.prev is not None:
        curr_entry = curr_entry.prev
    return curr_entry


def refactor(curr_entry, rank_range, typeid):
    if typeid == 0:  # up
        for i in range(rank_range):
            curr_entry.rank += 1
            curr_entry = curr_entry.next
    elif typeid == 1:  # down
        for i in range(rank_range):
            curr_entry = curr_entry.prev
        for i in range(rank_range):
            curr_entry.rank -= 1
            curr_entry = curr_entry.next
    elif typeid == 2:  # when removing
        for i in range(rank_range):
            curr_entry.rank -= 1
            curr_entry = curr_entry.next


def main():
    list_size = 0
    first_entry = None
    save_flag = False
    pathway = ""

    print('== Welcome to RankList! ==')
    while True:
        startup = input('\nWould you like to "open" an existing list, start a "new" list, or "quit"?\nInput Command:>\n')
        list_size = 0
        if startup == "quit":
            break
        elif startup == "open":
            root = Tk()
            root.fileName = filedialog.askopenfilename(filetypes=(("Text Files", "*.txt"), ("All files", "*.*")))
            file2read = open(root.fileName, "r")
            fwd_file = file2read.read()  # assigns the text of the file to a huge string
            file2read.close()  # closes interaction with the file
            the_lines = fwd_file.split("\n")  # Separates the long string into all of the lines
            count = 0
            root.destroy()
            new_lines = []
            while count < len(the_lines):
                new_lines.append(the_lines[count])
                count += 1
            for i, content in enumerate(the_lines):
                build_entry = ListEntry()
                build_entry.rank = i+1
                b_contents = ""
                entry_pieces = the_lines[i].split()
                for index, value in enumerate(entry_pieces):
                    if index == 0:
                        pass
                    elif index == 1:
                        b_contents = b_contents + entry_pieces[index]
                    else:
                        b_contents = b_contents + " " + entry_pieces[index]
                build_entry.contents = b_contents
                if list_size == 0:
                    first_entry = setup_list(b_contents)
                    list_size += 1
                else:
                    add(first_entry, build_entry)
                    list_size += 1
            print("\n")
            print("List opened.\n")
            print_list(first_entry, save_flag, pathway)
            print("\n")
            first_entry = ranklist(first_entry, save_flag, pathway, list_size)

        elif startup == "new":
            print('New list created!  You may now begin adding entries.\nYou may type "help" for details about manipulating lists.\n')
            ranklist(first_entry, save_flag, pathway, list_size)


if __name__ == "__main__":
    main()
