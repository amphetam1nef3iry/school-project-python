from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import time
import importlib.util
import os

root = Tk()
root.geometry("1800x900")

HEIGHT = 35
path = ""
test_path = ""
filename = ""
testfile = ""
tfl = []
fl = []


# All the functions and variables
def select_directory():
    global path
    path = filedialog.askdirectory()
    root.title(path)
    if path == "": return
    # updating the list
    global fl
    fl = []
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)) and file.split(".")[1] == "py":
            fl.append(file)
    file_selection.set(fl)


def select_test_directory():
    global test_path
    test_path = filedialog.askdirectory()
    test_dir_label.configure(text="Current test directory: "+test_path)
    if test_path == "": return
    # updating the list
    global tfl
    tfl = []
    for file in os.listdir(test_path):
        if os.path.isfile(os.path.join(test_path, file)) and file.split(".")[1] == "txt" \
            and os.path.isfile(os.path.join(test_path, file.split(".")[0]+".py")):
            tfl.append(file.split(".")[0])
    testfile_choice.set(tfl)


def main_test():
    global path
    global test_path
    global testfile
    global filename
    if path == "" or test_path == "" or filename == "" or testfile == "":
        return
    file = os.path.join(path, filename)
    test_f = os.path.join(test_path, testfile)

    # loading the code
    spec = importlib.util.spec_from_file_location("module_name", file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    results.configure(state=NORMAL)
    results.delete("1.0", END)

    # loading the correct code
    spec2 = importlib.util.spec_from_file_location("module_name", test_f+".py")
    ans = importlib.util.module_from_spec(spec2)
    spec2.loader.exec_module(ans)

    # testing the code
    with open(test_f+".txt", "r") as fh:
        count = 1
        lines = fh.readlines()
        total = len(lines)
        successful = 0
        for line in lines:
            args = list(map(int, line.split(" ")))
            num_args = args[0]
            passing = args[1:num_args+1]
            try: 
                expected = ans.main(*passing)
                try:
                    start = time.time()
                    answer = module.main(*passing)
                    end = time.time()
                    if end - start > intvar.get()/1000:
                        contents = "Test#{} exceeded the time limit| LE\n\
                        \t Aborting...\n".format(count)
                        results.insert(END, contents)
                        break
                    elif answer == expected:
                        contents = "Test#{} is passed | OK\n".format(count)
                        results.insert(END, contents)
                        successful += 1
                    else:
                        contents = '''Wrong answer in Test#{} | WA: \n \
                \tArguments: {}\n'''.format(count, ", ".join(map(str, passing)))
                        results.insert(END, contents)
                except ArithmeticError as e:
                    contents = '''Arithmetic error in test#{} | ArithE: \n \
                \tArguments: {}\n'''.format(count, ", ".join(map(str, passing)))
                    results.insert(END, contents)
                except AttributeError as e:
                    contents = '''Attribute error in test#{} | AttribE: \n \
                \tArguments: {}\n'''.format(count, ", ".join(map(str, passing)))
                    results.insert(END, contents)
                except ImportError as e:
                    contents = '''Import error in test#{} | ImportE: \n \
                \tArguments: {}\n'''.format(count, ", ".join(map(str, passing)))
                    results.insert(END, contents)
                except LookupError as e:
                    contents = '''Lookup error in test#{} | LookupE: \n \
                \tArguments: {}\n'''.format(count, ", ".join(map(str, passing)))
                    results.insert(END, contents)
                except IndexError as e:
                    contents = '''Index error in test#{} | IndexE: \n \
                \tArguments: {}\n'''.format(count, ", ".join(map(str, passing)))
                    results.insert(END, contents)
                except KeyError as e:
                    contents = '''Key error in test#{} | KeyE: \n \
                \tArguments: {}\n'''.format(count, ", ".join(map(str, passing)))
                    results.insert(END, contents)
                except NameError as e:
                    contents = '''Name error in test#{} | NameE: \n \
                \tArguments: {}\n'''.format(count, ", ".join(map(str, passing)))
                    results.insert(END, contents)
                except SyntaxError as e:
                    contents = '''Syntax error in test#{} | SyntaxE: \n \
                \tArguments: {}\n'''.format(count, ", ".join(map(str, passing)))
                    results.insert(END, contents)
                except IndentationError as e:
                    contents = '''Indentation error in test#{} | IndentE: \n \
                \tArguments: {}\n'''.format(count, ", ".join(map(str, passing)))
                    results.insert(END, contents)
                except TypeError as e:
                    contents = '''Type error in test#{} | TypeE: \n \
                \tArguments: {}\n'''.format(count, ", ".join(map(str, passing)))
                    results.insert(END, contents)
                except ValueError as e:
                    contents = '''Value error in test#{} | ValueE: \n \
                \tArguments: {}\n'''.format(count, ", ".join(map(str, passing)))
                    results.insert(END, contents)
                except RuntimeError:
                    contents = '''Runtime error in test#{} | RE: \n \
                \tArguments: {}\n'''.format(count, ", ".join(map(str, passing)))
                    results.insert(END, contents)
                except Exception as e: 
                    contents = "Test#{} is failed for unknown(maybe internal) reason | ER\n".format(count)
                    results.insert(END, contents)
            except ArithmeticError as e:
                contents = '''Internal Arithmetic error in test#{} | ArithE: \n \
            \tArguments: {}\n'''.format(count, ", ".join(map(str, passing)))
                results.insert(END, contents)
            except AttributeError as e:
                contents = '''Internal Attribute error in test#{} | AttribE: \n \
            \tArguments: {}\n'''.format(count, ", ".join(map(str, passing)))
                results.insert(END, contents)
            except ImportError as e:
                contents = '''Internal Import error in test#{} | ImportE: \n \
            \tArguments: {}\n'''.format(count, ", ".join(map(str, passing)))
                results.insert(END, contents)
            except LookupError as e:
                contents = '''Internal Lookup error in test#{} | LookupE: \n \
            \tArguments: {}\n'''.format(count, ", ".join(map(str, passing)))
                results.insert(END, contents)
            except IndexError as e:
                contents = '''Internal Index error in test#{} | IndexE: \n \
            \tArguments: {}\n'''.format(count, ", ".join(map(str, passing)))
                results.insert(END, contents)
            except KeyError as e:
                contents = '''Internal Key error in test#{} | KeyE: \n \
            \tArguments: {}\n'''.format(count, ", ".join(map(str, passing)))
                results.insert(END, contents)
            except NameError as e:
                contents = '''Internal Name error in test#{} | NameE: \n \
            \tArguments: {}\n'''.format(count, ", ".join(map(str, passing)))
                results.insert(END, contents)
            except SyntaxError as e:
                contents = '''Internal Syntax error in test#{} | SyntaxE: \n \
            \tArguments: {}\n'''.format(count, ", ".join(map(str, passing)))
                results.insert(END, contents)
            except IndentationError as e:
                contents = '''Internal Indentation error in test#{} | IndentE: \n \
            \tArguments: {}\n'''.format(count, ", ".join(map(str, passing)))
                results.insert(END, contents)
            except TypeError as e:
                contents = '''Internal Type error in test#{} | TypeE: \n \
            \tArguments: {}\n'''.format(count, ", ".join(map(str, passing)))
                results.insert(END, contents)
            except ValueError as e:
                contents = '''Internal Value error in test#{} | ValueE: \n \
            \tArguments: {}\n'''.format(count, ", ".join(map(str, passing)))
                results.insert(END, contents)
            except RuntimeError as e:
                contents = '''Internal Runtime error in test#{} | RE: \n \
            \tArguments: {}\n'''.format(count, ", ".join(map(str, passing)))
                results.insert(END, contents)
            except Exception as e: # all kinds of exceptions
                contents = '''Internal Internal error in test#{} | IE: \n \
                \tArguments: {}\n'''.format(count, ", ".join(map(str, passing)))
                results.insert(END, contents)
            count +=1
    results.configure(state=DISABLED)
    t = "{} out of {} passed, {}%".format(successful, total, successful*100//total)
    passed_text.configure(text=t)


def select_file(w):
    if len(dir_list.curselection()) < 1: return
    global filename
    filename= fl[int(dir_list.curselection()[0])]
    file = os.path.join(path, filename)
    with open(file, "r") as fh:
        contents = fh.readlines()
    contents = "".join(contents)
    text.configure(state=NORMAL)
    text.delete("1.0", END)
    text.insert(INSERT, contents)
    text.configure(state=DISABLED)


def select_test(w):
    if len(testlist.curselection()) < 1: return
    global testfile
    testfile = tfl[int(testlist.curselection()[0])]


mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
dirs = ttk.Labelframe(mainframe, text="Directory: ")
dirs.grid(column=0, row=1, sticky=NW, pady=0)

# choices for the listbox
file_selection = StringVar()
dir_list = Listbox(dirs, selectbackground="lightgreen", listvariable=file_selection, height=HEIGHT)
dir_list.bind("<<ListboxSelect>>", select_file)
dir_list.grid(row=1, column=0, sticky=NS, pady=0)

# displaying the code
code = ttk.LabelFrame(mainframe, text=filename)
code.grid(column=1, row=1, rowspan=2, sticky=N)
code_contents = "Select a file, please"
text = Text(code, height=HEIGHT)
text.insert(INSERT, code_contents)
text.configure(state=DISABLED)
text.grid(column=1, row=0)

# Menu bar
menu_bar = Menu(root)
utils = Menu(menu_bar, tearoff=0)
utils.add_command(label="Open directory", command=select_directory)
utils.add_command(label="Open test directory", command=select_test_directory)
menu_bar.add_cascade(label="Utils", menu=utils)

# The test frame
tests = ttk.LabelFrame(mainframe, text="Tests: ")
tests.grid(column=2, row=1, rowspan=2, sticky=N)
testfile_choice = StringVar()
testlist = Listbox(tests, listvariable=testfile_choice, height=HEIGHT)
testlist.bind("<<ListboxSelect>>", select_test)
testlist.grid()

# Displaying the testing directory path
test_dir_label = Label(mainframe, text="Select a testing directory", anchor=CENTER)
test_dir_label.grid(row=0, column=0, columnspan=4, sticky=N)

# Testing
answers = ttk.LabelFrame(mainframe, tex="Results:")
answers.grid(column=3, row=1, rowspan=2, sticky=NS)
results = Text(answers, height=HEIGHT-1)
test = Button(answers, text="Test", anchor=CENTER, width=6, height=1,
 activeforeground="green", padx=5, pady=2, command=main_test)
test.grid(column=0, row=0, sticky=W)

# time limit part
time_limit = ttk.Frame(answers)
time_limit.grid(column=1, row=0, sticky=W)

time_limit_text = Label(time_limit, text="Time limit in ms: ")
time_limit_text.grid(column=0, row=0, sticky=W)

intvar = IntVar(time_limit, value=400)
entry = Entry(time_limit, width=5, text=intvar)
entry.grid(column=1, row=0, padx=5, sticky=W)

passed_text = Label(answers, text="? out of ? passed")
passed_text.grid(column=2, row=0, sticky=W)

framet = ttk.Frame(answers)
framet.grid(column=0, row=1)

# Testing results
results.configure(state=DISABLED)
results.grid(column=0, row=1, columnspan=3)


root.config(menu=menu_bar)
root.title("Select directory")
root.mainloop()
